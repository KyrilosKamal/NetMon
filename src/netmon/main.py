import sys
from PySide6.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme
from netmon.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    setTheme(Theme.DARK)
    
    window = MainWindow()
    window.show()  # CRITICAL: Must call show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
