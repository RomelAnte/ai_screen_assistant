from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QMessageBox, QWidget


def build_message_text(answer: str, explanation: str, code: str) -> str:
    return answer.strip() or "Sin respuesta"


class ResponseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.message_box = QMessageBox(self)
        self.message_box.setWindowTitle("AI Screen Assistant")
        self.message_box.setIcon(QMessageBox.Information)
        self.message_box.setStandardButtons(QMessageBox.Ok)

    def show_response(self, answer: str, explanation: str, code: str) -> None:
        self.message_box.setText(build_message_text(answer, explanation, code))
        self.message_box.open()
        self.message_box.raise_()
        self.message_box.activateWindow()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()
            return
        super().keyPressEvent(event)