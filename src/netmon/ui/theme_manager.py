from PySide6.QtCore import QObject, Signal
from qfluentwidgets import setTheme, Theme, setThemeColor, qconfig
from PySide6.QtGui import QFont

class ThemeManager(QObject):
    """Centralized theme management with Fluent Design."""
    themeChanged = Signal(Theme)
    
    def __init__(self):
        super().__init__()
        self.setup_fluent_theme()
    
    def setup_fluent_theme(self):
        """Configure Fluent Design theme properly."""
        # Enable Fluent effects
        setTheme(Theme.DARK)
        
        # Set accent color (modern cyan/blue)
        setThemeColor("#00D9FF")
        
        # Enable acrylic/glass effects
        qconfig.set(qconfig.themeMode, Theme.DARK)
        
        # Set font
        QFont("Segoe UI", 10)
