"""
Background QThread workers for periodic data collection.
Emit data through the central state manager.
"""
import logging
import time
import psutil
import speedtest
from PySide6.QtCore import QThread, Signal
from netmon.core.backend import get_bandwidth, get_connections, get_listening_ports, run_speed_test, is_root, get_network_info
from netmon.core.state_manager import state
from netmon.core.quota_manager import quota_manager

# Configure module logger
logger = logging.getLogger(__name__)


class BandwidthWorker(QThread):
    """Fetches bandwidth every second."""
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self._running = False

    def run(self):
        print(f"DEBUG: Starting {self.__class__.__name__}")
        self._running = True
        while self._running:
            try:
                bw = get_bandwidth()
                state.update_bandwidth(bw['sent_Bps'], bw['recv_Bps'])
            except (psutil.Error, OSError) as e:
                logger.error(f"BandwidthWorker failed: {e}")
                self.error_occurred.emit(f"Bandwidth monitoring error: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error in BandwidthWorker: {e}")
                self.error_occurred.emit(f"Unexpected bandwidth error: {e}")
            time.sleep(1)

    def stop(self):
        self._running = False
        self.wait(2000)


class ConnectionsWorker(QThread):
    """Periodically updates connections and listening ports."""
    error_occurred = Signal(str)

    def __init__(self, interval=2):
        super().__init__()
        self.interval = interval
        self._running = False

    def run(self):
        print(f"DEBUG: Starting {self.__class__.__name__}")
        self._running = True
        while self._running:
            try:
                conns = get_connections()
                listen = get_listening_ports()
                state.update_connections(conns)
                state.update_listening(listen)
                state.update_privilege(is_root())
            except (psutil.Error, OSError) as e:
                logger.error(f"ConnectionsWorker failed: {e}")
                self.error_occurred.emit(f"Connections monitoring error: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error in ConnectionsWorker: {e}")
                self.error_occurred.emit(f"Unexpected connections error: {e}")
            time.sleep(self.interval)

    def stop(self):
        self._running = False
        self.wait(2000)


class SpeedTestWorker(QThread):
    """Runs a speed test and reports progress."""
    progress = Signal(str)   # status message
    finished = Signal(dict)  # result dict
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self._is_cancelled = False

    def run(self):
        print(f"DEBUG: Starting {self.__class__.__name__}")
        try:
            self.progress.emit("Finding best server...")
            # Check for cancellation before starting potentially long operation
            if self.isInterruptionRequested() or self._is_cancelled:
                self.finished.emit({'status': 'cancelled'})
                return

            result = run_speed_test()

            # Check again after the operation (in case it was requested during)
            if self.isInterruptionRequested() or self._is_cancelled:
                self.finished.emit({'status': 'cancelled'})
                return

            self.finished.emit(result)
        except speedtest.SpeedtestException as e:
            logger.error(f"SpeedTestWorker failed: {e}")
            self.progress.emit(f"Error: {str(e)}")
            self.error_occurred.emit(f"Speed test error: {e}")
            self.finished.emit({'status': 'error', 'message': str(e)})
        except Exception as e:
            logger.exception(f"Unexpected error in SpeedTestWorker: {e}")
            self.progress.emit(f"Error: {str(e)}")
            self.error_occurred.emit(f"Unexpected speed test error: {e}")
            self.finished.emit({'status': 'error', 'message': str(e)})

    def cancel(self):
        """Request cancellation of the speed test."""
        self._is_cancelled = True
        # Also request thread interruption for immediate response
        self.requestInterruption()


class NetworkInfoWorker(QThread):
    """Polls network interface info every 10 seconds."""
    error_occurred = Signal(str)
    
    def __init__(self, interval=10):
        super().__init__()
        self.interval = interval
        self._running = False
    
    def run(self):
        print(f"DEBUG: Starting {self.__class__.__name__}")
        self._running = True
        while self._running:
            try:
                print("DEBUG: Fetching network info..."); info = get_network_info()
                state.update_network_info(info)
            except Exception as e:
                logger.error(f"NetworkInfoWorker failed: {e}")
                self.error_occurred.emit(str(e))
            time.sleep(self.interval)
    
    def stop(self):
        self._running = False
        self.wait(2000)


class QuotaWorker(QThread):
    """Polls quota usage every 5 seconds."""
    error_occurred = Signal(str)
    
    def __init__(self, interval=5):
        super().__init__()
        self.interval = interval
        self._running = False
        self._last_warning = None
    
    def run(self):
        print(f"DEBUG: Starting {self.__class__.__name__}")
        self._running = True
        while self._running:
            try:
                print("DEBUG: Fetching quota..."); usage = quota_manager.get_usage()
                state.update_quota(usage)
                
                # Emit warning only once per level
                warnings = usage.get('warnings', [])
                if warnings:
                    current_warning = warnings[0]
                    if current_warning != self._last_warning:
                        state.quota_warning.emit(current_warning)
                        self._last_warning = current_warning
                else:
                    self._last_warning = None
            except Exception as e:
                logger.error(f"QuotaWorker failed: {e}")
            time.sleep(self.interval)
    
    def stop(self):
        self._running = False
        self.wait(2000)