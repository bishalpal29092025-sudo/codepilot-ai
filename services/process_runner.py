import subprocess
import time
from pathlib import Path

from pydantic import BaseModel


class ProcessResult(BaseModel):
    """
    Result of executing a shell command.
    """

    command: str

    success: bool

    exit_code: int

    stdout: str

    stderr: str

    duration: float


class ProcessRunner:
    """
    Executes shell commands safely and captures results.
    """

    def run(
        self,
        command: str,
        cwd: str | Path | None = None,
        timeout: int = 300,
    ) -> ProcessResult:
        """
        Execute a shell command.

        Args:
            command:
                Shell command to execute.

            cwd:
                Working directory.

            timeout:
                Timeout in seconds.

        Returns:
            ProcessResult
        """

        start = time.perf_counter()

        try:

            completed = subprocess.run(
                command,
                cwd=str(cwd) if cwd else None,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            duration = time.perf_counter() - start

            return ProcessResult(
                command=command,
                success=completed.returncode == 0,
                exit_code=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
                duration=duration,
            )

        except subprocess.TimeoutExpired:

            duration = time.perf_counter() - start

            return ProcessResult(
                command=command,
                success=False,
                exit_code=-1,
                stdout="",
                stderr="Process timed out.",
                duration=duration,
            )

        except Exception as e:

            duration = time.perf_counter() - start

            return ProcessResult(
                command=command,
                success=False,
                exit_code=-1,
                stdout="",
                stderr=str(e),
                duration=duration,
            )