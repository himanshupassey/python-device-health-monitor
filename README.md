# python-device-health-monitor
System automation tool to monitor CPU, RAM, disk usage and perform system operations with notifications.

diff --git a/README.md b/README.md
index e20324c3ea0e34425384b09a4ba38d44b1a188c4..997699b758c6fc9041bda7001139a46851afd3b0 100644
--- a/README.md
+++ b/README.md
@@ -1,2 +1,106 @@
-# python-device-health-monitor
-System automation tool to monitor CPU, RAM, disk usage and perform system operations with notifications.
+# Python Device Health Monitor
+
+Python Device Health Monitor is a beginner-friendly but portfolio-ready system automation project. It monitors core system resources, highlights heavy processes, sends desktop alerts, logs system stats, and offers a safe restart workflow through a simple menu-driven CLI.
+
+## Features
+
+- **System monitoring**
+  - CPU usage percentage
+  - RAM statistics: total, used, available, and usage percent
+  - Disk statistics: total, used, free, and usage percent
+  - System uptime and last restart time
+- **System control**
+  - Safe restart workflow with user confirmation
+  - Cross-platform restart command selection for Windows, Linux, and macOS
+- **Application monitoring**
+  - Lists top CPU-consuming processes
+  - Lists top memory-consuming processes
+  - Flags processes in stopped, dead, or zombie states when detectable
+- **Notifications**
+  - Desktop alerts for high CPU usage
+  - Desktop alerts for low disk space
+  - Manual reminder for system updates and maintenance
+- **Bonus features**
+  - Logs system snapshots to `device_health.log`
+  - Automatic health checks every X seconds
+  - Configurable alert thresholds in code
+
+## Project Structure
+
+```text
+python-device-health-monitor/
+├── main.py
+├── requirements.txt
+├── README.md
+└── src/
+    └── device_health_monitor/
+        ├── __init__.py
+        ├── cli.py
+        ├── logger.py
+        ├── monitor.py
+        ├── notifier.py
+        └── system_control.py
+```
+
+## Requirements
+
+- Python 3.10+
+- `psutil`
+- `plyer`
+
+Install dependencies:
+
+```bash
+pip install -r requirements.txt
+```
+
+## How to Run
+
+Start the application from the project root:
+
+```bash
+python main.py
+```
+
+## Menu Options
+
+1. View system health summary
+2. View process monitoring details
+3. Restart the system safely
+4. Send update reminder notification
+5. Run automatic health checks
+0. Exit
+
+## Example Output
+
+### System Health Summary
+
+```text
+============================================================
+System Health Summary
+============================================================
+CPU Usage: 14.20%
+RAM Usage: 7.42 GB used / 15.85 GB total (8.10 GB available, 46.80%)
+Disk Usage: 125.70 GB used / 256.00 GB total (130.30 GB free, 49.10%)
+System Uptime: 2d 4h 18m 02s
+Last Restart Time: 2026-03-16 09:05:31
+```
+
+### Top CPU-Consuming Processes
+
+```text
+PID: 1832     Name: python                    CPU:  22.50% Memory:   120.35 MB Status: running
+PID: 900      Name: chrome                    CPU:  12.30% Memory:   452.91 MB Status: sleeping
+```
+
+## Notes
+
+- Desktop notifications rely on the operating system and may behave differently by platform.
+- Restart commands usually require administrator or sudo privileges.
+- Some process details may be hidden if the current user lacks permission.
+
+## Future Improvements
+
+- Add a Tkinter dashboard as a GUI alternative.
+- Export reports in JSON or CSV format.
+- Add configurable thresholds via a settings file.
