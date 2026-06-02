"""Settings dialog for quota configuration."""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                                QDoubleSpinBox, QPushButton, QCheckBox)
from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as FIF, InfoBar, InfoBarPosition
from netmon.core.quota_manager import quota_manager

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(500)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # Quota section
        layout.addWidget(QLabel("<b>Data Quota Settings</b>"))
        
        quota_layout = QHBoxLayout()
        quota_layout.addWidget(QLabel("Monthly Quota (GB):"))
        self.quota_spin = QDoubleSpinBox()
        self.quota_spin.setRange(0, 10000)
        self.quota_spin.setDecimals(1)
        self.quota_spin.setValue(quota_manager.monthly_quota_gb)
        quota_layout.addWidget(self.quota_spin)
        layout.addLayout(quota_layout)
        
        # Warning thresholds
        self.warn_80 = QCheckBox("Warning at 80%")
        self.warn_90 = QCheckBox("Warning at 90%")
        self.warn_100 = QCheckBox("Critical at 100%")
        self.warn_80.setChecked(quota_manager.warning_80)
        self.warn_90.setChecked(quota_manager.warning_90)
        self.warn_100.setChecked(quota_manager.warning_100)
        layout.addWidget(self.warn_80)
        layout.addWidget(self.warn_90)
        layout.addWidget(self.warn_100)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("Reset Billing Cycle")
        reset_btn.clicked.connect(self.reset_cycle)
        btn_layout.addWidget(reset_btn)
        
        btn_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def save_settings(self):
        quota_manager.set_quota(self.quota_spin.value())
        quota_manager.warning_80 = self.warn_80.isChecked()
        quota_manager.warning_90 = self.warn_90.isChecked()
        quota_manager.warning_100 = self.warn_100.isChecked()
        quota_manager._save_settings()
        
        InfoBar.success("Settings saved successfully", self.window(), duration=2000)
    
    def reset_cycle(self):
        quota_manager.reset_cycle()
        InfoBar.success("Billing cycle reset", self.window(), duration=2000)
