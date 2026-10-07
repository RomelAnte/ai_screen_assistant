import unittest

from PySide6.QtCore import QPoint, QRect

from response_parser import parse_response
from screen_capture import primary_screen_region
from ui.response_window import build_message_text
from ui.selection_window import (
    SelectionWindow,
    screen_is_valid,
    screen_point_to_physical,
    selection_rect_from_points,
)


class ScreenCaptureTests(unittest.TestCase):
    def test_primary_screen_region_uses_only_primary_monitor(self):
        primary_geometry = QRect(100, 200, 1280, 720)
        self.assertEqual(
            primary_screen_region(primary_geometry),
            (100, 200, 1380, 920),
        )


class OcrOutputTests(unittest.TestCase):
    def test_normalizes_tesseract_output(self):
        from ocr import _normalize_ocr_data

        data = {
            "text": ["hola", "", "mundo"],
            "conf": [95, -1, 80],
        }
        words, confidences = _normalize_ocr_data(data)
        self.assertEqual(words, ["hola", "mundo"])
        self.assertEqual(confidences, [95.0, 80.0])


class ResponseParserTests(unittest.TestCase):
    def test_parses_all_sections(self):
        raw = """RESPUESTA:
La opción B.

EXPLICACIÓN:
Porque la opción B cumple el requisito.

CÓDIGO:
print('ok')
"""
        parsed = parse_response(raw)
        self.assertEqual(parsed["answer"], "La opción B.")
        self.assertEqual(parsed["explanation"], "Porque la opción B cumple el requisito.")
        self.assertEqual(parsed["code"], "print('ok')")

    def test_uses_no_applicable_for_missing_code(self):
        raw = """RESPUESTA:
La respuesta correcta.

EXPLICACIÓN:
Explicación breve.

CÓDIGO:
No aplica
"""
        parsed = parse_response(raw)
        self.assertEqual(parsed["code"], "No aplica")


class SelectionWindowTests(unittest.TestCase):
    def test_has_labels_for_selection_behavior(self):
        self.assertTrue(hasattr(SelectionWindow, "mousePressEvent"))
        self.assertTrue(hasattr(SelectionWindow, "mouseMoveEvent"))
        self.assertTrue(hasattr(SelectionWindow, "mouseReleaseEvent"))
        self.assertTrue(hasattr(SelectionWindow, "keyPressEvent"))

    def test_screen_is_valid_accepts_real_qscreen(self):
        self.assertTrue(screen_is_valid(QRect(0, 0, 1920, 1080)))

    def test_selection_rect_accepts_fractional_mouse_positions(self):
        rect = selection_rect_from_points(
            QPoint(10, 20),
            QPoint(120, 240),
        )
        self.assertEqual(rect, QRect(10, 20, 110, 220))

    def test_screen_point_to_physical_uses_available_geometry(self):
        point = screen_point_to_physical(
            (100, 200),
            QRect(0, 0, 1920, 1080),
            QRect(0, 0, 1920, 1080),
        )
        self.assertEqual(point, (100, 200))

    def test_message_text_contains_only_the_answer(self):
        self.assertEqual(
            build_message_text("La respuesta correcta", "Explicación", "print('ok')"),
            "La respuesta correcta",
        )


if __name__ == "__main__":
    unittest.main()
