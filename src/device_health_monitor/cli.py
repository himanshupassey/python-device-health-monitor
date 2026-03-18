"""Command-line interface for the Python Device Health Monitor project."""

from __future__ import annotations

import time
from typing import Iterable

from .logger import configure_logger, log_snapshot
from .monitor import ProcessStat, SystemMonitor
from .notifier import AlertThresholds, NotificationManager
from .system_control import SystemController


class DeviceHealthCLI:
    """Menu-driven interface for monitoring system health."""

    def __init__(self) -> None:
        self.monitor = SystemMonitor()
        self.notifier = NotificationManager()
        self.controller = SystemController()
        self.thresholds = AlertThresholds()
        self.logger = configure_logger()

    @staticmethod
    def _print_header(title: str) -> None:
        print("\n" + "=" * 60)
        print(title)
        print("=" * 60)

    @staticmethod
    def _print_processes(processes: Iterable[ProcessStat]) -> None:
        for process in processes:
            print(
                f"PID: {process.pid:<8} Name: {process.name:<25} "
                f"CPU: {process.cpu_percent:>6.2f}% Memory: {process.memory_mb:>8.2f} MB Status: {process.status}"
            )

    def display_system_health(self) -> None:
        """Show the latest system health information."""
        snapshot = self.monitor.get_system_snapshot()
        self._print_header("System Health Summary")
        print(f"CPU Usage: {snapshot.cpu_percent:.2f}%")
        print(
            "RAM Usage: "
            f"{snapshot.memory_used_gb:.2f} GB used / {snapshot.memory_total_gb:.2f} GB total "
            f"({snapshot.memory_available_gb:.2f} GB available, {snapshot.memory_percent:.2f}%)"
        )
        print(
            "Disk Usage: "
            f"{snapshot.disk_used_gb:.2f} GB used / {snapshot.disk_total_gb:.2f} GB total "
            f"({snapshot.disk_free_gb:.2f} GB free, {snapshot.disk_percent:.2f}%)"
        )
        print(f"System Uptime: {snapshot.uptime}")
        print(f"Last Restart Time: {snapshot.last_restart}")
        log_snapshot(self.logger, snapshot)
        self.check_alerts(snapshot.cpu_percent, snapshot.disk_free_gb)

    def display_process_health(self) -> None:
        """Show top CPU and memory consuming applications."""
        self._print_header("Top CPU-Consuming Processes")
        self._print_processes(self.monitor.get_top_processes(sort_by="cpu"))

        self._print_header("Top Memory-Consuming Processes")
        self._print_processes(self.monitor.get_top_processes(sort_by="memory"))

        problematic = self.monitor.get_unresponsive_processes()
        self._print_header("Potentially Problematic Processes")
        if problematic:
            self._print_processes(problematic)
        else:
            print("No stopped, zombie, or dead processes were detected.")

    def check_alerts(self, cpu_percent: float, disk_free_gb: float) -> None:
        """Notify the user when a threshold is exceeded."""
        if cpu_percent >= self.thresholds.cpu_percent:
            self.notifier.send_notification(
                "High CPU Usage",
                f"CPU usage is at {cpu_percent:.2f}%. Consider closing heavy applications.",
            )
        if disk_free_gb <= self.thresholds.disk_free_gb:
            self.notifier.send_notification(
                "Low Disk Space",
                f"Only {disk_free_gb:.2f} GB of free disk space remains.",
            )

    def send_update_reminder(self) -> None:
        """Send a manual reminder notification for updates or maintenance."""
        self.notifier.send_notification(
            "System Reminder",
            "Check for operating system updates and install security patches.",
        )
        print("A system update reminder notification has been sent.")

    def auto_monitor(self) -> None:
        """Run recurring system checks at a user-defined interval."""
        try:
            interval = int(input("Enter the check interval in seconds: ").strip())
            cycles = int(input("Enter number of checks to run (e.g. 5): ").strip())
        except ValueError:
            print("Please enter valid whole numbers.")
            return

        for cycle in range(1, cycles + 1):
            self._print_header(f"Auto Health Check {cycle}/{cycles}")
            self.display_system_health()
            if cycle < cycles:
                time.sleep(interval)

    def run(self) -> None:
        """Display the main menu until the user exits."""
        menu = {
            "1": ("View system health summary", self.display_system_health),
            "2": ("View process monitoring details", self.display_process_health),
            "3": ("Restart the system safely", self.controller.confirm_and_restart),
            "4": ("Send update reminder notification", self.send_update_reminder),
            "5": ("Run automatic health checks", self.auto_monitor),
            "0": ("Exit", None),
        }

        while True:
            self._print_header("Python Device Health Monitor")
            for key, (label, _) in menu.items():
                print(f"{key}. {label}")

            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye!")
                break

            action = menu.get(choice)
            if not action:
                print("Invalid option. Please try again.")
                continue

            _, handler = action
            if handler:
                handler()
            input("\nPress Enter to return to the menu...")


def main() -> None:
    """Application entry point."""
    DeviceHealthCLI().run()


if __name__ == "__main__":
    main()
