"""Manages data quota tracking with persistent storage via QSettings."""
from PySide6.QtCore import QSettings, QDate
import psutil

class QuotaManager:
    def __init__(self):
        self.settings = QSettings("NetMon", "NetMon")
        self._load_settings()
    
    def _load_settings(self):
        self.monthly_quota_gb = self.settings.value("quota/monthly_gb", 0.0, type=float)
        self.billing_start = self.settings.value("quota/billing_start", "")
        self.baseline_bytes = self.settings.value("quota/baseline_bytes", 0, type=int)
        self.warning_80 = self.settings.value("quota/warning_80", True, type=bool)
        self.warning_90 = self.settings.value("quota/warning_90", True, type=bool)
        self.warning_100 = self.settings.value("quota/warning_100", True, type=bool)
    
    def set_quota(self, gb: float, billing_start: str = None):
        """Set monthly quota and capture current usage as baseline."""
        self.monthly_quota_gb = gb
        self.billing_start = billing_start or QDate.currentDate().toString("yyyy-MM-dd")
        io = psutil.net_io_counters()
        self.baseline_bytes = io.bytes_sent + io.bytes_recv
        self._save_settings()
    
    def get_usage(self) -> dict:
        """Calculate current quota usage."""
        if self.monthly_quota_gb <= 0:
            return {"enabled": False}
        
        io = psutil.net_io_counters()
        current_total = io.bytes_sent + io.bytes_recv
        used_bytes = max(0, current_total - self.baseline_bytes)
        
        quota_bytes = self.monthly_quota_gb * (1024 ** 3)
        used_gb = used_bytes / (1024 ** 3)
        remaining_gb = max(0, self.monthly_quota_gb - used_gb)
        percentage = (used_bytes / quota_bytes) * 100 if quota_bytes > 0 else 0
        
        return {
            "enabled": True,
            "monthly_gb": self.monthly_quota_gb,
            "used_gb": round(used_gb, 2),
            "remaining_gb": round(remaining_gb, 2),
            "percentage": round(percentage, 1),
            "billing_start": self.billing_start,
            "warnings": self._check_warnings(percentage)
        }
    
    def _check_warnings(self, percentage: float) -> list:
        warnings = []
        if percentage >= 100 and self.warning_100:
            warnings.append("critical")
        elif percentage >= 90 and self.warning_90:
            warnings.append("high")
        elif percentage >= 80 and self.warning_80:
            warnings.append("medium")
        return warnings
    
    def reset_cycle(self):
        """Reset for new billing cycle."""
        self.billing_start = QDate.currentDate().toString("yyyy-MM-dd")
        io = psutil.net_io_counters()
        self.baseline_bytes = io.bytes_sent + io.bytes_recv
        self._save_settings()
    
    def _save_settings(self):
        self.settings.setValue("quota/monthly_gb", self.monthly_quota_gb)
        self.settings.setValue("quota/billing_start", self.billing_start)
        self.settings.setValue("quota/baseline_bytes", self.baseline_bytes)
        self.settings.sync()

quota_manager = QuotaManager()
