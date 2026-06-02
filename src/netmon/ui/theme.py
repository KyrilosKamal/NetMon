"""
Centralized theme management for NetMon.
Handles dark/light modes, accent colors, and global QSS.
"""
from PySide6.QtGui import QColor
from qfluentwidgets import setTheme, Theme, setThemeColor, FluentStyleSheet
from PySide6.QtCore import QObject

class ThemeManager(QObject):
    def __init__(self):
        super().__init__()
        self.accent_color = QColor("#00d9ff")  # Default Cyan accent
        
    def apply_theme(self, is_dark: bool = True):
        theme = Theme.DARK if is_dark else Theme.LIGHT
        setTheme(theme)
        setThemeColor(self.accent_color)
        
    def get_card_qss(self):
        """Returns custom QSS for cards with glassmorphism-like effects."""
        return """
        CardWidget {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
        }
        CardWidget:hover {
            background-color: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(0, 217, 255, 0.3);
        }
        """

theme_manager = ThemeManager()
