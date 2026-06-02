from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import CardWidget
import pyqtgraph as pg
from netmon.core.state_manager import state

class BandwidthView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_chart()
        self.connect_signals()
        
        # Data buffers for chart
        self.max_points = 60
        self.sent_data = []
        self.recv_data = []
        self.time_data = []
        self.counter = 0
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("📈 Live Bandwidth Monitor")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # Chart
        self.chart_widget = pg.PlotWidget()
        self.chart_widget.setBackground('#1a1a1a')
        self.chart_widget.showGrid(x=True, y=True, alpha=0.3)
        self.chart_widget.setMinimumHeight(400)
        layout.addWidget(self.chart_widget)
        
        # Stats row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        self.upload_label = QLabel("⬆ Upload: 0 B/s")
        self.upload_label.setStyleSheet("font-size: 16px; color: #FF6B6B; font-weight: bold;")
        stats_layout.addWidget(self.upload_label)
        
        self.download_label = QLabel("⬇ Download: 0 B/s")
        self.download_label.setStyleSheet("font-size: 16px; color: #00D9FF; font-weight: bold;")
        stats_layout.addWidget(self.download_label)
        
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
    
    def setup_chart(self):
        """Configure pyqtgraph chart."""
        self.chart_widget.setLabel('left', 'Bytes/s', color='#FFFFFF', size='12pt')
        self.chart_widget.setLabel('bottom', 'Time (s)', color='#FFFFFF', size='12pt')
        self.chart_widget.setTitle('Real-time Bandwidth', color='#FFFFFF', size='14pt')
        
        # Create plot lines
        self.sent_curve = self.chart_widget.plot(
            pen=pg.mkPen(color='#FF6B6B', width=2),
            name='Upload'
        )
        self.recv_curve = self.chart_widget.plot(
            pen=pg.mkPen(color='#00D9FF', width=2),
            name='Download'
        )
        
        # Add legend
        self.chart_widget.addLegend()
    
    def connect_signals(self):
        state.bandwidth_updated.connect(self._on_bandwidth)
    
    def _format_bytes(self, bps):
        if bps >= 1_000_000:
            return f"{bps/1_000_000:.2f} MB/s"
        elif bps >= 1_000:
            return f"{bps/1_000:.2f} KB/s"
        return f"{bps:.0f} B/s"
    
    def _on_bandwidth(self, sent: float, recv: float):
        """Update labels and chart."""
        # Update labels
        self.upload_label.setText(f"⬆ Upload: {self._format_bytes(sent)}")
        self.download_label.setText(f"⬇ Download: {self._format_bytes(recv)}")
        
        # Update chart data
        self.time_data.append(self.counter)
        self.sent_data.append(sent)
        self.recv_data.append(recv)
        self.counter += 1
        
        # Keep only last N points
        if len(self.time_data) > self.max_points:
            self.time_data.pop(0)
            self.sent_data.pop(0)
            self.recv_data.pop(0)
        
        # Update curves
        self.sent_curve.setData(self.time_data, self.sent_data)
        self.recv_curve.setData(self.time_data, self.recv_data)
