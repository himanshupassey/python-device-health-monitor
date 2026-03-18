"""Notification helpers for system alerts."""

from __future__ import annotations

from dataclasses import dataclass

from plyer import notification


@dataclass
class AlertThresholds:
    """Alert thresholds used by the application."""

    cpu_percent: float = 80.0
    disk_free_gb: float = 5.0


class NotificationManager:
    """Wrapper around plyer notifications with a safe console fallback."""

    def send_notification(self, title: str, message: str, timeout: int = 5) -> None:
        """Send a desktop notification, or print a fallback message if unavailable."""
        try:
            notification.notify(title=title, message=message, timeout=timeout)
        except Exception:
            print(f"[Notification fallback] {title}: {message}")
