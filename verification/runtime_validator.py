"""
Runtime Validator.

Validates that the application starts successfully.

Runtime validation strategy:
- Execute application start command
- Capture startup output
- Detect startup failures
- Return RuntimeResult
"""

from __future__ import annotations

import time
from pathlib import Path

from core.context import AgentContext
from core.models import RuntimeResult
from services.process_runner import ProcessRunner


class RuntimeValidator:
    """
    Validates application runtime startup.
    """

    STARTUP_WAIT_SECONDS = 5

    def __init__(
        self,
        repository_path: str,
    ) -> None:

        self.repository_path = Path(
            repository_path
        )

        self.runner = ProcessRunner()


    # ==========================================================
    # Public API
    # ==========================================================

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:

        self._print_header()


        report = context.dependency_report


        if report is None:
            raise ValueError(
                "Dependency report is missing."
            )


        if not report.run_command:

            result = RuntimeResult(
                success=False,
                command="",
                logs="",
                errors=[
                    "No run command available."
                ],
            )

            context.runtime_result = result

            self._print_summary(
                result
            )

            return context



        print(
            f"Starting application: {report.run_command}"
        )


        process = self.runner.start(
            command=report.run_command,
            cwd=self.repository_path,
        )


        # Give application time to start
        time.sleep(
            self.STARTUP_WAIT_SECONDS
        )


        errors = self._extract_errors(
            process.stderr
        )


        success = (
            process.success
            or self._detect_startup_success(
                process.stdout
            )
        )


        result = RuntimeResult(
            success=success,
            command=process.command,
            logs=process.stdout,
            errors=errors,
        )


        context.runtime_result = result


        self._print_summary(
            result
        )


        return context


    # ==========================================================
    # Helpers
    # ==========================================================

    def _detect_startup_success(
        self,
        stdout: str,
    ) -> bool:
        """
        Detect common startup messages.
        """

        if not stdout:
            return False


        success_keywords = [
            "started",
            "running",
            "listening",
            "ready",
            "success",
        ]


        output = stdout.lower()


        return any(
            keyword in output
            for keyword in success_keywords
        )


    def _extract_errors(
        self,
        stderr: str,
    ) -> list[str]:

        if not stderr.strip():
            return []


        return [
            line.strip()
            for line in stderr.splitlines()
            if line.strip()
        ]


    # ==========================================================
    # Console
    # ==========================================================

    def _print_header(self) -> None:

        print("\n" + "=" * 70)
        print("🚀 Runtime Validator")
        print("=" * 70)


    def _print_summary(
        self,
        result: RuntimeResult,
    ) -> None:

        print(
            f"Command   : {result.command}"
        )

        print(
            f"Success   : {result.success}"
        )

        print(
            f"Errors    : {len(result.errors)}"
        )