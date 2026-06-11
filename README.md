# NetMon - Modern Network Monitor (Cross-Platform)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/UI-PySide6-green.svg" alt="PySide6">
  <img src="https://img.shields.io/badge/Design-Fluent-purple.svg" alt="Fluent Design">
  <img src="https://img.shields.io/badge/Platform-Cross_Platform-lightgrey.svg" alt="Cross Platform">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

<p align="center">
  A modern, fast, and beautiful cross-platform network monitoring application.
  Featuring real-time bandwidth tracking, speed tests, connection monitoring, and data quota management.
</p>

---

## Features

###  Dashboard
- Real-time download/upload speed monitoring
- Active connections counter
- Listening ports counter
- Data quota overview with progress bar
- Root privilege detection

### Speed Test
- One-click speed testing
- Download/Upload speed in Mbps
- Ping measurement
- ISP detection

### Live Bandwidth Monitor
- Real-time area chart visualization
- Sent/Received traffic tracking
- Auto-scaling graphs
- 60-second rolling window
- Color-coded upload/download lines

### Network Connections
- Complete connection table
- Local/Remote addresses
- Connection status (ESTABLISHED, LISTEN, TIME_WAIT, etc.)
- Process name and PID
- Listening ports counter

### Network Details
- All network interfaces overview
- IP address and subnet (CIDR notation)
- Default gateway detection
- MAC address
- Interface status and speed
- Default interface indicator

### Data Quota Tracker
- Monthly quota monitoring
- Usage percentage visualization
- Configurable warning thresholds (80%, 90%, 100%)
- Billing cycle tracking
- Persistent settings via QSettings

### Settings
- Configure monthly data quota
- Warning threshold customization
- Billing cycle reset
- Settings persistence across reboots

---

##  UI Highlights

- **Modern Fluent Design** powered by PySide6-Fluent-Widgets
- **Dark theme** by default with smooth animations
- **Intuitive navigation** with sidebar menu
- **Real-time updates** without UI freezing (QThread workers)
- **Responsive layout** that adapts to window size
- **Signal/Slot architecture** for smooth data flow

### Windows-Specific Visual Enhancements
- **Acrylic/Blur Effect**: Native Windows 10/11 acrylic material effect on Windows 11 22H2+ and Windows 10 with updates
- **Enhanced Glassmorphism**: Improved transparency and blur effects for cards and panels
- **Modern Fluent Integration**: Seamless integration with Windows Fluent Design System
- **Dynamic Theme Adaptation**: Automatic adjustment based on Windows system theme settings
- **Graceful Linux Fallback**: Maintains beautiful appearance on Linux with standard Fluent Design effects

---

## 📦 Installation

### Method 1: From AUR (Arch Linux Only) ⭐

```bash
# Using yay
yay -S netmon-gui

# Using paru
paru -S netmon-gui
```
This will automatically install all dependencies including **python-pyside6-fluent-widgets**.

> **Note:** This method is only available on Arch Linux and Arch-based distributions. Windows users should use Method 2 or 3.

### Method 2: From Source
```bash
# Clone the repository
git clone https://github.com/KyrilosKamal/NetMon.git
cd NetMon

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Run the application (after installation, the command is 'netmon-gui')
netmon-gui
```

### Method 3: With Root Privileges (for full network visibility)
```bash
sudo netmon-gui
```

> **Note:** After installation via any method (AUR, source, or pip), the application is available as the `netmon-gui` command. Running with root privileges (`sudo netmon-gui`) provides complete process name resolution, all network connections visibility, and system-wide bandwidth monitoring.

## Running with root privileges provides
- Complete process name resolution
- All network connections visibility
- System-wide bandwidth monitoring

---
### Usage

