from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Qt
from qfluentwidgets import CardWidget, FluentIcon as FIF
from netmon.core.state_manager import state

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        # Create layout with proper margins
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("📊 Network Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # 2x2 Grid for stat cards
        grid = QGridLayout()
        grid.setSpacing(16)
        
        # Create 4 cards
        self.download_card = self.create_stat_card("⬇ Download", "0 B/s", "#00D9FF")
        self.upload_card = self.create_stat_card("⬆ Upload", "0 B/s", "#FF6B6B")
        self.connections_card = self.create_stat_card("🔗 Active Connections", "0", "#4ECDC4")
        self.ports_card = self.create_stat_card(" Listening Ports", "0", "#95E1D3")
        
        grid.addWidget(self.download_card, 0, 0)
        grid.addWidget(self.upload_card, 0, 1)
        grid.addWidget(self.connections_card, 1, 0)
        grid.addWidget(self.ports_card, 1, 1)
        
        layout.addLayout(grid)
        
        # Privilege banner
        self.privilege_label = QLabel("")
        self.privilege_label.setStyleSheet("color: #FFA500; font-size: 12px;")
        layout.addWidget(self.privilege_label)
        
        layout.addStretch()
    
    def create_stat_card(self, title, value, color):
        card = CardWidget()
        card.setMinimumSize(280, 140)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 13px; color: {color}; font-weight: 500;")
        card_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        card_layout.addWidget(value_label)
        
        card.value_label = value_label  # Store reference
        return card
    
    def connect_signals(self):
        # USE EXACT SIGNAL NAMES from state_manager.py
        state.bandwidth_updated.connect(self._on_bandwidth)
        state.connections_updated.connect(self._on_connections)
        state.listening_updated.connect(self._on_listening)
        state.privilege_changed.connect(self._on_privilege)
        state.speed_test_completed.connect(self._on_speed_test)
    
    def _format_bytes(self, bps):
        if bps >= 1_000_000:
            return f"{bps/1_000_000:.2f} MB/s"
        elif bps >= 1_000:
            return f"{bps/1_000:.2f} KB/s"
        return f"{bps:.0f} B/s"
    
    def _on_bandwidth(self, sent: float, recv: float):
        self.upload_card.value_label.setText(self._format_bytes(sent))
        self.download_card.value_label.setText(self._format_bytes(recv))
    
    def _on_connections(self, data: list):
        self.connections_card.value_label.setText(str(len(data)))
    
    def _on_listening(self, data: list):
        self.ports_card.value_label.setText(str(len(data)))
    
    def _on_privilege(self, is_root: bool):
        if is_root:
            self.privilege_label.setText("✓ Running with root privileges - full network visibility")
        else:
            self.privilege_label.setText(" Running as regular user - some connections hidden")
    
    def _on_speed_test(self, result: dict):
        # Update speed test display if we add a card later
        pass
