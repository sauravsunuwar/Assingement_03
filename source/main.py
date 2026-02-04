import tkinter as tk
from tkinter import messagebox
from app import ImageEditorApp

def main():
    try:
        root = tk.Tk()
        ImageEditorApp(root)
        root.mainloop()
    except Exception as e:
        # If something unexpected happens, show a user-friendly message
        messagebox.showerror("Application Error", str(e))

if __name__ == "__main__":
    main()
