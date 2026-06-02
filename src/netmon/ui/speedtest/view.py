"""
Modern Speed Test View with Circular Progress and Results Cards.
"""
import os
import json
from datetime import datetime
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QTableWidgetItem
from qfluentwidgets import (
    TitleLabel, SubtitleLabel, ProgressRing, PrimaryPushButton, 
    CardWidget, FluentIcon as FIF, TableWidget
)
from netmon.core.state_manager import state

HISTORY_DIR = os.path.expanduser("~/.local/share/netmon")
HISTORY_FILE = os.path.join(HISTORY_DIR, "speed_history.json")

class SpeedTestView(QWidget):
    start_test_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("speedTestView")
        self.history = []
        self._load_history()
        self._build_ui()

    def _build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(32)
        self.main_layout.setContentsMargins(32, 32, 32, 32)

        # Header
        self.main_layout.addWidget(TitleLabel("Speed Test", self))

        # Test Area (Circular Progress + Controls)
        self.test_area = QHBoxLayout()
        
        # Left: Progress Ring
        self.progress_container = QVBoxLayout()
        self.progress_ring = ProgressRing(self)
        self.progress_ring.setFixedSize(200, 200)
        self.progress_ring.setStrokeWidth(12)
        self.progress_ring.setValue(0)
        self.progress_ring.setTextVisible(True)
        
        self.status_label = SubtitleLabel("Ready", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.progress_container.addWidget(self.progress_ring, 0, Qt.AlignCenter)
        self.progress_container.addWidget(self.status_label)
        
        self.test_area.addLayout(self.progress_container)
        
        # Right: Controls and Latest Result
        self.controls_layout = QVBoxLayout()
        self.start_btn = PrimaryPushButton(FIF.PLAY, "Start Speed Test", self)
        self.start_btn.setFixedSize(200, 50)
        self.start_btn.clicked.connect(self.start_test)
        
        self.controls_layout.addWidget(self.start_btn)
        self.controls_layout.addStretch()
        
        self.test_area.addLayout(self.controls_layout)
        self.test_area.addStretch()
        
        self.main_layout.addLayout(self.test_area)

        # History Table
        self.main_layout.addWidget(SubtitleLabel("Test History", self))
        self.history_table = TableWidget(self)
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels([
            "Timestamp", "Download (Mbps)", "Upload (Mbps)", "Ping (ms)", "ISP"
        ])
        self.history_table.verticalHeader().hide()
        self.history_table.setBorderRadius(8)
        self.history_table.setBorderVisible(True)
        
        self.main_layout.addWidget(self.history_table)
        self._update_history_table()

    def start_test(self):
        self.start_btn.setEnabled(False)
        self.progress_ring.setValue(0)
        self.progress_ring.setRange(0, 0)  # Indefinite while initializing
        self.status_label.setText("Initializing...")
        self.start_test_requested.emit()

    @Slot(str)
    def set_progress_message(self, msg):
        self.status_label.setText(msg)

    @Slot(dict)
    def on_speed_test_finished(self, result):
        self.start_btn.setEnabled(True)
        self.progress_ring.setRange(0, 100)
        self.progress_ring.setValue(100)
        
        if result.get('status') == 'error':
            self.status_label.setText(f"Error: {result.get('message')}")
            return

        if result.get('status') == 'cancelled':
            self.status_label.setText("Cancelled")
            return

        self.status_label.setText("Complete")
        state.update_speed_test(result)
        
        # Save to history
        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'download': result['download_mbps'],
            'upload': result['upload_mbps'],
            'ping': result['ping_ms'],
            'isp': result.get('isp', 'Unknown')
        }
        self.history.insert(0, entry)
        self._save_history()
        self._update_history_table()

    def _update_history_table(self):
        self.history_table.setRowCount(len(self.history))
        for i, h in enumerate(self.history):
            self.history_table.setItem(i, 0, QTableWidgetItem(h['timestamp']))
            self.history_table.setItem(i, 1, QTableWidgetItem(str(h['download'])))
            self.history_table.setItem(i, 2, QTableWidgetItem(str(h['upload'])))
            self.history_table.setItem(i, 3, QTableWidgetItem(str(h['ping'])))
            self.history_table.setItem(i, 4, QTableWidgetItem(h['isp']))

    def _load_history(self):
        try:
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE) as f:
                    self.history = json.load(f)
        except Exception:
            self.history = []

    def _save_history(self):
        try:
            os.makedirs(HISTORY_DIR, exist_ok=True)
            with open(HISTORY_FILE, 'w') as f:
                json.dump(self.history[:50], f, indent=2)
        except Exception:
            pass
