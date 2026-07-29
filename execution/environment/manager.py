"""
Execution environment manager.

Responsible for preparing project environments
before running commands.

Supports:
- Python
- Node.js
- Rust
"""

from __future__ import annotations

from pathlib import Path

from core.context import AgentContext

from execution.runner.command_runner import CommandRunner


class EnvironmentManager:
    """
    Prepares and validates execution environments.
    """

    def __init__(
        self,
        repository_path: str,
    ) -> None:

        self.repository_path = Path(
            repository_path
        )

        self.runner = CommandRunner()


    # ==========================================================
    # Public API
    # ==========================================================

    def prepare(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Prepare repository environment.

        Steps:

        1. Read dependency information
        2. Install dependencies
        3. Store result in context
        """

        self._print_header()


        report = context.dependency_report

        if report is None:
            raise ValueError(
                "Dependency report is missing."
            )


        if report.install_command:

            result = self.runner.run(
                command=report.install_command,
                cwd=self.repository_path,
            )

            context.environment_result = result

            self._print_summary(
                result
            )

        else:

            print(
                "No dependency installation required."
            )


        return context


    # ==========================================================
    # Runtime Detection
    # ==========================================================

    def detect_runtime(
        self,
        context: AgentContext,
    ) -> str:
        """
        Detect project runtime.
        """

        report = context.dependency_report


        if report is None:
            return "unknown"


        language = (
            report.language.lower()
        )


        if language == "python":
            return "python"


        if language in (
            "javascript",
            "typescript",
        ):
            return "node"


        if language == "rust":
            return "rust"


        return "unknown"


    # ==========================================================
    # Console
    # ==========================================================

    def _print_header(self) -> None:

        print("\n" + "=" * 70)
        print("⚙️ Environment Manager")
        print("=" * 70)


    def _print_summary(
        self,
        result,
    ) -> None:

        print(
            f"Install Command : {result.command}"
        )

        print(
            f"Success         : {result.success}"
        )

        print(
            f"Exit Code       : {result.exit_code}"
        )