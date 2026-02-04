"""
Image processing module (OpenCV).

This file is responsible ONLY for image processing logic.
The GUI (Tkinter) should call these methods to apply effects.

Assignment required filters (all included here):
1) Grayscale
2) Blur (Gaussian) - adjustable
3) Edge detection (Canny)
4) Brightness adjustment
5) Contrast adjustment
6) Rotation (90/180/270)
7) Flip (horizontal/vertical)
8) Resize/Scale
"""

from __future__ import annotations

from typing import Optional, Tuple
import cv2


class BaseProcessor:
    """
    Parent class (used to demonstrate inheritance).

    Why this class exists:
    - Encapsulation: store image and file path inside the object.
    - Reuse: child classes can reuse helper methods like _require_image().
    """

    def __init__(self) -> None:
        self._image_bgr: Optional["cv2.MatLike"] = None
        self._filepath: Optional[str] = None

    # ---------- Encapsulation helpers ----------

    def has_image(self) -> bool:
        """Returns True if an image is currently loaded."""
        return self._image_bgr is not None

    def _require_image(self) -> None:
        """
        Why we do this:
        - If user clicks a filter without opening an image, OpenCV would crash.
        - We raise a clear error so GUI can show a friendly message box.
        """
        if self._image_bgr is None:
            raise ValueError("No image loaded. Please open an image first.")

    def get_image(self):
        """
        Returns a COPY of the image (or None).
        Why copy:
        - prevents other code from modifying our internal image accidentally.
        """
        return None if self._image_bgr is None else self._image_bgr.copy()

    def set_image(self, image_bgr) -> None:
        """
        Stores a new image (copy).
        Supports undo/redo: app can restore older images safely.
        """
        if image_bgr is None:
            self._image_bgr = None
            return
        self._image_bgr = image_bgr.copy()

    def get_filepath(self) -> Optional[str]:
        """Returns the path of the last loaded image (or None)."""
        return self._filepath

    def get_dimensions(self) -> Tuple[int, int]:
        """Returns (width, height)."""
        self._require_image()
        h, w = self._image_bgr.shape[:2]
        return w, h


class ImageProcessor(BaseProcessor):
    """
    Child class (inherits from BaseProcessor).
    Implements all required OpenCV filters.
    """

    def __init__(self) -> None:
        super().__init__()

    # ---------- Loading / Saving ----------

    def load(self, filepath: str):
        """
        Loads an image from disk.

        Why cv2.imread:
        - supports common formats (JPG, PNG, BMP) required by assignment.
        """
        img = cv2.imread(filepath)
        if img is None:
            raise ValueError("Could not read image. Please use JPG, PNG, or BMP.")
        self._image_bgr = img
        self._filepath = filepath
        return self.get_image()

    def save(self, filepath: str) -> None:
        """
        Saves the current image to a file.
        This is optional for GUI, but shows strong OOP design.
        """
        self._require_image()
        ok = cv2.imwrite(filepath, self._image_bgr)
        if not ok:
            raise ValueError("Could not save image to the selected path.")

    # ---------- Required Filters ----------

    def grayscale(self):
        """Converts the image to grayscale (then back to BGR for consistent display)."""
        self._require_image()
        gray = cv2.cvtColor(self._image_bgr, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def blur(self, intensity):
        """
        Applies Gaussian blur with adjustable intensity.
        OpenCV requires odd kernel width/height, so we force odd.
        """
        self._require_image()
        k = max(1, int(intensity))
        if k % 2 == 0:
            k += 1
        return cv2.GaussianBlur(self._image_bgr, (k, k), 0)

    def edges(self):
        """Canny edge detection (uses grayscale internally)."""
        self._require_image()
        gray = cv2.cvtColor(self._image_bgr, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 50, 150)
        return cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    def brightness(self, beta):
        """Brightness adjustment using beta."""
        self._require_image()
        return cv2.convertScaleAbs(self._image_bgr, alpha=1.0, beta=int(beta))

    def contrast(self, alpha):
        """Contrast adjustment using alpha (clamped to avoid unusable images)."""
        self._require_image()
        alpha_f = max(0.1, min(float(alpha), 3.0))
        return cv2.convertScaleAbs(self._image_bgr, alpha=alpha_f, beta=0)

    def rotate(self, angle: int):
        """Rotate image by 90, 180, or 270 degrees."""
        self._require_image()
        if angle == 90:
            return cv2.rotate(self._image_bgr, cv2.ROTATE_90_CLOCKWISE)
        if angle == 180:
            return cv2.rotate(self._image_bgr, cv2.ROTATE_180)
        if angle == 270:
            return cv2.rotate(self._image_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return self._image_bgr.copy()

    def flip(self, mode: str):
        """Flip image horizontally ('h') or vertically ('v')."""
        self._require_image()
        if mode == "h":
            return cv2.flip(self._image_bgr, 1)
        if mode == "v":
            return cv2.flip(self._image_bgr, 0)
        return self._image_bgr.copy()

    def resize(self, scale):
        """Resize/scale image with clamped scale value."""
        self._require_image()
        scale_f = max(0.1, min(float(scale), 5.0))

        h, w = self._image_bgr.shape[:2]
        new_w = max(1, int(w * scale_f))
        new_h = max(1, int(h * scale_f))
        return cv2.resize(self._image_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
