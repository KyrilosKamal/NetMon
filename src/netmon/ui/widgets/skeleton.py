"""
Skeleton loader - shimmer placeholder for loading states.
"""
from PySide6.QtCore import Qt, QTimer, Property
from PySide6.QtGui import QLinearGradient, QPainter, QBrush, QColor
from PySide6.QtWidgets import QWidget

class SkeletonLoader(QWidget):
    def __init__(self, width=200, height=20, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self._opacity = 0.4
        self._phase = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(80)

    def _animate(self):
        self._phase += 0.1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Choose colors based on theme (simple approach)
        base = QColor(200, 200, 200)  # light shimmer
        highlight = base.lighter(130)
        grad = QLinearGradient(
            self._phase * 50, 0,
            self._phase * 50 + 80, 0
        )
        grad.setColorAt(0, base)
        grad.setColorAt(0.5, highlight)
        grad.setColorAt(1, base)
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 6, 6)