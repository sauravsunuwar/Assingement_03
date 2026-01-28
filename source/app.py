import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

from image_processor import ImageProcessor

from history_manager import HistoryManager


class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor (Tkinter + OpenCV)")
        self.root.geometry("1000x650")

        self.processor = ImageProcessor()
        self.history = HistoryManager()

        self.current_path = None
        self.tk_img = None

        self._build_menu()
        self._build_ui()
        self._set_status("No image loaded")

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label="Save As", command=self.save_as_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menubar)

    def _build_ui(self):
        self.left = tk.Frame(self.root, width=230)
        self.left.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        self.right = tk.Frame(self.root)
        self.right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.canvas = tk.Label(self.right, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.left, text="Controls", font=("Arial", 12, "bold")).pack(pady=(0, 10))

        tk.Button(self.left, text="Grayscale", command=self.apply_grayscale).pack(fill=tk.X, pady=4)
        tk.Button(self.left, text="Edge Detection", command=self.apply_edges).pack(fill=tk.X, pady=4)

        tk.Label(self.left, text="Blur Intensity").pack(pady=(12, 2))
        self.blur_slider = tk.Scale(self.left, from_=1, to=31, orient=tk.HORIZONTAL, command=self.apply_blur)
        self.blur_slider.set(1)
        self.blur_slider.pack(fill=tk.X, pady=4)

        self.status = tk.StringVar()
        status_bar = tk.Label(self.root, textvariable=self.status, anchor="w", relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _set_status(self, text):
        self.status.set(text)

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")]
        )
        if not path:
            return

        try:
            img = self.processor.load(path)
            self.history.reset()
            self.history.push(img)
            self.show_image(img)
            h, w = img.shape[:2]
            self._set_status(f"{path} | {w}x{h}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_image(self):
        if self.processor.get_image() is None:
            return
        if not self.current_path:
            self.save_as_image()
            return
        cv2.imwrite(self.current_path, self.processor.get_image())

    def save_as_image(self):
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if not path:
            return
        cv2.imwrite(path, self.processor.get_image())
        self.current_path = path

    def show_image(self, image_bgr):
        rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        pil.thumbnail((800, 600))
        self.tk_img = ImageTk.PhotoImage(pil)
        self.canvas.config(image=self.tk_img)

    def undo(self):
        img = self.history.undo()
        if img is not None:
            self.processor.set_image(img)
            self.show_image(img)

    def redo(self):
        img = self.history.redo()
        if img is not None:
            self.processor.set_image(img)
            self.show_image(img)

    def apply_grayscale(self):
        img = self.processor.grayscale()
        self.history.push(img)
        self.show_image(img)

    def apply_edges(self):
        img = self.processor.edges()
        self.history.push(img)
        self.show_image(img)

    def apply_blur(self, _):
        img = self.processor.blur(self.blur_slider.get())
        self.history.push(img)
        self.show_image(img)
