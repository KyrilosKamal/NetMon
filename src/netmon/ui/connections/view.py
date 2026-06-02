from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import CardWidget
from netmon.core.state_manager import state

class ConnectionsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🌐 Network Connections")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # Stats row
        stats_layout = QHBoxLayout()
        self.connections_count_label = QLabel("Active Connections: 0")
        self.connections_count_label.setStyleSheet("font-size: 14px; color: #4ECDC4;")
        stats_layout.addWidget(self.connections_count_label)
        
        self.ports_count_label = QLabel("Listening Ports: 0")
        self.ports_count_label.setStyleSheet("font-size: 14px; color: #95E1D3;")
        stats_layout.addWidget(self.ports_count_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Local", "Remote", "Status", "PID", "Process"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background: #1a1a1a;
                color: white;
                border: 1px solid #333333;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background: #2a2a2a;
                color: white;
                padding: 8px;
                border: 1px solid #333333;
            }
        """)
        layout.addWidget(self.table)
    
    def connect_signals(self):
        state.connections_updated.connect(self._on_connections)
        state.listening_updated.connect(self._on_listening)
    
    def _on_connections(self, data: list):
        """Update connections table."""
        self.connections_count_label.setText(f"Active Connections: {len(data)}")
        
        self.table.setRowCount(len(data))
        for i, conn in enumerate(data):
            # USE CORRECT KEYS: local, remote, status, pid, process
            self.table.setItem(i, 0, QTableWidgetItem(str(conn.get('local', ''))))
            self.table.setItem(i, 1, QTableWidgetItem(str(conn.get('remote', ''))))
            self.table.setItem(i, 2, QTableWidgetItem(str(conn.get('status', ''))))
            self.table.setItem(i, 3, QTableWidgetItem(str(conn.get('pid', 0))))
            self.table.setItem(i, 4, QTableWidgetItem(str(conn.get('process', ''))))
    
    def _on_listening(self, data: list):
        """Update listening ports count."""
        self.ports_count_label.setText(f"Listening Ports: {len(data)}")
