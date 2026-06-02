#!/usr/bin/env python3
"""Entry point for the NetMon GUI application."""
import sys
from PySide6.QtWidgets import QApplication
from netmon.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("NetMon")
    app.setApplicationVersion("2.0.0")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()