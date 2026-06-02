# NetMon

A modern, pro-grade network monitor for Arch Linux built with **PySide6** and **Fluent Design**. NetMon provides real-time insights into your system's bandwidth, active connections, listening ports, and internet speed.

## Features

-   **Modern Fluent UI:** A high-fidelity interface with dark mode, acrylic effects, and smooth animations using `QFluentWidgets`.
-   **Live Dashboard:** Real-time stats cards for instant network health checks, including Data Quota usage.
-   **Bandwidth Monitoring:** Detailed charts showing live upload/download traffic.
-   **Process-Level Connections:** View every active connection with local/remote IPs, PIDs, and associated process names.
-   **Security Audit:** Quickly identify open listening ports and potentially sensitive services.
-   **Speed Test:** Integrated speedtest.net client with circular progress gauges.
-   **Network Details:** Comprehensive view of network interfaces, IP/Subnet info, and default gateway.
-   **Data Quota Tracking:** Monitor monthly data usage with configurable limits and warning thresholds.
-   **Arch Optimized:** Native PKGBUILD and `.desktop` integration for seamless Arch Linux deployment.

## Technologies

-   **Language:** Python 3.12+
-   **GUI Framework:** [PySide6](https://doc.qt.io/qtforpython-6/)
-   **UI Design:** [QFluentWidgets](https://github.com/zhiyiYo/PySide6-Fluent-Widgets)
-   **Data Acquisition:** [psutil](https://github.com/giampaolo/psutil)
-   **Networking:** [speedtest-cli](https://github.com/sivel/speedtest-cli)
-   **Plotting:** [pyqtgraph](https://github.com/pyqtgraph/pyqtgraph)

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/netmon.git
    cd netmon
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install .
    ```

## Usage

Due to security restrictions in Linux, NetMon requires root privileges to resolve process names for network connections owned by other users.

### Run NetMon
After installing in your virtual environment, run:
```bash
python -m netmon
```

### Run with Root Privileges (Full Visibility)
If you need to see processes owned by other users:
```bash
sudo ./.venv/bin/python -m netmon
```
*(Note: Ensure your virtual environment is created before running this command).*

## Project Structure

-   `src/netmon/core/`: Backend logic, workers, state management, and quota tracking.
-   `src/netmon/ui/`: Fluent Design views, custom widgets (QuotaCard), and settings dialog.
-   `src/netmon/resources/`: Icons and assets.
-   `PKGBUILD`: Arch Linux package build script.

## License

MIT License
