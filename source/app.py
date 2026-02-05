"""
HIT137 Assignment 3 - Image Editor Application
Main application file with Tkinter GUI
Demonstrates OOP principles, OpenCV image processing, and GUI development
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import cv2
import numpy as np
from history_manager import HistoryManager
from image_processor import ImageProcessor
from PIL import Image, ImageTk


class ImageEditorApp:
    """
    Main application class for the Image Editor.
    Handles GUI creation, user interactions, and coordinates between
    ImageProcessor and HistoryManager classes.
    
    Demonstrates:
    - Encapsulation: Private methods with underscore prefix
    - Constructor: __init__ method initializes all components
    - Methods: Multiple methods for different functionalities
    - Class Interaction: Works with ImageProcessor and HistoryManager
    """
    
    def __init__(self, root):
        """
        Constructor: Initialize the Image Editor application
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Image Editor - HIT137 Assignment 3")
        self.root.geometry("1200x700")
        
        # Initialize image processor and history manager (Class Interaction)
        self.processor = ImageProcessor()
        self.history = HistoryManager()
        
        # Current state variables (Encapsulation)
        self.current_path = None
        self.tk_img = None
        self.original_image = None
        
        # Build GUI components
        self._build_menu()
        self._build_ui()
        self._set_status("No image loaded. Use File > Open to load an image.")
        # Keyboard Shortcuts 
        self.root.bind("<Control-o>", lambda e: self.open_image())
        self.root.bind("<Control-s>", lambda e: self.save_image())
        self.root.bind("<Control-Shift-S>", lambda e: self.save_as_image())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())

    
    def _build_menu(self):
        """Private method to build the menu bar (Encapsulation)"""
        menubar = tk.Menu(self.root)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_image, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._exit_application)
        
        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Reset to Original", command=self.reset_to_original)
        
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        self.root.config(menu=menubar)
    
    def _build_ui(self):
        """Private method to build the main user interface (Encapsulation)"""
        # Left control panel
        self.left_panel = tk.Frame(self.root, width=280, bg="#f0f0f0")
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.left_panel.pack_propagate(False)
        
        # Right image display area
        self.right_panel = tk.Frame(self.root, bg="#2b2b2b")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Image canvas
        self.canvas = tk.Label(self.right_panel, bg="#2b2b2b", text="No Image Loaded", 
                            fg="white", font=("Arial", 16))
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Build control sections
        self._build_basic_filters()
        self._build_adjustment_controls()
        self._build_transform_controls()
        
        # Status bar at bottom
        self.status = tk.StringVar()
        status_bar = tk.Label(self.root, textvariable=self.status, anchor="w", 
                            relief=tk.SUNKEN, bg="#e0e0e0", font=("Arial", 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _build_basic_filters(self):
        """Build basic filter buttons section"""
        frame = tk.LabelFrame(self.left_panel, text="Basic Filters", 
                            font=("Arial", 10, "bold"), bg="#f0f0f0", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(frame, text="Grayscale", command=self.apply_grayscale, 
                width=20, bg="#4CAF50", fg="white").pack(pady=3)
        tk.Button(frame, text="Edge Detection", command=self.apply_edges, 
                width=20, bg="#2196F3", fg="white").pack(pady=3)
        
                # Edge Detection sliders (Canny thresholds)
        tk.Label(frame, text="Edge Detection (Canny):", bg="#f0f0f0").pack(anchor="w", pady=(10, 0))

        tk.Label(frame, text="Threshold 1 (0-255):", bg="#f0f0f0").pack(anchor="w")
        self.edge_t1 = tk.Scale(frame, from_=0, to=255, orient=tk.HORIZONTAL,
                                length=200, bg="#f0f0f0")
        self.edge_t1.set(50)
        self.edge_t1.pack(fill=tk.X, pady=(0, 5))

        tk.Label(frame, text="Threshold 2 (0-255):", bg="#f0f0f0").pack(anchor="w")
        self.edge_t2 = tk.Scale(frame, from_=0, to=255, orient=tk.HORIZONTAL,
                                length=200, bg="#f0f0f0")
        self.edge_t2.set(150)
        self.edge_t2.pack(fill=tk.X, pady=(0, 5))

        tk.Button(frame, text="Apply Edge (Sliders)", command=self.apply_edges_slider,
                  width=20, bg="#03A9F4", fg="white").pack(pady=3)

    
    def _build_adjustment_controls(self):
        """Build adjustment controls with sliders section"""
        frame = tk.LabelFrame(self.left_panel, text="Adjustments", 
                            font=("Arial", 10, "bold"), bg="#f0f0f0", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Blur slider
        tk.Label(frame, text="Blur Intensity (1-31):", bg="#f0f0f0").pack(anchor="w", pady=(5,0))
        self.blur_slider = tk.Scale(frame, from_=1, to=31, orient=tk.HORIZONTAL, 
                                resolution=2, length=200, bg="#f0f0f0")
        self.blur_slider.set(1)
        self.blur_slider.pack(fill=tk.X, pady=(0,5))
        tk.Button(frame, text="Apply Blur", command=self.apply_blur, 
                width=20, bg="#FF9800", fg="white").pack(pady=3)
        
        # Brightness slider
        tk.Label(frame, text="Brightness (-100 to +100):", bg="#f0f0f0").pack(anchor="w", pady=(10,0))
        self.brightness_slider = tk.Scale(frame, from_=-100, to=100, orient=tk.HORIZONTAL, 
                                        length=200, bg="#f0f0f0")
        self.brightness_slider.set(0)
        self.brightness_slider.pack(fill=tk.X, pady=(0,5))
        tk.Button(frame, text="Apply Brightness", command=self.apply_brightness, 
                width=20, bg="#9C27B0", fg="white").pack(pady=3)
        
        # Contrast slider
        tk.Label(frame, text="Contrast (0.5 to 3.0):", bg="#f0f0f0").pack(anchor="w", pady=(10,0))
        self.contrast_slider = tk.Scale(frame, from_=0.5, to=3.0, resolution=0.1, 
                                    orient=tk.HORIZONTAL, length=200, bg="#f0f0f0")
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(fill=tk.X, pady=(0,5))
        tk.Button(frame, text="Apply Contrast", command=self.apply_contrast, 
                width=20, bg="#673AB7", fg="white").pack(pady=3)
    
    def _build_transform_controls(self):
        """Build transformation controls section"""
        frame = tk.LabelFrame(self.left_panel, text="Transformations", 
                            font=("Arial", 10, "bold"), bg="#f0f0f0", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Rotation buttons
        tk.Label(frame, text="Rotate:", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5,2))
        rotation_frame = tk.Frame(frame, bg="#f0f0f0")
        rotation_frame.pack(fill=tk.X, pady=3)
        tk.Button(rotation_frame, text="90°", command=lambda: self.apply_rotation(90), 
                width=6, bg="#00BCD4", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(rotation_frame, text="180°", command=lambda: self.apply_rotation(180), 
                width=6, bg="#00BCD4", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(rotation_frame, text="270°", command=lambda: self.apply_rotation(270), 
                width=6, bg="#00BCD4", fg="white").pack(side=tk.LEFT, padx=2)
        
        # Flip buttons
        tk.Label(frame, text="Flip:", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10,2))
        flip_frame = tk.Frame(frame, bg="#f0f0f0")
        flip_frame.pack(fill=tk.X, pady=3)
        tk.Button(flip_frame, text="Horizontal", command=lambda: self.apply_flip("horizontal"), 
                width=10, bg="#009688", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(flip_frame, text="Vertical", command=lambda: self.apply_flip("vertical"), 
                width=10, bg="#009688", fg="white").pack(side=tk.LEFT, padx=2)
        
        # Resize controls
        tk.Label(frame, text="Resize (%):", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10,2))
        self.resize_slider = tk.Scale(frame, from_=10, to=200, orient=tk.HORIZONTAL, 
                                    length=200, bg="#f0f0f0")
        self.resize_slider.set(100)
        self.resize_slider.pack(fill=tk.X, pady=(0,5))
        
        tk.Button(frame, text="Apply Resize", command=self.apply_resize, 
                width=20, bg="#795548", fg="white").pack(pady=3)
        # Zoom controls (view-only)
        tk.Label(frame, text="Zoom:", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 2))
        zoom_frame = tk.Frame(frame, bg="#f0f0f0")
        zoom_frame.pack(fill=tk.X, pady=3)

        tk.Button(zoom_frame, text="Zoom +", command=self.zoom_in,
                  width=8, bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(zoom_frame, text="Zoom -", command=self.zoom_out,
                  width=8, bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(zoom_frame, text="Reset", command=self.zoom_reset,
                  width=8, bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=2)

    
    def _set_status(self, text):
        """Update status bar text (Private method - Encapsulation)"""
        self.status.set(text)
    
    def _exit_application(self):
        """Handle application exit with confirmation"""
        if messagebox.askokcancel("Exit", "Do you want to exit the application?"):
            self.root.quit()
    
    # ==================== File Operations ====================
    
    def open_image(self):
        """
        Open an image file using file dialog.
        Supports JPG, PNG, and BMP formats as required.
        """
        path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("All Images", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("BMP files", "*.bmp")
            ]
        )
        if not path:
            return
        
        try:
            # Load image using ImageProcessor
            img = self.processor.load(path)
            self.original_image = img.copy()
            self.current_path = path
            
            # Reset history and add initial image
            self.history.reset()
            self.history.push(img.copy())
            
            # Display image
            self.show_image(img)
            
            # Update status bar with image info
            h, w = img.shape[:2]
            channels = img.shape[2] if len(img.shape) == 3 else 1
            self._set_status(f"Loaded: {path.split('/')[-1]} | Size: {w}x{h} | Channels: {channels}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
    
    def save_image(self):
        """Save the current image to the current path"""
        if self.processor.get_image() is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        
        if not self.current_path:
            self.save_as_image()
            return
        
        try:
            cv2.imwrite(self.current_path, self.processor.get_image())
            messagebox.showinfo("Success", f"Image saved to:\n{self.current_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")
    
    def save_as_image(self):
        """Save the current image to a new path"""
        if self.processor.get_image() is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("BMP files", "*.bmp")
            ]
        )
        if not path:
            return
        
        try:
            cv2.imwrite(path, self.processor.get_image())
            self.current_path = path
            messagebox.showinfo("Success", f"Image saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")
    
    # ==================== Display Methods ====================
    
    def show_image(self, image_bgr):
        """
        Display an OpenCV image (BGR format) on the canvas.
        Converts to RGB and resizes to fit the display area.
        """
        if image_bgr is None:
            return
        
        # Convert BGR to RGB for display
        if len(image_bgr.shape) == 2:  # Grayscale
            rgb = cv2.cvtColor(image_bgr, cv2.COLOR_GRAY2RGB)
        else:
            rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image and resize to fit canvas
        pil_img = Image.fromarray(rgb)
        pil_img.thumbnail((900, 650), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage and display
        self.tk_img = ImageTk.PhotoImage(pil_img)
        self.canvas.config(image=self.tk_img, text="")
    
    # ==================== Edit Operations ====================
    
    def undo(self):
        """Undo the last operation"""
        img = self.history.undo()
        if img is not None:
            self.processor.set_image(img)
            self.show_image(img)
            self._set_status("Undo successful")
        else:
            messagebox.showinfo("Info", "Nothing to undo!")
    
    def redo(self):
        """Redo the last undone operation"""
        img = self.history.redo()
        if img is not None:
            self.processor.set_image(img)
            self.show_image(img)
            self._set_status("Redo successful")
        else:
            messagebox.showinfo("Info", "Nothing to redo!")
    
    def reset_to_original(self):
        """Reset image to original state"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        
        if messagebox.askyesno("Reset", "Reset to original image?"):
            self.processor.set_image(self.original_image.copy())
            self.history.reset()
            self.history.push(self.original_image.copy())
            self.show_image(self.original_image)
            self._set_status("Image reset to original")
    
    # ==================== Image Processing Methods ====================
    
    def apply_grayscale(self):
        """Apply grayscale filter"""
        if self.processor.get_image() is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        img = self.processor.grayscale()
        self.history.push(img.copy())
        self.show_image(img)
        self._set_status("Applied: Grayscale")
    
    def apply_edges(self):
        """Apply Canny edge detection"""
        if self.processor.get_image() is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        img = self.processor.edges()
        self.history.push(img.copy())
        self.show_image(img)
        self._set_status("Applied: Edge Detection (Canny)")

    def apply_edges_slider(self):
        """Apply Canny edge detection using threshold sliders"""
        if self.processor.get_image() is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return

        t1 = self.edge_t1.get()
        t2 = self.edge_t2.get()

        if t1 >= t2:
            messagebox.showerror("Error", "Threshold 1 must be less than Threshold 2.")
            return

        img = self.processor.edges(t1, t2)
        self.processor.set_image(img)
        self.history.push(img.copy())
        self.show_image(img)
        self._set_status(f"Applied: Edge Detection (t1={t1}, t2={t2})")

    
    def apply_blur(self):
        """Apply Gaussian blur with adjustable intensity"""
        if self.processor.get_image() is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        kernel_size = self.blur_slider.get()
        img = self.processor.blur(kernel_size)
        self.history.push(img.copy())
        self.show_image(img)
        self._set_status(f"Applied: Blur (kernel size: {kernel_size})")
    
    def apply_brightness(self):
        """Apply brightness adjustment"""
        if self.processor.get_image() is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        value = self.brightness_slider.get()
        img = self.processor.brightness(value)
        self.processor.set_image(img)
        self.history.push(img.copy())
        self.show_image(img)
        self._set_status(f"Applied: Brightness ({value:+d})")
    
    def apply_contrast(self):
        """Apply contrast adjustment"""
        if self.processor.get_image() is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        value = self.contrast_slider.get()
        img = self.processor.contrast(value)
        self.processor.set_image(img)
        self.history.push(img.copy())
        self.show_image(img)
        self._set_status(f"Applied: Contrast ({value:.1f}x)")
    
    def apply_rotation(self, angle):
        """Apply rotation by specified angle (90, 180, or 270 degrees)"""
        if self.processor.get_image() is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        img = self.processor.rotate(angle)
        self.history.push(img.copy())
        self.show_image(img)
        self._set_status(f"Applied: Rotation ({angle}°)")
    
    def apply_flip(self, direction):
        """Apply flip (horizontal or vertical)"""
        if self.processor.get_image() is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        mode = "h" if direction == "horizontal" else "v"
        img = self.processor.flip(mode)
        self.processor.set_image(img)
        self.history.push(img.copy())
        self.show_image(img)
        self._set_status(f"Applied: Flip ({direction})")
    
    def apply_resize(self):
        """Apply resize/scale based on percentage"""
        if self.processor.get_image() is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        scale_percent = self.resize_slider.get()
        scale_factor = scale_percent / 100.0
        img = self.processor.resize(scale_factor)
        self.processor.set_image(img)
        self.history.push(img.copy())
        self.show_image(img)
        h, w = img.shape[:2]
        self._set_status(f"Applied: Resize ({scale_percent}%) | New size: {w}x{h}")


# ==================== Main Execution ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()