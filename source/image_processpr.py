import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.image_bgr = None
        self.filepath = None

    def load(self, filepath):
        img = cv2.imread(filepath)
        if img is None:
            raise ValueError("Could not read image. Use JPG, PNG, or BMP.")
        self.image_bgr = img
        self.filepath = filepath
        return self.image_bgr

    def set_image(self, image_bgr):
        self.image_bgr = image_bgr.copy()

    def get_image(self):
        return None if self.image_bgr is None else self.image_bgr.copy()

    # ---------- Image Processing Features ----------

    def grayscale(self):
        gray = cv2.cvtColor(self.image_bgr, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def blur(self, intensity):
        k = max(1, int(intensity))
        if k % 2 == 0:
            k += 1
        return cv2.GaussianBlur(self.image_bgr, (k, k), 0)

    def edges(self):
        gray = cv2.cvtColor(self.image_bgr, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 50, 150)
        return cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    def brightness(self, beta):
        return cv2.convertScaleAbs(self.image_bgr, alpha=1.0, beta=int(beta))

    def contrast(self, alpha):
        return cv2.convertScaleAbs(self.image_bgr, alpha=float(alpha), beta=0)

    def rotate(self, angle):
        if angle == 90:
            return cv2.rotate(self.image_bgr, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            return cv2.rotate(self.image_bgr, cv2.ROTATE_180)
        elif angle == 270:
            return cv2.rotate(self.image_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return self.image_bgr.copy()

    def flip(self, mode):
        if mode == "h":
            return cv2.flip(self.image_bgr, 1)
        elif mode == "v":
            return cv2.flip(self.image_bgr, 0)
        return self.image_bgr.copy()

    def resize(self, scale):
        h, w = self.image_bgr.shape[:2]
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        return cv2.resize(
            self.image_bgr,
            (new_w, new_h),
            interpolation=cv2.INTER_AREA
        )
