"""
Non-intrusive privilege warning banner.
"""
from qfluentwidgets import InfoBar, InfoBarPosition
from netmon.core.backend import is_root

class PrivilegeBanner:
    @staticmethod
    def show_if_needed(parent):
        if not is_root():
            InfoBar.warning(
                title="Limited visibility",
                content="Run as root to see all connections. Use 'sudo netmon'.",
                duration=-1,  # persistent
                position=InfoBarPosition.TOP,
                parent=parent
            )