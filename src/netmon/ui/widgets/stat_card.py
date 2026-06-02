"""
Modern Stat Card with icon and animations.
"""
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import CardWidget, IconWidget, FluentIcon as FIF, StrongBodyLabel, CaptionLabel, BodyLabel

class StatCard(CardWidget):
    def __init__(self, title: str, icon: FIF, unit: str = "", parent=None):
        super().__init__(parent)
        self.setFixedSize(280, 140)
        
        # Layout
        self.main_layout = QVBoxLayout(self)
        self.header_layout = QHBoxLayout()
        
        # Icon
        self.icon_widget = IconWidget(icon, self)
        self.icon_widget.setFixedSize(32, 32)
        
        # Title
        self.title_label = CaptionLabel(title, self)
        self.title_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")
        
        self.header_layout.addWidget(self.icon_widget)
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        
        # Value and Unit
        self.value_layout = QHBoxLayout()
        self.value_label = StrongBodyLabel("--", self)
        self.value_label.setStyleSheet("font-size: 28px; color: #00d9ff;")
        
        self.unit_label = BodyLabel(unit, self)
        self.unit_label.setStyleSheet("margin-top: 8px; color: rgba(255, 255, 255, 0.5);")
        
        self.value_layout.addWidget(self.value_label)
        self.value_layout.addWidget(self.unit_label)
        self.value_layout.addStretch()
        
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.value_layout)
        
        # Hover effect styling
        self.setCursor(Qt.PointingHandCursor)

    def set_value(self, value: str):
        self.value_label.setText(value)
