"""
Command Runner.

Responsible for executing shell commands
and returning structured execution results.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

from execution.models.command_result import CommandResult


class CommandRunner:
    """
    Executes system commands safely.

    Used by the Execution Engine for:

    - dependency installation
    - build execution
    - test execution
    - application startup
    """

    DEFAULT_TIMEOUT = 300


    # ==========================================================
    # Public API
    # ==========================================================

    def run(
        self,
        command: str,
        cwd: str | Path | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> CommandResult:
        """
        Execute a shell command.

        Args:
            command:
                Command to execute.

            cwd:
                Working directory.

            timeout:
                Maximum execution time.

        Returns:
            CommandResult
        """

        start_time = time.perf_counter()


        try:

            process = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )


            duration = (
                time.perf_counter()
                - start_time
            )


            return CommandResult(
                command=command,
                success=(
                    process.returncode == 0
                ),
                exit_code=process.returncode,
                stdout=process.stdout.strip(),
                stderr=process.stderr.strip(),
                duration=round(
                    duration,
                    3,
                ),
            )


        except subprocess.TimeoutExpired:

            duration = (
                time.perf_counter()
                - start_time
            )


            return CommandResult(
                command=command,
                success=False,
                exit_code=-1,
                stdout="",
                stderr=(
                    "Command execution timed out."
                ),
                duration=round(
                    duration,
                    3,
                ),
            )


        except Exception as exc:

            duration = (
                time.perf_counter()
                - start_time
            )


            return CommandResult(
                command=command,
                success=False,
                exit_code=-1,
                stdout="",
                stderr=str(exc),
                duration=round(
                    duration,
                    3,
                ),
            )


    # ==========================================================
    # Helpers
    # ==========================================================

    def run_many(
        self,
        commands: list[str],
        cwd: str | Path | None = None,
    ) -> list[CommandResult]:
        """
        Execute multiple commands sequentially.
        """

        results: list[CommandResult] = []


        for command in commands:

            result = self.run(
                command=command,
                cwd=cwd,
            )

            results.append(
                result
            )


            # Stop after first failure
            if not result.success:
                break


        return results