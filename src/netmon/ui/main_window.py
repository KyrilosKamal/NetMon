from PySide6.QtCore import Qt
from qfluentwidgets import FluentWindow, FluentIcon as FIF
from netmon.ui.dashboard.view import DashboardView
from netmon.ui.speedtest.view import SpeedTestView
from netmon.ui.bandwidth.view import BandwidthView
from netmon.ui.connections.view import ConnectionsView
from netmon.core.workers import BandwidthWorker, ConnectionsWorker
from netmon.core.state_manager import state

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("NetMon - Network Monitor")
        self.resize(1200, 800)
        
        # Create views
        self.dashboard_view = DashboardView()
        self.dashboard_view.setObjectName("dashboardView")
        self.speedtest_view = SpeedTestView()
        self.speedtest_view.setObjectName("speedTestView")
        self.bandwidth_view = BandwidthView()
        self.bandwidth_view.setObjectName("bandwidthView")
        self.connections_view = ConnectionsView()
        self.connections_view.setObjectName("connectionsView")
        
        # Add sub-interfaces
        self.addSubInterface(self.dashboard_view, FIF.HOME, "Dashboard")
        self.addSubInterface(self.speedtest_view, FIF.SPEED_HIGH, "Speed Test")
        self.addSubInterface(self.bandwidth_view, FIF.PIE_SINGLE, "Bandwidth")
        self.addSubInterface(self.connections_view, FIF.GLOBE, "Connections")
        
        # Start workers (SpeedTestWorker is inside SpeedTestView)
        self.bw_worker = BandwidthWorker()
        self.conn_worker = ConnectionsWorker(interval=2)
        
        self.bw_worker.start()
        self.conn_worker.start()
        
        # Set initial view
        self.switchTo(self.dashboard_view)
    
    def closeEvent(self, event):
        self.bw_worker.stop()
        self.conn_worker.stop()
        self.speedtest_view.speed_worker.cancel()
        super().closeEvent(event)
