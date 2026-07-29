from pathlib import Path

from core.context import AgentContext
from core.models import BuildResult
from services.process_runner import ProcessRunner


class BuildValidator:
    """
    Validates that the repository builds successfully.
    """

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)
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

        if not report.build_command:

            result = BuildResult(
                success=False,
                command="",
                exit_code=-1,
                logs="",
                errors=["No build command available."],
            )

            context.build_result = result

            self._print_summary(result)

            return context

        process = self.runner.run(
            command=report.build_command,
            cwd=self.repository_path,
        )

        result = BuildResult(
            success=process.success,
            command=process.command,
            exit_code=process.exit_code,
            logs=process.stdout,
            errors=self._extract_errors(process.stderr),
        )

        context.build_result = result

        self._print_summary(result)

        return context

    # ==========================================================
    # Helpers
    # ==========================================================

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
        print("🔨 Build Validator")
        print("=" * 70)

    def _print_summary(
        self,
        result: BuildResult,
    ) -> None:

        print(f"Command      : {result.command}")
        print(f"Success      : {result.success}")
        print(f"Exit Code    : {result.exit_code}")
        print(f"Errors       : {len(result.errors)}")