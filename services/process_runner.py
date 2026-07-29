import subprocess
import time
from pathlib import Path
from typing import Optional

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
    Executes shell commands and long-running processes.
    """

    # ==========================================================
    # One-shot execution
    # ==========================================================

    def run(
        self,
        command: str,
        cwd: str | Path | None = None,
        timeout: int = 300,
    ) -> ProcessResult:

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

    # ==========================================================
    # Long-running execution
    # ==========================================================

    def start(
        self,
        command: str,
        cwd: str | Path | None = None,
        startup_timeout: int = 5,
    ) -> ProcessResult:
        """
        Starts a long-running application (e.g. pnpm dev, flask run),
        waits for a few seconds, then terminates it.
        """

        start = time.perf_counter()
        process: Optional[subprocess.Popen] = None

        try:

            process = subprocess.Popen(
                command,
                cwd=str(cwd) if cwd else None,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            time.sleep(startup_timeout)

            if process.poll() is None:
                # Process is still running -> considered healthy
                process.terminate()

                try:
                    stdout, stderr = process.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()

                duration = time.perf_counter() - start

                return ProcessResult(
                    command=command,
                    success=True,
                    exit_code=0,
                    stdout=stdout,
                    stderr=stderr,
                    duration=duration,
                )

            stdout, stderr = process.communicate()

            duration = time.perf_counter() - start

            return ProcessResult(
                command=command,
                success=False,
                exit_code=process.returncode,
                stdout=stdout,
                stderr=stderr,
                duration=duration,
            )

        except Exception as e:

            if process and process.poll() is None:
                process.kill()

            duration = time.perf_counter() - start

            return ProcessResult(
                command=command,
                success=False,
                exit_code=-1,
                stdout="",
                stderr=str(e),
                duration=duration,
            )