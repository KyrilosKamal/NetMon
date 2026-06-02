from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from qfluentwidgets import CardWidget, ProgressRing, FluentIcon as FIF
from netmon.core.state_manager import state
from netmon.core.workers import SpeedTestWorker

class SpeedTestView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_worker()
        self.connect_signals()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🚀 Speed Test")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # Progress ring (hidden initially)
        self.progress_ring = ProgressRing()
        self.progress_ring.setFixedSize(120, 120)
        self.progress_ring.setStrokeWidth(8)
        self.progress_ring.setValue(0)
        self.progress_ring.setVisible(False)
        layout.addWidget(self.progress_ring, alignment=Qt.AlignCenter)
        
        # Progress label
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet("font-size: 14px; color: #AAAAAA;")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)
        
        # Start button
        self.start_button = QPushButton("Run Speed Test")
        self.start_button.setFixedSize(200, 50)
        self.start_button.setStyleSheet("""
            QPushButton {
                background: #00D9FF;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #00B8E6;
            }
            QPushButton:disabled {
                background: #555555;
            }
        """)
        self.start_button.clicked.connect(self.start_test)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        
        # Results card
        self.results_card = CardWidget()
        self.results_card.setMinimumHeight(150)
        results_layout = QVBoxLayout(self.results_card)
        results_layout.setContentsMargins(20, 20, 20, 20)
        
        self.results_label = QLabel("Click 'Run Speed Test' to begin...")
        self.results_label.setStyleSheet("font-size: 14px; color: #AAAAAA;")
        results_layout.addWidget(self.results_label)
        
        layout.addWidget(self.results_card)
        layout.addStretch()
    
    def setup_worker(self):
        """Initialize SpeedTestWorker."""
        self.speed_worker = SpeedTestWorker()
        self.speed_worker.progress.connect(self.on_progress)
        self.speed_worker.finished.connect(self.on_finished)
    
    def connect_signals(self):
        """Connect to state_manager for historical results."""
        state.speed_test_completed.connect(self.on_speed_test_completed)
    
    def start_test(self):
        """Start speed test."""
        self.start_button.setEnabled(False)
        self.progress_ring.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_label.setText("Initializing...")
        self.results_label.setText("Testing...")
        
        # Animate progress ring
        self.progress_ring.setValue(30)
        self.speed_worker.start()
    
    def on_progress(self, message: str):
        """Update progress display."""
        self.progress_label.setText(message)
        self.progress_ring.setValue(60)
    
    def on_finished(self, result: dict):
        """Handle test completion."""
        self.progress_ring.setVisible(False)
        self.progress_label.setVisible(False)
        self.start_button.setEnabled(True)
        
        if result.get('status') == 'cancelled':
            self.results_label.setText("Test cancelled")
            return
        
        if result.get('status') == 'error':
            self.results_label.setText(f"Error: {result.get('message', 'Unknown error')}")
            return
        
        # Display results
        dl = result.get('download_mbps', 0)
        ul = result.get('upload_mbps', 0)
        ping = result.get('ping_ms', 0)
        isp = result.get('isp', 'Unknown')
        
        self.results_label.setText(
            f"⬇ Download: {dl:.2f} Mbps\n"
            f"⬆ Upload: {ul:.2f} Mbps\n"
            f"📡 Ping: {ping:.1f} ms\n"
            f"🌐 ISP: {isp}"
        )
        self.results_label.setStyleSheet("font-size: 16px; color: white; line-height: 1.6;")
    
    def on_speed_test_completed(self, result: dict):
        """Handle state_manager signal (for historical data)."""
        # Already handled by worker signal
        pass
