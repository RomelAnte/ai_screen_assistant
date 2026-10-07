from typing import Optional

from PySide6.QtCore import Qt, QRect, QEvent, QPoint, Signal, QObject
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QApplication, QWidget


def screen_is_valid(geometry: QRect) -> bool:
    return geometry.width() > 0 and geometry.height() > 0


def selection_rect_from_points(start: QPoint, end: QPoint) -> QRect:
    return QRect(
        start.x(),
        start.y(),
        end.x() - start.x(),
        end.y() - start.y(),
    ).normalized()


def screen_point_to_physical(
    point: tuple[int, int],
    screen_geometry: QRect,
    physical_geometry: QRect,
) -> tuple[int, int]:
    ratio_x = physical_geometry.width() / max(1, screen_geometry.width())
    ratio_y = physical_geometry.height() / max(1, screen_geometry.height())
    x = physical_geometry.x() + int(
        (point[0] - screen_geometry.x()) * ratio_x
    )
    y = physical_geometry.y() + int(
        (point[1] - screen_geometry.y()) * ratio_y
    )
    return max(0, int(x)), max(0, int(y))


class SelectionWindow(QWidget):
    """Superposición de selección de pantalla para cada monitor."""

    selection_ready = Signal(object)
    cancelled = Signal()

    def __init__(self, screen: Optional[object] = None):
        super().__init__()
        self._screen = screen or QApplication.primaryScreen()
        self._selection: Optional[QRect] = None
        self._drag_start: Optional[QPoint] = None
        self._dragging = False

        geometry = self._screen.availableGeometry()
        self.setGeometry(geometry)
        self.setWindowTitle("AI Screen Assistant - selección")
        self.setWindowFlags(
            Qt.Tool
            | Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFocusPolicy(Qt.StrongFocus)
        self.show()
        self.raise_()

    def _physical_point(self, point: tuple[int, int]) -> tuple[int, int]:
        return screen_point_to_physical(
            point,
            self._screen.geometry(),
            self._screen.geometry(),
        )

    def mousePressEvent(self, event: QEvent) -> None:
        if event.button() == Qt.LeftButton and not self._dragging:
            self._dragging = True
            self._drag_start = event.position().toPoint()
            self._selection = QRect(self._drag_start, self._drag_start)
            self.update()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QEvent) -> None:
        if self._dragging and event.buttons() & Qt.LeftButton:
            if self._drag_start is None:
                return
            self._selection = selection_rect_from_points(
                self._drag_start,
                event.position().toPoint(),
            )
            self.update()
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QEvent) -> None:
        if self._dragging and event.button() == Qt.LeftButton:
            self._dragging = False
            self._drag_start = None
            if self._selection is not None:
                self._selection = self._selection.normalized()
                if self._selection.width() < 8 or self._selection.height() < 8:
                    self._selection = None
            if self._selection is not None:
                top_left = self._physical_point((self._selection.left(), self._selection.top()))
                bottom_right = self._physical_point(
                    (self._selection.right(), self._selection.bottom())
                )
                physical_rect = QRect(
                    top_left[0],
                    top_left[1],
                    bottom_right[0] - top_left[0],
                    bottom_right[1] - top_left[1],
                )
                self.selection_ready.emit(physical_rect)
            self.update()
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.cancelled.emit()
            self.close()
            return
        super().keyPressEvent(event)

    def paintEvent(self, event: None) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(8, 18, 32, 30))

        if self._selection is not None:
            selection = self._selection
            painter.fillRect(
                selection,
                QColor(0, 160, 255, 50),
            )
            painter.setPen(QPen(QColor(0, 180, 255), 3))
            painter.drawRect(selection)
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.drawRect(selection.adjusted(1, 1, -1, -1))

        painter.end()


class SelectionWindowManager(QObject):
    selection_ready = Signal(object)
    cancelled = Signal()

    def __init__(self):
        super().__init__()
        self.windows: list[SelectionWindow] = []

    def show(self) -> None:
        self.close_windows()
        for screen in QApplication.screens():
            if not screen_is_valid(screen.geometry()):
                continue
            window = SelectionWindow(screen)
            window.selection_ready.connect(self.handle_selection)
            window.cancelled.connect(self.handle_cancelled)
            window.show()
            self.windows.append(window)

    def handle_selection(self, region: object) -> None:
        self.close_windows()
        self.selection_ready.emit(region)

    def handle_cancelled(self) -> None:
        self.close_windows()
        self.cancelled.emit()

    def close_windows(self) -> None:
        for window in self.windows:
            window.close()
        self.windows.clear()

    def is_visible(self) -> bool:
        return bool(self.windows)