## Launch the Application
```bash
# Normal mode
netmon-gui

# With root privileges
sudo netmon-gui
```
---
## Navigation
### Use the left sidebar to switch between tabs:
- Dashboard - Overview of all network stats
- Speed Test - Test your internet speed
- Bandwidth - Live bandwidth monitoring
- Connections - Active network connections
- Network Details - Interface information
- Quota - Data usage tracking
️ - Settings (bottom icon) - Configure quota and warnings

### Setting Up Data Quota
1. Click the Settings icon (️) at the bottom of the sidebar
2. Enter your Monthly Quota (GB)
3. Enable/disable warning thresholds
4. Click Save Settings
5. The quota card will appear on the Dashboard

---
## Architecture
```bash
NetMon/
├── src/netmon/
│   ├── __main__.py              # Application entry point
│   ├── core/
│   │   ├── backend.py           # psutil wrappers & network functions
│   │   ├── workers.py           # QThread background workers
│   │   ├── state_manager.py     # Central pub/sub state (Qt Signals)
│   │   └── quota_manager.py     # Quota tracking with QSettings
│   └── ui/
│       ├── main_window.py       # FluentWindow with navigation
│       ├── dashboard/           # Dashboard view
│       ├── speedtest/           # Speed test view
│       ├── bandwidth/           # Bandwidth chart view
│       ├── connections/         # Connections table view
│       ├── network_details/     # Network info view
│       ├── quota/               # Quota tracker view
│       ├── settings/            # Settings dialog
│       └── widgets/             # Reusable components
── pyproject.toml               # PEP 621 package config
└── README.md
```

### Design Patterns
- MVC Architecture: Strict separation of Model (backend), View (UI), and Controller (workers)
- Pub/Sub Pattern: Central state manager with Qt Signals for decoupled communication
- Thread Safety: All background operations in QThreads, UI updates via signals
- Singleton Pattern: State manager and quota manager as application-wide singletons
---
## Requirements
### System Requirements
- OS: Arch Linux (or Arch-based distro) and Windows 10/11
- Python: 3.11 or higher
- Display: X11 or Wayland
- Privileges: Root (Linux) or Administrator (Windows) for full network visibility (optional)
### Dependencies

| Package | Source | Description |
|----------|----------|-------------|
| python-pyside6 | Official Repo | Qt6 GUI framework |
| python-pyside6-fluent-widgets | AUR | Modern Fluent Design UI |
| python-psutil | Official Repo | System & network monitoring |
| python-speedtest-cli | Official Repo | Internet speed testing |
| python-pyqtgraph | Official Repo | Real-time charting |
| qt6-wayland | Official Repo | Wayland support |
| hicolor-icon-theme | Official Repo | Icon theme |

---
## Development
### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/KyrilosKamal/NetMon.git
cd NetMon
python -m venv venv
source venv/bin/activate
pip install -e .

# Run the application (after installation, the command is 'netmon-gui')
netmon-gui
```
### Code Style
This project follows PEP 8 style guidelines with type hints.

---
### Troubleshooting
If you encounter issues with Claude Code permissions or development tools:

**Permission Fix for PowerShell:**
If you see an error like: `Invalid permission rule "powershell(node *)" was skipped: Tool names must start with uppercase. Use "Powershell"`

Fix this by editing `.claude/settings.local.json` and changing:
```json
"powershell(node *)"
```
to:
```json
"Powershell(node *)"
```
(Note the uppercase "P" in "Powershell")

---
### Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

---
### Bug Reports
If you encounter any issues, please report them at:
https://github.com/KyrilosKamal/NetMon/issues
Include:
- Your OS version (Arch Linux or Windows)
- Python version (python --version)
- Error messages (if any)
- Steps to reproduce

---
### License
This project is licensed under the MIT License - see the LICENSE file for details.

---
### Acknowledgments
- **PySide6** - Qt6 Python bindings
- **PyQt-Fluent-Widgets** - Modern UI components
- **psutil** - System monitoring
- **speedtest-cli** - Speed testing
- **pyqtgraph** - Fast plotting