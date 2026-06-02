"""Core backend and threading components."""
"""
Pure functions for network data acquisition.
No Qt/GUI dependencies – safe to call from any thread.
"""
import os
import time
import threading
import socket
import struct
from typing import Dict, List, Optional, Any

import psutil
import speedtest


# ------------------------------------------------------------
# Bandwidth tracking with thread-safe state
# ------------------------------------------------------------




class BandwidthTracker:
    """Thread-safe bandwidth calculator using psutil.net_io_counters."""

    def __init__(self):
        self._lock = threading.Lock()
        self._prev_time = time.monotonic()
        self._prev_sent = 0
        self._prev_recv = 0

    def get_bandwidth(self) -> Dict[str, float]:
        """
        Calculate current sent/received bytes per second.
        Returns dict with keys 'sent_Bps' and 'recv_Bps'.
        Thread-safe; safe to call from any thread.
        """
        with self._lock:
            io = psutil.net_io_counters()
            now = time.monotonic()
            elapsed = now - self._prev_time
            if elapsed < 0.001:
                return {'sent_Bps': 0.0, 'recv_Bps': 0.0}
            sent_delta = io.bytes_sent - self._prev_sent
            recv_delta = io.bytes_recv - self._prev_recv
            self._prev_time = now
            self._prev_sent = io.bytes_sent
            self._prev_recv = io.bytes_recv
            return {
                'sent_Bps': round(sent_delta / elapsed, 1),
                'recv_Bps': round(recv_delta / elapsed, 1)
            }


# Singleton instance
_bandwidth_tracker = BandwidthTracker()


def get_bandwidth() -> Dict[str, float]:
    """Public wrapper for the BandwidthTracker singleton."""
    return _bandwidth_tracker.get_bandwidth()


# ------------------------------------------------------------
# Cached network connections to reduce psutil calls
# ------------------------------------------------------------
_connections_cache: Optional[List[Dict]] = None
_connections_cache_time: float = 0.0
_CACHE_INTERVAL: float = 2.0  # seconds, configurable via set_connections_cache_interval


def set_connections_cache_interval(interval: float) -> None:
    """
    Set the minimum interval (in seconds) between psutil.net_connections calls.
    Defaults to 2.0 seconds.
    """
    global _CACHE_INTERVAL
    if interval <= 0:
        raise ValueError("Cache interval must be positive")
    _CACHE_INTERVAL = interval


def get_connections() -> List[Dict]:
    """
    Return all active network connections (IPv4/IPv6 only).
    Each entry: local, remote, status, pid, process.
    Uses caching to avoid excessive psutil.net_connections calls.
    """
    global _connections_cache, _connections_cache_time

    now = time.monotonic()
    if (_connections_cache is not None and
            (now - _connections_cache_time) < _CACHE_INTERVAL):
        return _connections_cache

    try:
        conns = []
        for c in psutil.net_connections(kind='inet'):
            laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ''
            raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else ''
            pid = c.pid or 0
            proc_name = ''
            if pid:
                try:
                    proc = psutil.Process(pid)
                    proc_name = proc.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    proc_name = '?'
            conns.append({
                'local': laddr,
                'remote': raddr,
                'status': c.status,
                'pid': pid,
                'process': proc_name
            })
        _connections_cache = conns
        _connections_cache_time = now
        return conns
    except Exception as e:
        # Return last known good cache on error to prevent UI freezing
        if _connections_cache is not None:
            return _connections_cache
        # If no cache available, return empty list
        return []


def get_listening_ports() -> List[Dict]:
    """
    Return only connections with status == 'LISTEN'.
    Leverages cached connections from get_connections().
    """
    conns = get_connections()
    return [c for c in conns if c['status'] == 'LISTEN']


# ------------------------------------------------------------
# Network info and gateway
# ------------------------------------------------------------


def _parse_gateway() -> str:
    """Parse default gateway from /proc/net/route (hex to IP)."""
    try:
        with open('/proc/net/route', 'r') as f:
            for line in f.readlines()[1:]:  # Skip header
                parts = line.strip().split()
                if len(parts) >= 3 and parts[1] == '00000000':  # Default route
                    gateway_int = int(parts[2], 16)
                    return socket.inet_ntoa(struct.pack('<L', gateway_int))
    except (FileNotFoundError, PermissionError, ValueError):
        pass
    return "Unknown"


def _mask_to_cidr(mask: str) -> int:
    """Convert netmask to CIDR prefix length."""
    return sum(bin(int(x)).count('1') for x in mask.split('.'))


def get_network_info() -> Dict[str, Dict[str, Any]]:
    """Return network info for all interfaces including gateway."""

    gateway = _parse_gateway()
    result = {}

    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for iface, addr_list in addrs.items():
        iface_info = {
            'ip': None,
            'subnet_cidr': None,
            'mac': None,
            'is_up': False,
            'speed': 0,
            'is_default': False
        }

        # Get stats
        if iface in stats:
            iface_info['is_up'] = stats[iface].isup
            iface_info['speed'] = stats[iface].speed

        for addr in addr_list:
            if addr.family == socket.AF_INET:  # IPv4 only
                iface_info['ip'] = addr.address
                cidr = _mask_to_cidr(addr.netmask)
                iface_info['subnet_cidr'] = f"{addr.address}/{cidr}"
            elif addr.family == 17:  # AF_PACKET (MAC address)
                iface_info['mac'] = addr.address

        # Check if this interface has the gateway
        if gateway != "Unknown" and iface_info.get('ip'):
            # Simple check: interface IP in same subnet as gateway
            # For now, mark first interface with IP as default
            if not any(v.get('is_default') for v in result.values()):
                iface_info['is_default'] = True
                iface_info['gateway'] = gateway

        if iface_info['ip']:  # Only add interfaces with IPs
            result[iface] = iface_info

    return result


# ------------------------------------------------------------
# Speed Test
# ------------------------------------------------------------


def run_speed_test() -> Dict:
    """
    Run a full speed test. Returns dict with download/upload/ping/isp.
    Note: This operation is blocking and may take 10-30 seconds.
    For cancellation support, callers should check for interruption
    before invoking this function.
    """
    st = speedtest.Speedtest()
    st.get_best_server()
    dl = st.download()  # bits per second
    ul = st.upload()
    ping = st.results.ping
    return {
        'download_mbps': round(dl / 1e6, 2),
        'upload_mbps': round(ul / 1e6, 2),
        'ping_ms': round(ping, 1),
        'isp': st.results.client.get('isp', 'Unknown')
    }


# ------------------------------------------------------------
# Privilege helpers
# ------------------------------------------------------------


def is_root() -> bool:
    """Return True if the process has effective UID 0."""
    return os.geteuid() == 0