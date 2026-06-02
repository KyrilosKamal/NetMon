# from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
# from PySide6.QtCore import Qt
# from qfluentwidgets import CardWidget, InfoBadge, InfoBadgePosition
# from netmon.core.state_manager import state

# class NetworkDetailsView(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setup_ui()
#         self.connect_signals()
    
#     def setup_ui(self):
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(24, 24, 24, 24)
#         layout.setSpacing(20)
        
#         title = QLabel("🌐 Network Details")
#         title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
#         layout.addWidget(title)
        
#         self.table = QTableWidget()
#         self.table.setColumnCount(7)
#         self.table.setHorizontalHeaderLabels([
#             "Interface", "IP/Subnet", "Gateway", "MAC", "Status", "Speed", "Default"
#         ])
#         self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         self.table.setAlternatingRowColors(True)
#         layout.addWidget(self.table)
    
#     def connect_signals(self):
#         state.network_info_updated.connect(self._on_network_info)
    
#     def _on_network_info(self, info: dict):
#         """Update table with network info."""
#         # DEBUG: Print what we received
#         print(f"DEBUG [view]: Received {len(info)} interfaces", flush=True)
#         for iface, data in info.items():
#             print(f"DEBUG [view]: {iface} -> gateway={data.get('gateway')}, default={data.get('is_default')}", flush=True)
            
#         self.table.setRowCount(len(info))
#         for row, (iface, data) in enumerate(info.items()):
#             # Handle None values properly
#             gateway = data.get('gateway') or 'N/A'
#             mac = data.get('mac') or 'N/A'
#             subnet = data.get('subnet_cidr') or 'N/A'
#             speed = data.get('speed', 0)
#             is_up = data.get('is_up', False)
#             is_default = data.get('is_default', False)
            
#             self.table.setItem(row, 0, QTableWidgetItem(iface))
#             self.table.setItem(row, 1, QTableWidgetItem(subnet))
#             self.table.setItem(row, 2, QTableWidgetItem(gateway))
#             self.table.setItem(row, 3, QTableWidgetItem(mac))
#             self.table.setItem(row, 4, QTableWidgetItem("Up" if is_up else "Down"))
#             self.table.setItem(row, 5, QTableWidgetItem(f"{speed} Mbps"))
#             self.table.setItem(row, 6, QTableWidgetItem("✓" if is_default else ""))


from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from netmon.core.state_manager import state

class NetworkDetailsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("DEBUG [NetworkDetailsView]: Creating view", flush=True)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        print("DEBUG [NetworkDetailsView]: Setting up UI", flush=True)
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
        print("DEBUG [NetworkDetailsView]: Connecting signals", flush=True)
        state.network_info_updated.connect(self._on_network_info)
    
    def _on_network_info(self, info: dict):
        """Update table with network info."""
        print(f"DEBUG [NetworkDetailsView]: _on_network_info called with {len(info)} interfaces", flush=True)
        
        # Clear table first
        self.table.setRowCount(0)
        self.table.setRowCount(len(info))
        
        for row, (iface, data) in enumerate(info.items()):
            print(f"DEBUG [NetworkDetailsView]: Processing {iface}", flush=True)
            
            # Handle None values properly
            gateway = data.get('gateway') or 'N/A'
            mac = data.get('mac') or 'N/A'
            subnet = data.get('subnet_cidr') or 'N/A'
            speed = data.get('speed', 0)
            is_up = data.get('is_up', False)
            is_default = data.get('is_default', False)
            
            print(f"DEBUG [NetworkDetailsView]: {iface} -> gateway={gateway}, default={is_default}", flush=True)
            
            self.table.setItem(row, 0, QTableWidgetItem(iface))
            self.table.setItem(row, 1, QTableWidgetItem(subnet))
            self.table.setItem(row, 2, QTableWidgetItem(gateway))
            self.table.setItem(row, 3, QTableWidgetItem(mac))
            self.table.setItem(row, 4, QTableWidgetItem("Up" if is_up else "Down"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{speed} Mbps"))
            self.table.setItem(row, 6, QTableWidgetItem("✓" if is_default else ""))
        
        print(f"DEBUG [NetworkDetailsView]: Table updated with {self.table.rowCount()} rows", flush=True)