import sys
from typing import Optional

import keyboard
from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QApplication

from config import HOTKEY
from ollama_client import ask_ollama
from response_parser import parse_response
from screen_capture import capture_region, primary_screen_region
from ui.response_window import ResponseWindow
from ui.selection_window import SelectionWindowManager


class AssistantWorker(QObject):
    finished = Signal(str, str, str)
    error = Signal(str)

    def __init__(self, region: Optional[tuple[int, int, int, int]] = None):
        super().__init__()
        self.region = region

    def process(self) -> None:
        try:
            print("\n[1/3] Capturando ventana principal...")
            if self.region is None:
                from PySide6.QtWidgets import QApplication

                screen = QApplication.primaryScreen()
                if screen is None:
                    raise RuntimeError("No se encontró una pantalla principal.")
                self.region = primary_screen_region(screen.geometry())
            image = capture_region(self.region)

            print("[2/3] Consultando Ollama con la imagen...")
            raw_response = ask_ollama(image)

            print("[3/3] Mostrando respuesta...")
            parsed = parse_response(raw_response)
            self.finished.emit(
                parsed["answer"],
                parsed["explanation"],
                parsed["code"],
            )
        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.error.emit(str(exc))


class AssistantController(QObject):
    request_region = Signal(object)
    request_selector = Signal()
    quit_requested = Signal()

    def __init__(self, response_window: ResponseWindow):
        super().__init__()
        self.response_window = response_window
        self.thread: QThread | None = None
        self.worker: AssistantWorker | None = None
        self.request_region.connect(self.start_processing)

    def start_processing(self, region: Optional[tuple[int, int, int, int]] = None) -> None:
        if self.thread is not None and self.thread.isRunning():
            return
        self.worker = AssistantWorker(region)
        self.thread = QThread(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.process)
        self.worker.finished.connect(self.show_result)
        self.worker.error.connect(self.show_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.thread.finished.connect(self._cleanup_thread)
        self.thread.start()

    def show_result(self, answer: str, explanation: str, code: str) -> None:
        self.response_window.show_response(answer, explanation, code)

    def show_error(self, message: str) -> None:
        self.response_window.show_response(
            "ERROR",
            f"No se pudo procesar la región seleccionada.\n\n{message}",
            "",
        )

    def _cleanup_thread(self) -> None:
        self.worker = None
        self.thread = None


def main() -> int:
    app = QApplication(sys.argv)
    response_window = ResponseWindow()
    controller = AssistantController(response_window)
    controller.quit_requested.connect(app.quit)
    selector = SelectionWindowManager()
    controller.request_selector.connect(selector.show)
    selector.selection_ready.connect(controller.request_region.emit)
    selector.cancelled.connect(lambda: print("Selección cancelada."))

    def hotkey_pressed() -> None:
        print("F8 detectado: capturando solo la ventana principal.")
        controller.request_region.emit(None)

    def quit_requested_callback() -> None:
        print("Ctrl+C detectado. Cerrando aplicación.")
        controller.quit_requested.emit()

    keyboard.add_hotkey(HOTKEY, hotkey_pressed)
    keyboard.add_hotkey("ctrl+c", quit_requested_callback)

    print("--------------------------------")
    print(" AI SCREEN ASSISTANT")
    print("--------------------------------")
    print(f"Hotkey: {HOTKEY.upper()}")
    print("Pulsa ESC para cancelar la selección.")
    print("CTRL+C para salir.")
    print()

    try:
        exit_code = app.exec()
        return exit_code
    finally:
        selector.close_windows()
        keyboard.unhook_all()


if __name__ == "__main__":
    raise SystemExit(main())