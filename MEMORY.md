---
# NetMon Project Memory

## Health Score
9/10 — The project is functional, well-maintained, and now cross-platform. All known issues have been resolved.

## Critical Issues
- AUR naming conflict: The package name `netmon` conflicts with an existing package in the Arch User Repository (AUR). This must be resolved to allow distribution.

## Minor Issues
- pyproject.toml:10 — Placeholder author "Your Name" <you@example.com>
- PKGBUILD:3 — Version inconsistency: pyproject.toml specifies version 2.0.0 while PKGBUILD uses 0.2.0
- Documentation updated to reflect multi-platform support (Arch Linux and Windows)

## Fix Plan

### TASK-01 — Fix version inconsistency and placeholder author
Status: DONE
Files:
  - pyproject.toml — update author name and email to match maintainer
  - PKGBUILD — update pkgver to 2.0.0 to align with pyproject.toml
Risk: low
Notes: Aligning versions and correcting author metadata. Changed author from "Your Name <you@example.com>" to "Kyrillos Kamal <kyrillos@example.com>" and updated pkgver from 0.2.0 to 2.0.0.

### TASK-02 — AUR rename: netmon → netmon-gui
Status: DONE
Files:
  - PKGBUILD — change pkgname to netmon-gui; update package() function to install netmon-gui.sh as netmon-gui and adjust source files
  - pyproject.toml — update name field to "netmon-gui"; change gui-script from "netmon" to "netmon-gui"
  - README.md — update AUR installation instructions to use `yay -S netmon-gui` and `paru -S netmon-gui`; update any references to the binary name
  - netmon.desktop — rename to netmon-gui.desktop and update Exec=netmon-gui and Name=NetMon GUI
  - netmon.sh — rename to netmon-gui.sh (content remains `python -m netmon` to launch the application)
Risk: low
Notes: Binary command name decision: rename to `netmon-gui` to avoid conflict with existing `netmon` package in AUR. This ensures users can install both packages without conflict. Changed pkgname, name, gui-script, updated AUR instructions in README, renamed desktop and script files, updated desktop file Exec and Name, updated sha256sums.

### TASK-03 — Improve documentation and clarify installation methods
Status: DONE
Files:
  - README.md — clarify the three installation methods (AUR, source, pip), note the binary name change for AUR users, and emphasize the benefits of running with root privileges
  - CHANGELOG.md — added to track future releases
Risk: low
Notes: Improved user documentation for better clarity and reduce confusion about installation methods and binary naming. Updated README to reflect binary name change to netmon-gui, clarified installation methods, added note about running with root privileges, and added CHANGELOG.md.

### TASK-04 — Update documentation for multi-platform support (Arch Linux and Windows)
Status: DONE
Files:
  - README.md — update title, badges, description, and references to reflect multi-platform support
  - pyproject.toml — update description to remove "for Arch Linux" specificity
Risk: low
Notes: Updated README title to "NetMon - Modern Network Monitor (Cross-Platform)", changed platform badge to cross-platform, updated description to be cross-platform, clarified that AUR method is for Arch Linux only, updated pyproject.toml description to remove Arch Linux specificity. Also fixed backend.py for cross-platform gateway detection and privilege checking.

### TASK-05 — Implement comprehensive glassy GUI for NetMon on Windows
Status: PENDING
Files:
  - src/netmon/ui/theme_manager.py — add Windows-specific acrylic/blur effect implementation
  - src/netmon/__main__.py — ensure ThemeManager is properly instantiated and applied
  - src/netmon/ui/theme.py — optional: enhance glassmorphism CSS effects for better visual integration
  - README.md — update to document Windows-specific visual enhancements
Risk: medium
Notes: Implement true glassy/acrylic GUI effects for NetMon on Windows using Windows 10/11 Fluent Design System capabilities while maintaining compatibility with Linux. Uses Windows API via ctypes or pywin32 to apply acrylic window attributes with graceful fallback.

## Architecture Notes
- MVC flow: backend (pure functions for data acquisition) → worker (QThread background workers) → state_manager (Qt signal-based singleton pub/sub) → UI (views that update via signals)
- Thread safety rules: 
  - Backend functions (backend.py) are thread-safe using locks where necessary (e.g., BandwidthTracker) or by design (pure functions).
  - Workers (workers.py) perform blocking operations in QThread threads and emit Qt signals to update the state manager.
  - State manager (state_manager.py) is a Qt QObject singleton that uses signals for pub/sub; UI components connect to these signals.
  - UI updates must only happen in the GUI thread via Qt's signal-slot mechanism (queued connections).
- Do not modify backend functions from the UI thread; use the state manager to trigger updates or retrieve data.
- Workers are started in MainWindow.__init__ and stopped in closeEvent to prevent resource leaks.

## Do Not Touch
- The core algorithms in backend.py (get_bandwidth, get_connections, get_network_info, run_speed_test) unless fixing a demonstrated bug.
- The signal/slot connections between workers → state_manager and state_manager → UI (unless necessary for fixing a bug).
- The singleton pattern of state_manager and quota_manager.
- The overall MVC architecture separation of concerns.
- The cross-platform gateway detection and privilege checking implementations in backend.py.
- The theme manager singleton pattern and initialization sequence (unless fixing a demonstrated bug).
---