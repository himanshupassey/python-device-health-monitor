"""Utilities for collecting system and process health information."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

import psutil


@dataclass
class SystemSnapshot:
    """Represents a single snapshot of system health metrics."""

    cpu_percent: float
    memory_total_gb: float
    memory_used_gb: float
    memory_available_gb: float
    memory_percent: float
    disk_total_gb: float
    disk_used_gb: float
    disk_free_gb: float
    disk_percent: float
    uptime: str
    last_restart: str


@dataclass
class ProcessStat:
    """Contains the most relevant process information for display."""

    pid: int
    name: str
    cpu_percent: float
    memory_mb: float
    status: str


class SystemMonitor:
    """Collects health data for the local machine using psutil."""

    def __init__(self, disk_path: str = "/") -> None:
        self.disk_path = disk_path

    @staticmethod
    def _bytes_to_gb(value: float) -> float:
        return round(value / (1024 ** 3), 2)

    @staticmethod
    def _bytes_to_mb(value: float) -> float:
        return round(value / (1024 ** 2), 2)

    @staticmethod
    def _format_timedelta(delta: timedelta) -> str:
        total_seconds = int(delta.total_seconds())
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days}d {hours}h {minutes}m {seconds}s"

    def get_system_snapshot(self) -> SystemSnapshot:
        """Collect CPU, memory, disk, uptime, and restart information."""
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(self.disk_path)
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        now = datetime.now()

        return SystemSnapshot(
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_total_gb=self._bytes_to_gb(memory.total),
            memory_used_gb=self._bytes_to_gb(memory.used),
            memory_available_gb=self._bytes_to_gb(memory.available),
            memory_percent=memory.percent,
            disk_total_gb=self._bytes_to_gb(disk.total),
            disk_used_gb=self._bytes_to_gb(disk.used),
            disk_free_gb=self._bytes_to_gb(disk.free),
            disk_percent=disk.percent,
            uptime=self._format_timedelta(now - boot_time),
            last_restart=boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        )

    def get_top_processes(self, sort_by: str = "cpu", limit: int = 5) -> List[ProcessStat]:
        """Return top running processes sorted by CPU or memory usage."""
        process_stats: List[ProcessStat] = []
        psutil.cpu_percent(interval=None)

        for process in psutil.process_iter(["pid", "name", "memory_info", "status"]):
            try:
                cpu_percent = process.cpu_percent(interval=None)
                memory_info = process.info.get("memory_info")
                memory_mb = self._bytes_to_mb(memory_info.rss) if memory_info else 0.0
                process_stats.append(
                    ProcessStat(
                        pid=process.info["pid"],
                        name=process.info.get("name") or "Unknown",
                        cpu_percent=round(cpu_percent, 2),
                        memory_mb=memory_mb,
                        status=process.info.get("status") or "unknown",
                    )
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        key = (lambda item: item.memory_mb) if sort_by == "memory" else (lambda item: item.cpu_percent)
        return sorted(process_stats, key=key, reverse=True)[:limit]

    def get_unresponsive_processes(self, limit: int = 10) -> List[ProcessStat]:
        """Return processes that are likely problematic based on their status."""
        flagged_statuses = {psutil.STATUS_STOPPED, psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD}
        problematic: List[ProcessStat] = []

        for process in psutil.process_iter(["pid", "name", "status", "memory_info"]):
            try:
                status = process.info.get("status") or "unknown"
                if status in flagged_statuses:
                    memory_info = process.info.get("memory_info")
                    memory_mb = self._bytes_to_mb(memory_info.rss) if memory_info else 0.0
                    problematic.append(
                        ProcessStat(
                            pid=process.info["pid"],
                            name=process.info.get("name") or "Unknown",
                            cpu_percent=0.0,
                            memory_mb=memory_mb,
                            status=status,
                        )
                    )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        return problematic[:limit]
