"""
Modern Bandwidth View with full-size charts.
"""
from collections import deque
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import TitleLabel, SubtitleLabel

from netmon.core.state_manager import state
from netmon.ui.widgets.modern_chart import ModernChart
from netmon.ui.widgets.stat_card import StatCard
from qfluentwidgets import FluentIcon as FIF

class BandwidthView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("bandwidthView")
        self.sent_history = deque(maxlen=300)
        self.recv_history = deque(maxlen=300)
        self._build_ui()
        state.bandwidth_updated.connect(self.on_bandwidth)

    def _build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(24)
        self.main_layout.setContentsMargins(32, 32, 32, 32)

        # Header
        self.main_layout.addWidget(TitleLabel("Bandwidth Monitor", self))

        # Top Row: Current Stats
        self.stats_layout = QHBoxLayout()
        self.sent_card = StatCard("Current Sent", FIF.UP, "B/s", self)
        self.recv_card = StatCard("Current Received", FIF.DOWNLOAD, "B/s", self)
        self.stats_layout.addWidget(self.sent_card)
        self.stats_layout.addWidget(self.recv_card)
        self.stats_layout.addStretch()
        self.main_layout.addLayout(self.stats_layout)

        # Main Chart Area
        self.chart = ModernChart("Live Traffic", color="#00d9ff", parent=self)
        # Add second curve for received
        self.recv_curve = self.chart.plot(pen={'color': "#ff00ff", 'width': 2})
        # Fill for recv
        fill_color = self.chart.palette().color(self.chart.foregroundRole()) # placeholder
        from PySide6.QtGui import QColor
        self.recv_curve.setFillBrush(QColor(255, 0, 255, 30))
        self.recv_curve.setFillLevel(0)
        
        self.main_layout.addWidget(self.chart)

    @Slot(float, float)
    def on_bandwidth(self, sent, recv):
        self.sent_history.append(sent)
        self.recv_history.append(recv)
        
        self.chart.update_data(list(self.sent_history))
        self.recv_curve.setData(list(self.recv_history))
        
        self.sent_card.set_value(f"{sent:.1f}")
        self.recv_card.set_value(f"{recv:.1f}")
