"""
Modern Connections View with Search and Filter.
"""
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem
from qfluentwidgets import (
    TitleLabel, SearchLineEdit, ComboBox, TableWidget, 
    FluentIcon as FIF, RoundMenu, Action
)
from netmon.core.state_manager import state

class ConnectionsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("connectionsView")
        self.show_listening = False
        self._build_ui()
        state.connections_updated.connect(self.update_data)

    def _build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(32, 32, 32, 32)

        # Header
        self.main_layout.addWidget(TitleLabel("Network Connections", self))

        # Filter Bar
        self.filter_bar = QHBoxLayout()
        self.search_input = SearchLineEdit(self)
        self.search_input.setPlaceholderText("Search process, IP, or status...")
        self.search_input.textChanged.connect(self._on_search)
        
        self.mode_combo = ComboBox(self)
        self.mode_combo.addItems(["All Connections", "Listening Ports"])
        self.mode_combo.currentIndexChanged.connect(self._mode_changed)
        
        self.filter_bar.addWidget(self.search_input, 1)
        self.filter_bar.addWidget(self.mode_combo)
        self.main_layout.addLayout(self.filter_bar)

        # Table
        self.table = TableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Local Address", "Remote Address", "Status", "PID", "Process"
        ])
        self.table.verticalHeader().hide()
        self.table.setBorderRadius(8)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        
        self.main_layout.addWidget(self.table)

    @Slot(int)
    def _mode_changed(self, idx):
        self.show_listening = (idx == 1)
        data = state.listening if self.show_listening else state.connections
        self._populate_table(data)

    def _on_search(self, text):
        # Simple client-side filtering by re-populating or hiding rows
        data = state.listening if self.show_listening else state.connections
        filtered = [
            c for c in data 
            if text.lower() in str(c.values()).lower()
        ]
        self._populate_table(filtered)

    @Slot(list)
    def update_data(self, conns):
        if not self.search_input.text():
            data = state.listening if self.show_listening else conns
            self._populate_table(data)

    def _populate_table(self, data):
        self.table.setRowCount(len(data))
        for i, c in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(c.get('local', '')))
            self.table.setItem(i, 1, QTableWidgetItem(c.get('remote', '')))
            
            # Status badge styling could be added here
            status = c.get('status', '')
            self.table.setItem(i, 2, QTableWidgetItem(status))
            
            self.table.setItem(i, 3, QTableWidgetItem(str(c.get('pid', ''))))
            self.table.setItem(i, 4, QTableWidgetItem(c.get('process', '')))
