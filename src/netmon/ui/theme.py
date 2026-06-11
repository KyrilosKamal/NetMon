"""
Centralized theme management for NetMon.
Handles dark/light modes, accent colors, and global QSS.
Enhanced with glassmorphism effects for better visual integration.
"""
from PySide6.QtGui import QColor
from qfluentwidgets import setTheme, Theme, setThemeColor, FluentStyleSheet
from PySide6.QtCore import QObject
import platform

class ThemeManager(QObject):
    def __init__(self):
        super().__init__()
        self.accent_color = QColor("#00d9ff")  # Default Cyan accent

    def apply_theme(self, is_dark: bool = True):
        theme = Theme.DARK if is_dark else Theme.LIGHT
        setTheme(theme)
        setThemeColor(self.accent_color)

    def get_card_qss(self):
        """Returns custom QSS for cards with enhanced glassmorphism-like effects."""
        # Enhanced glassmorphism effect with multiple layers for depth
        return """
        CardWidget {
            background-color: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            backdrop-filter: blur(10px);
        }
        CardWidget:hover {
            background-color: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(0, 217, 255, 0.4);
            backdrop-filter: blur(15px);
        }
        CardWidget:pressed {
            background-color: rgba(0, 217, 255, 0.1);
        }
        """

    def get_sidebar_qss(self):
        """Returns QSS for sidebar with glassmorphism effect."""
        return """
        QWidget#leftContainer {
            background-color: rgba(255, 255, 255, 0.05);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
        }
        """

    def get_transparent_bg_qss(self):
        """Returns QSS for transparent background elements."""
        return """
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        """

theme_manager = ThemeManager()
