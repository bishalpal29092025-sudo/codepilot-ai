from pathlib import Path

from core.context import AgentContext
from core.models import CodeResponse, ExecutionResult

class CodeExecutor:
    """
    Writes generated code to the repository.

    Responsibilities:
        - Validate output paths
        - Create missing directories
        - Write generated files
        - Store execution results in AgentContext

    It does NOT:
        - Generate code
        - Build the project
        - Execute tests
        - Analyse failures
    """

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path).resolve()

    # ==========================================================
    # Public API
    # ==========================================================

    def run(self, context: AgentContext) -> AgentContext:
        """
        Write generated files to the repository.
        """

        self._print_header()

        result = ExecutionResult()

        self._write_files(
            context.code_response,
            result,
        )

        context.execution_result = result

        self._print_summary(result)

        return context

    # ==========================================================
    # File Writing
    # ==========================================================

    def _write_files(
        self,
        response: CodeResponse,
        result: ExecutionResult,
    ) -> None:
        """
        Write every generated file.
        """

        for generated_file in response.files:
            self._write_file(generated_file, result)

    def _write_file(
        self,
        generated_file,
        result: ExecutionResult,
    ) -> None:
        """
        Write a single generated file.
        """

        try:

            output_path = self._validate_path(
                generated_file.path
            )

            self._ensure_directory(output_path)

            output_path.write_text(
                generated_file.content,
                encoding="utf-8",
            )

            result.written_files.append(
                generated_file.path
            )

            print(f"✅ Wrote : {generated_file.path}")

        except Exception as e:

            result.failed_files.append(
                generated_file.path
            )

            print(f"❌ Failed : {generated_file.path}")
            print(e)

    # ==========================================================
    # Helpers
    # ==========================================================

    def _validate_path(
        self,
        relative_path: str,
    ) -> Path:
        """
        Prevent writing outside the repository.
        """

        output_path = (
            self.repository_path / relative_path
        ).resolve()

        output_path.relative_to(
            self.repository_path
        )

        return output_path

    @staticmethod
    def _ensure_directory(
        output_path: Path,
    ) -> None:
        """
        Create parent directories if necessary.
        """

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ==========================================================
    # Console Output
    # ==========================================================

    def _print_header(self) -> None:

        print("\n" + "=" * 70)
        print("📝 Code Executor")
        print("=" * 70)

    @staticmethod
    def _print_summary(
        result: ExecutionResult,
    ) -> None:

        print("\n" + "-" * 70)
        print(f"Written : {len(result.written_files)}")
        print(f"Failed  : {len(result.failed_files)}")
        print("-" * 70)