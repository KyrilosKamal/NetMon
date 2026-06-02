# NetMon 

A modern, pro-grade network monitor for Arch Linux built with **PySide6** and **Fluent Design**. NetMon provides real-time insights into your system's bandwidth, active connections, listening ports, and internet speed.

## Features

-   **Modern Fluent UI:** A high-fidelity interface with dark mode, acrylic effects, and smooth animations using `QFluentWidgets`.
-   **Live Dashboard:** Real-time stats cards and sparkline charts for instant network health checks.
-   **Bandwidth Monitoring:** Detailed area charts showing live upload/download traffic.
-   **Process-Level Connections:** View every active connection with local/remote IPs, PIDs, and associated process names.
-   **Security Audit:** Quickly identify open listening ports and potentially sensitive services.
-   **Speed Test:** Integrated speedtest.net client with circular progress gauges and a persistent history log.
-   **Arch Optimized:** Native PKGBUILD and `.desktop` integration for seamless Arch Linux deployment.

## Technologies

-   **Language:** Python 3.14+
-   **GUI Framework:** [PySide6](https://doc.qt.io/qtforpython-6/) (Official Qt for Python)
-   **UI Design:** [QFluentWidgets](https://github.com/zhiyiYo/PySide6-Fluent-Widgets) (Fluent Design System)
-   **Data Acquisition:** [psutil](https://github.com/giampaolo/psutil) (Cross-platform system/process utilities)
-   **Networking:** [speedtest-cli](https://github.com/sivel/speedtest-cli)
-   **Plotting:** [pyqtgraph](https://github.com/pyqtgraph/pyqtgraph) (High-performance scientific graphics)
-   **Packaging:** Setuptools (PEP 621 `pyproject.toml`)

## Installation (Arch Linux)

### Manual Installation (Development)
```bash
git clone https://github.com/YOUR_USERNAME/netmon.git
cd netmon
python -m venv venv
# For fish users: source venv/bin/activate.fish
source venv/bin/activate
pip install -e .
```

## Usage

Due to security restrictions in Linux, NetMon requires root privileges to resolve process names for network connections owned by other users.

### Standard Run
```bash
netmon
```

### Root Run (Full Visibility)
```bash
# Allow root to access the display
xhost +local:root
# Run with sudo using the absolute path
sudo ./venv/bin/netmon
```

## Project Structure

-   `src/netmon/core/`: Backend logic, workers, and state management.
-   `src/netmon/ui/`: Fluent Design views and custom widgets.
-   `src/netmon/resources/`: Icons and assets.
-   `PKGBUILD`: Arch Linux package build script.

## License

MIT License
