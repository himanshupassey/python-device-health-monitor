"""System control actions such as restart commands."""

from __future__ import annotations

import platform
import subprocess


class SystemController:
    """Handles safe, confirmed system operations."""

    def get_restart_command(self) -> list[str]:
        """Return the platform-specific restart command."""
        system_name = platform.system().lower()
        if system_name == "windows":
            return ["shutdown", "/r", "/t", "0"]
        if system_name == "darwin":
            return ["sudo", "shutdown", "-r", "now"]
        return ["sudo", "shutdown", "-r", "now"]

    def confirm_and_restart(self) -> bool:
        """Ask the user for confirmation and restart if they approve."""
        confirmation = input("Are you sure you want to restart the system? (y/n): ").strip().lower()
        if confirmation != "y":
            print("Restart cancelled.")
            return False

        command = self.get_restart_command()
        print(f"Running restart command: {' '.join(command)}")
        try:
            subprocess.run(command, check=True)
            return True
        except FileNotFoundError:
            print("Restart command not found on this system.")
        except subprocess.CalledProcessError as error:
            print(f"Restart failed: {error}")
        return False
