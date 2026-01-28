import tkinter as tk
from app import ImageEditorApp

def main():
    print("Starting app...")
    root = tk.Tk()
    ImageEditorApp(root)
    print("Entering mainloop...")
    root.mainloop()

if __name__ == "__main__":
    main()
