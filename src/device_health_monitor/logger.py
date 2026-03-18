"""File logging for system health snapshots."""

from __future__ import annotations

import logging
from pathlib import Path

from .monitor import SystemSnapshot


def configure_logger(log_file: str = "device_health.log") -> logging.Logger:
    """Create or return a logger configured for system snapshots."""
    logger = logging.getLogger("device_health_monitor")
    if logger.handlers:
        return logger

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(log_path)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def log_snapshot(logger: logging.Logger, snapshot: SystemSnapshot) -> None:
    """Write a system snapshot to the log file."""
    logger.info(
        "CPU: %.2f%% | Memory: %.2f/%.2f GB (%.2f%%) | Disk: %.2f/%.2f GB (%.2f%%) | Uptime: %s",
        snapshot.cpu_percent,
        snapshot.memory_used_gb,
        snapshot.memory_total_gb,
        snapshot.memory_percent,
        snapshot.disk_used_gb,
        snapshot.disk_total_gb,
        snapshot.disk_percent,
        snapshot.uptime,
    )
