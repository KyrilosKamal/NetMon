from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PySide6.QtCore import Qt
from qfluentwidgets import CardWidget, InfoBadge, InfoBadgePosition
from netmon.core.state_manager import state

class NetworkDetailsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        title = QLabel("🌐 Network Details")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Interface", "IP/Subnet", "Gateway", "MAC", "Status", "Speed", "Default"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
    
    def connect_signals(self):
        state.network_info_updated.connect(self._on_network_info)
    
    def _on_network_info(self, info: dict):
        self.table.setRowCount(len(info))
        for row, (iface, data) in enumerate(info.items()):
            self.table.setItem(row, 0, QTableWidgetItem(iface))
            self.table.setItem(row, 1, QTableWidgetItem(data.get('subnet_cidr', 'N/A')))
            self.table.setItem(row, 2, QTableWidgetItem(data.get('gateway', 'N/A')))
            self.table.setItem(row, 3, QTableWidgetItem(data.get('mac', 'N/A')))
            self.table.setItem(row, 4, QTableWidgetItem("Up" if data.get('is_up') else "Down"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{data.get('speed', 0)} Mbps"))
            self.table.setItem(row, 6, QTableWidgetItem("✓" if data.get('is_default') else ""))
