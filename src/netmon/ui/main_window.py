"""
Main Fluent Window with sidebar navigation.
"""
from PySide6.QtCore import Qt
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon as FIF

from netmon.ui.theme import theme_manager
from netmon.ui.dashboard.view import DashboardView
from netmon.ui.speedtest.view import SpeedTestView
from netmon.ui.bandwidth.view import BandwidthView
from netmon.ui.connections.view import ConnectionsView
from netmon.ui.widgets.privilege_banner import PrivilegeBanner
from netmon.core.workers import BandwidthWorker, ConnectionsWorker, SpeedTestWorker

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetMon")
        self.resize(1280, 800)
        
        # Apply global theme
        theme_manager.apply_theme(is_dark=True)

        # Create view instances
        self.dashboard_view = DashboardView(self)
        self.speed_view = SpeedTestView(self)
        self.bandwidth_view = BandwidthView(self)
        self.connections_view = ConnectionsView(self)

        # Add sub-interfaces
        self.addSubInterface(self.dashboard_view, FIF.HOME, "Dashboard")
        self.addSubInterface(self.speed_view, FIF.SPEED_HIGH, "Speed Test")
        self.addSubInterface(self.bandwidth_view, FIF.MEDIA, "Bandwidth")
        self.addSubInterface(self.connections_view, FIF.GLOBE, "Connections")

        # Background workers
        self.bw_worker = BandwidthWorker()
        self.conn_worker = ConnectionsWorker()
        self.speed_worker = SpeedTestWorker()

        # Connect signals
        self.speed_view.start_test_requested.connect(self.speed_worker.start)
        self.speed_worker.progress.connect(self.speed_view.set_progress_message)
        self.speed_worker.finished.connect(self.speed_view.on_speed_test_finished)

        self.bw_worker.start()
        self.conn_worker.start()

    def closeEvent(self, event):
        self.bw_worker.stop()
        self.conn_worker.stop()
        self.speed_worker.cancel()
        super().closeEvent(event)