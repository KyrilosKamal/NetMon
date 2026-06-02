"""
Modern Dashboard with StatCards and MiniCharts.
"""
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from qfluentwidgets import FluentIcon as FIF, TitleLabel, BodyLabel

from netmon.core.state_manager import state
from netmon.ui.widgets.stat_card import StatCard
from netmon.ui.widgets.modern_chart import ModernChart

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboardView")
        self._build_ui()
        
        # Connect to state
        state.bandwidth_updated.connect(self.on_bandwidth)
        state.connections_updated.connect(self.on_connections)
        state.listening_updated.connect(self.on_listening)
        state.speed_test_completed.connect(self.on_speed)

    def _build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(24)
        self.main_layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        self.title = TitleLabel("Network Dashboard", self)
        self.main_layout.addWidget(self.title)
        
        # Stat Cards Row
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(16)
        
        self.dl_card = StatCard("Download", FIF.DOWNLOAD, "Mbps", self)
        self.ul_card = StatCard("Upload", FIF.UP, "Mbps", self)
        self.ping_card = StatCard("Ping", FIF.SEND, "ms", self)
        
        self.stats_layout.addWidget(self.dl_card)
        self.stats_layout.addWidget(self.ul_card)
        self.stats_layout.addWidget(self.ping_card)
        self.stats_layout.addStretch()
        
        self.main_layout.addLayout(self.stats_layout)
        
        # Charts Grid
        self.charts_layout = QGridLayout()
        self.charts_layout.setSpacing(20)
        
        self.sent_chart = ModernChart("Sent Bandwidth", color="#00d9ff", parent=self)
        self.recv_chart = ModernChart("Received Bandwidth", color="#ff00ff", parent=self)
        
        self.charts_layout.addWidget(self.sent_chart, 0, 0)
        self.charts_layout.addWidget(self.recv_chart, 0, 1)
        
        self.main_layout.addLayout(self.charts_layout)
        
        # Summary Row
        self.summary_layout = QHBoxLayout()
        self.conn_label = BodyLabel("Active Connections: 0", self)
        self.listen_label = BodyLabel("Listening Ports: 0", self)
        self.alert_label = BodyLabel("", self)
        self.alert_label.setStyleSheet("color: #ff4d4d; font-weight: bold;")
        
        self.summary_layout.addWidget(self.conn_label)
        self.summary_layout.addSpacing(20)
        self.summary_layout.addWidget(self.listen_label)
        self.summary_layout.addStretch()
        self.summary_layout.addWidget(self.alert_label)
        
        self.main_layout.addLayout(self.summary_layout)

    @Slot(float, float)
    def on_bandwidth(self, sent, recv):
        # We need a small history for the chart
        if not hasattr(self, '_sent_history'):
            self._sent_history = []
            self._recv_history = []
        
        self._sent_history.append(sent)
        self._recv_history.append(recv)
        
        if len(self._sent_history) > 60:
            self._sent_history = self._sent_history[-60:]
            self._recv_history = self._recv_history[-60:]
            
        self.sent_chart.update_data(self._sent_history)
        self.recv_chart.update_data(self._recv_history)

    @Slot(list)
    def on_connections(self, conns):
        self.conn_label.setText(f"Active Connections: {len(conns)}")

    @Slot(list)
    def on_listening(self, ports):
        self.listen_label.setText(f"Listening Ports: {len(ports)}")

    @Slot(dict)
    def on_speed(self, res):
        self.dl_card.set_value(str(res.get('download_mbps', '--')))
        self.ul_card.set_value(str(res.get('upload_mbps', '--')))
        self.ping_card.set_value(str(res.get('ping_ms', '--')))
