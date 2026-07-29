"""
Process Manager.

Handles lifecycle management of running processes
inside the Execution Engine.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class ProcessManager:
    """
    Manages application processes.
    """

    def __init__(self) -> None:

        self.process: subprocess.Popen | None = None


    # ==========================================================
    # Public API
    # ==========================================================

    def start(
        self,
        command: str,
        cwd: str | Path | None = None,
    ) -> subprocess.Popen:
        """
        Start a process.
        """

        self.process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        return self.process


    def stop(self) -> None:
        """
        Stop running process.
        """

        if self.process:

            self.process.terminate()

            self.process = None


    def is_running(self) -> bool:
        """
        Check process state.
        """

        if self.process is None:
            return False

        return (
            self.process.poll()
            is None
        )


    def output(self) -> tuple[str, str]:
        """
        Read process output.
        """

        if self.process is None:
            return "", ""

        stdout, stderr = (
            self.process.communicate()
        )

        return stdout, stderr