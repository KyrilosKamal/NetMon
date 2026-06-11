from PySide6.QtCore import QObject, Signal, QTimer
from qfluentwidgets import setTheme, Theme, setThemeColor, qconfig
from PySide6.QtGui import QFont
import platform

class ThemeManager(QObject):
    """Centralized theme management with Fluent Design."""
    themeChanged = Signal(Theme)

    def __init__(self):
        super().__init__()
        self._acrylic_enabled = False
        self.setup_fluent_theme()
        # Apply Windows acrylic effect after a short delay to ensure window is ready
        if platform.system() == "Windows":
            QTimer.singleShot(100, self.enable_windows_acrylic_effect)

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

    def enable_windows_acrylic_effect(self):
        """Enable Windows 10/11 acrylic blur effect on application windows."""
        if platform.system() != "Windows":
            return

        try:
            import ctypes
            from ctypes import wintypes

            # Constants for DwmSetWindowAttribute
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19
            DWMWA_BORDER_COLOR = 34
            DWMWA_CAPTION_COLOR = 35
            DWMWA_TEXT_COLOR = 36
            DWMWA_FRAME_RIGHT = 33
            DWMWA_FRAME_BOTTOM = 32
            DWMWA_FRAME_LEFT = 31
            DWMWA_FRAME_TOP = 30
            DWMWA_BACKGROUND_COLOR = 37

            # Constants for acrylic effect
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19

            # Get the active window
            hwnd = ctypes.windll.user32.GetForegroundWindow()

            if hwnd:
                # Enable dark mode for title bar (Windows 10 1809+)
                try:
                    # Try newer constant first
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        wintypes.HWND(hwnd),
                        wintypes.DWORD(DWMWA_USE_IMMERSIVE_DARK_MODE),
                        ctypes.byref(wintypes.BOOL(True)),
                        wintypes.DWORD(ctypes.sizeof(wintypes.BOOL))
                    )
                except:
                    # Fall back to older constant
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        wintypes.HWND(hwnd),
                        wintypes.DWORD(DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1),
                        ctypes.byref(wintypes.BOOL(True)),
                        wintypes.DWORD(ctypes.sizeof(wintypes.BOOL))
                    )

                # Enable acrylic/blur effect (requires Windows 11 22H2+ or Windows 10 1809+ with specific updates)
                # We'll attempt to set the background color to a transparent dark shade
                # which combined with Qt's translucent background can create acrylic-like effect
                try:
                    # Dark semi-transparent background for acrylic effect
                    # ARGB format: 0xAARRGGBB
                    acrylic_color = 0x99000000  # 60% opacity black
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        wintypes.HWND(hwnd),
                        wintypes.DWORD(DWMWA_BACKGROUND_COLOR),
                        ctypes.byref(wintypes.DWORD(acrylic_color)),
                        wintypes.DWORD(ctypes.sizeof(wintypes.DWORD))
                    )
                    self._acrylic_enabled = True
                except:
                    # Acrylic effect not available on this Windows version
                    pass

        except Exception:
            # Silently fail if Windows APIs are not available
            pass

    def is_acrylic_enabled(self):
        """Check if acrylic effect is enabled."""
        return self._acrylic_enabled
