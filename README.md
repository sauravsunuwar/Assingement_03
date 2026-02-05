# Assingement_03
Image Editor Application

HIT137 – Assignment 3

📌 Overview

This project is a desktop Image Editor application developed using Python, Tkinter, and OpenCV.
It demonstrates Object-Oriented Programming (OOP) principles, GUI development, and basic image processing operations.

The application allows users to load, edit, transform, and save images through an interactive graphical interface.

✨ Features
📂 File Operations

Open images (.jpg, .jpeg, .png, .bmp)

Save image

Save image as a new file

Reset image to original

Exit with confirmation

🎨 Basic Filters

Grayscale

Edge Detection (Canny)

Edge Detection with adjustable thresholds

🔧 Adjustments

Blur (adjustable kernel size)

Brightness control

Contrast control

🔄 Transformations

Rotate (90°, 180°, 270°)

Flip (horizontal / vertical)

Resize (percentage-based)

Zoom in / Zoom out / Reset zoom (view-only)

↩️ History Management

Undo

Redo

🧠 OOP Design

The application is structured using multiple classes to maintain clean separation of responsibilities:

File	Purpose
app.py	Main GUI application and user interaction logic
image_processor.py	Image processing operations using OpenCV
history_manager.py	Undo/Redo image history management
main.py	Application entry point
🛠️ Technologies Used

Python 3.14

Tkinter (GUI)

OpenCV (cv2) – image processing

Pillow (PIL) – image rendering in GUI

NumPy

📦 Installation & Setup
1️⃣ Install dependencies

Make sure you are in the project root directory:

pip install -r requirements.txt

2️⃣ Navigate to source folder
cd source

3️⃣ Run the application
python main.py

📁 Project Structure
Assingement_03/
│
├── requirements.txt
├── README.md
│
└── source/
    ├── app.py
    ├── main.py
    ├── image_processor.py
    ├── history_manager.py
    └── __pycache__/

⚠️ Notes

Zoom is view-only and does not affect the saved image.

Undo/Redo works for all image transformations.

The left control panel is scrollable to accommodate all features.

👨‍🎓 Author Group Members:
Saurab Kumar Sunuwar -S397374 
Ujwal Lamsal -S399646 
Anish Bhattarai - S398108 
Bibek Guurung - S397310
Unit: HIT137
Institution: Charles Darwin University
Note:all the work has been equally done and distributed.
