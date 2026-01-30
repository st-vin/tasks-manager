"""UI utilities: gradient images for KPI cards (PIL)."""

from typing import Tuple, TYPE_CHECKING

try:
    from PIL import Image
    from PIL import ImageTk
except ImportError:
    Image = None
    ImageTk = None

if TYPE_CHECKING:
    from tkinter import PhotoImage


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert #RRGGBB to (r, g, b)."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def create_vertical_gradient_image(
    width: int,
    height: int,
    top_color: str,
    bottom_color: str,
) -> "Image.Image":
    """Create a PIL Image with vertical gradient."""
    if Image is None:
        raise RuntimeError("Pillow is required for gradient images. Install with: pip install Pillow")
    top = hex_to_rgb(top_color)
    bottom = hex_to_rgb(bottom_color)
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for y in range(height):
        t = y / max(height - 1, 1)
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        for x in range(width):
            pixels[x, y] = (r, g, b)
    return img


def gradient_photo(width: int, height: int, top_color: str, bottom_color: str) -> "PhotoImage":
    """Create a tkinter PhotoImage for use as background. Caller must keep a reference."""
    if ImageTk is None:
        raise RuntimeError("Pillow is required. Install with: pip install Pillow")
    img = create_vertical_gradient_image(width, height, top_color, bottom_color)
    return ImageTk.PhotoImage(img)
