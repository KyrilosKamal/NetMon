from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import CardWidget
from netmon.ui.widgets.quota_card import QuotaCard
from netmon.core.state_manager import state

class QuotaView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        title = QLabel("📊 Data Quota Tracker")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        self.quota_card = QuotaCard(compact=False)
        layout.addWidget(self.quota_card)
        layout.addStretch()
    
    def connect_signals(self):
        state.quota_updated.connect(self.quota_card.update_usage)
