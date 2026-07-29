from pathlib import Path

from core.context import AgentContext
from core.models import RuntimeResult
from services.process_runner import ProcessRunner


class RuntimeValidator:
    """
    Validates that the application starts successfully.
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
            raise ValueError("Dependency report is missing.")

        if not report.run_command:

            context.runtime_result = RuntimeResult(
                success=False,
                command="",
                logs="",
                errors=["No run command available."],
            )

            self._print_summary(context.runtime_result)

            return context

        process = self.runner.start(
            command=report.run_command,
            cwd=self.repository_path,
        )

        context.runtime_result = RuntimeResult(
            success=process.success,
            command=process.command,
            logs=process.stdout,
            errors=self._extract_errors(process.stderr),
        )

        self._print_summary(context.runtime_result)

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
        print("🚀 Runtime Validator")
        print("=" * 70)

    def _print_summary(
        self,
        result: RuntimeResult,
    ) -> None:

        print(f"Command   : {result.command}")
        print(f"Success   : {result.success}")
        print(f"Errors    : {len(result.errors)}")