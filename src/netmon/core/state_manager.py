"""
Central state store using Qt signals (pub/sub).
Allows Dashboard and other views to subscribe to live data.
"""
from PySide6.QtCore import QObject, Signal

class NetMonState(QObject):
    bandwidth_updated = Signal(float, float)      # sent, recv (Bps)
    connections_updated = Signal(list)            # list of dicts
    listening_updated = Signal(list)
    speed_test_completed = Signal(dict)           # result dict
    privilege_changed = Signal(bool)              # True if root

    def __init__(self):
        super().__init__()
        self._sent = 0.0
        self._recv = 0.0
        self._connections = []
        self._listening = []
        self._last_speed = {}
        self._is_root = False

    # ---- Properties ----
    @property
    def sent(self): return self._sent
    @property
    def recv(self): return self._recv
    @property
    def connections(self): return self._connections
    @property
    def listening(self): return self._listening
    @property
    def last_speed(self): return self._last_speed
    @property
    def is_root(self): return self._is_root

    # ---- Update methods (called from workers) ----
    def update_bandwidth(self, sent: float, recv: float):
        self._sent = sent
        self._recv = recv
        self.bandwidth_updated.emit(sent, recv)

    def update_connections(self, data: list):
        self._connections = data
        self.connections_updated.emit(data)

    def update_listening(self, data: list):
        self._listening = data
        self.listening_updated.emit(data)

    def update_speed_test(self, result: dict):
        self._last_speed = result
        self.speed_test_completed.emit(result)

    def update_privilege(self, is_root: bool):
        self._is_root = is_root
        self.privilege_changed.emit(is_root)

# Singleton instance used application-wide
state = NetMonState()