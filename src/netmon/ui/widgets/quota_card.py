"""Reusable Quota Card widget."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from qfluentwidgets import CardWidget

class QuotaCard(CardWidget):
    def __init__(self, compact=False, parent=None):
        super().__init__(parent)
        self.compact = compact
        self.setup_ui()
    
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(12)
        
        self.title_label = QLabel("📊 Data Quota")
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        self.layout.addWidget(self.title_label)
        
        self.usage_label = QLabel("Not configured")
        self.usage_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.layout.addWidget(self.usage_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444;
                border-radius: 6px;
                text-align: center;
                color: white;
                height: 20px;
            }
            QProgressBar::chunk {
                background: #00D9FF;
                border-radius: 5px;
            }
        """)
        self.layout.addWidget(self.progress_bar)
        
        self.detail_label = QLabel("")
        self.detail_label.setStyleSheet("font-size: 12px; color: #AAAAAA;")
        self.layout.addWidget(self.detail_label)
    
    def update_usage(self, data: dict):
        if not data.get('enabled'):
            self.usage_label.setText("Not configured")
            self.progress_bar.setValue(0)
            self.detail_label.setText("Open Settings to configure quota")
            return
        
        pct = data['percentage']
        self.usage_label.setText(f"{data['used_gb']} / {data['monthly_gb']} GB")
        self.progress_bar.setValue(int(pct))
        self.detail_label.setText(
            f"{data['remaining_gb']} GB remaining • Since {data['billing_start']}"
        )
        
        # Color changes based on usage
        if pct >= 100:
            color = "#FF4444"
        elif pct >= 90:
            color = "#FFA500"
        elif pct >= 80:
            color = "#FFD700"
        else:
            color = "#00D9FF"
        
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #444;
                border-radius: 6px;
                text-align: center;
                color: white;
                height: 20px;
            }}
            QProgressBar::chunk {{
                background: {color};
                border-radius: 5px;
            }}
        """)
