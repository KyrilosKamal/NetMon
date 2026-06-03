import sys
import os
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QIcon, QGuiApplication
from PySide6.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme
from netmon.ui.main_window import MainWindow


def main():
    # ضبط معلومات التطبيق قبل إنشاء الواجهة
    QCoreApplication.setApplicationName("netmon-gui")
    QCoreApplication.setOrganizationName("NetMon")
    QCoreApplication.setApplicationVersion("0.2.2")
    
    app = QApplication(sys.argv)
    
    # ⭐ مهم: ضبظ الـ Dark Mode على مستوى التطبيق
    QGuiApplication.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    
    # ربط التطبيق بالـ Desktop File (مهم جداً لـ Wayland/GNOME)
    app.setDesktopFileName("netmon-gui")
    
    # ⭐ تحميل الأيقونة على مستوى التطبيق (الحل النهائي)
    icon_paths = [
        "/usr/share/icons/hicolor/256x256/apps/netmon-gui.png",
        os.path.join(os.path.dirname(__file__), "ui", "assets", "netmon-gui-256.png"),
    ]
    
    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
            print(f"✓ Application icon set from: {icon_path}")
            break
    
    # ⭐ مهم: ضبظ Fluent Widgets على Dark Theme
    setTheme(Theme.DARK)
    
    # إنشاء وعرض النافذة الرئيسية
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()