from PIL import Image
import mss
from PySide6.QtCore import QRect


def primary_screen_region(geometry: QRect) -> tuple[int, int, int, int]:
    return (
        geometry.x(),
        geometry.y(),
        geometry.x() + geometry.width(),
        geometry.y() + geometry.height(),
    )


def capture_region(region: tuple[int, int, int, int]) -> Image.Image:
    left, top, right, bottom = region
    if right <= left or bottom <= top:
        raise ValueError("La región seleccionada no tiene dimensiones válidas.")

    with mss.MSS() as sct:
        screenshot = sct.grab(
            {
                "left": left,
                "top": top,
                "width": right - left,
                "height": bottom - top,
            }
        )
        image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

    if image.width < 1 or image.height < 1:
        raise ValueError("La región seleccionada está vacía.")
    return image


def capture_full_screen() -> Image.Image:
    with mss.MSS() as sct:
        screenshot = sct.grab(sct.monitors[0])
        return Image.frombytes("RGB", screenshot.size, screenshot.rgb)