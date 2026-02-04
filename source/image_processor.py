import cv2

class ImageProcessor:
    """
    Handles all image processing using OpenCV.
    GUI should call this class instead of writing OpenCV code inside Tkinter.
    """

    def __init__(self):
        # Encapsulation: store image data inside the class
        self._image_bgr = None
        self._filepath = None

    def _require_image(self):
        """Stops filters from crashing if no image is loaded yet."""
        if self._image_bgr is None:
            raise ValueError("No image loaded. Please open an image first.")

    def load(self, filepath):
        """
        Loads an image from disk.
        We use cv2.imread because it supports common formats like JPG/PNG/BMP.
        """
        img = cv2.imread(filepath)
        if img is None:
            raise ValueError("Could not read image. Use JPG, PNG, or BMP.")
        self._image_bgr = img
        self._filepath = filepath
        return self.get_image()

    def set_image(self, image_bgr):
        """Stores a copy so outside code cannot accidentally change our image."""
        self._image_bgr = image_bgr.copy()

    def get_image(self):
        """Returns a copy to protect internal data (encapsulation)."""
        return None if self._image_bgr is None else self._image_bgr.copy()

    def get_filepath(self):
        return self._filepath

    def get_dimensions(self):
        self._require_image()
        h, w = self._image_bgr.shape[:2]
        return w, h

    # ---------- Image Processing Features ----------

    def grayscale(self):
        self._require_image()
        # Convert to gray (single channel), then back to BGR so GUI always receives 3 channels.
        gray = cv2.cvtColor(self._image_bgr, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def blur(self, intensity):
        self._require_image()
        # Gaussian blur kernel must be odd, so we force odd number.
        k = max(1, int(intensity))
        if k % 2 == 0:
            k += 1
        return cv2.GaussianBlur(self._image_bgr, (k, k), 0)

    def edges(self):
        self._require_image()
        # Canny works better on grayscale images.
        gray = cv2.cvtColor(self._image_bgr, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 50, 150)
        return cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    def brightness(self, beta):
        self._require_image()
        # beta increases/decreases brightness; alpha stays 1.0 (no contrast change here).
        return cv2.convertScaleAbs(self._image_bgr, alpha=1.0, beta=int(beta))

    def contrast(self, alpha):
        self._require_image()
        # alpha controls contrast; beta stays 0 (no brightness change here).
        return cv2.convertScaleAbs(self._image_bgr, alpha=float(alpha), beta=0)

    def rotate(self, angle):
        self._require_image()
        if angle == 90:
            return cv2.rotate(self._image_bgr, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            return cv2.rotate(self._image_bgr, cv2.ROTATE_180)
        elif angle == 270:
            return cv2.rotate(self._image_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return self._image_bgr.copy()

    def flip(self, mode):
        self._require_image()
        # mode "h" = horizontal, "v" = vertical
        if mode == "h":
            return cv2.flip(self._image_bgr, 1)
        elif mode == "v":
            return cv2.flip(self._image_bgr, 0)
        return self._image_bgr.copy()

    def resize(self, scale):
        self._require_image()
        h, w = self._image_bgr.shape[:2]
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        return cv2.resize(self._image_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
