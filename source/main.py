# main.py
"""
Entry point for the Tkinter + OpenCV Image Editor.

Why keep this file small:
- Clean project structure
- Easy for markers to run: python main.py
"""

import tkinter as tk
from tkinter import messagebox
from app import ImageEditorApp


def main() -> None:
    """
    Starts the application safely.
    If something unexpected crashes, a message box will show the error.
    """
    try:
        root = tk.Tk()
        ImageEditorApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Application Error", str(e))


if __name__ == "__main__":
    main()
