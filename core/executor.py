from pathlib import Path

from core.models import CodeResponse, ExecutionResult


class CodeExecutor:
    """
    Writes generated code to the repository.

    Responsibilities:
    - Create missing directories
    - Write files
    - Prevent writing outside the repository
    - Return execution results
    """

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path).resolve()

    # -------------------------------------------------
    # Execute
    # -------------------------------------------------

    def execute(
        self,
        response: CodeResponse,
    ) -> ExecutionResult:

        print("\n" + "=" * 70)
        print("📝 Code Executor")
        print("=" * 70)

        result = ExecutionResult()

        for generated_file in response.files:

            try:

                output_path = (
                    self.repository_path / generated_file.path
                ).resolve()

                # -----------------------------
                # Prevent Path Traversal
                # -----------------------------

                output_path.relative_to(self.repository_path)

                # -----------------------------
                # Create Parent Directories
                # -----------------------------

                output_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                # -----------------------------
                # Write File
                # -----------------------------

                output_path.write_text(
                    generated_file.content,
                    encoding="utf-8",
                )

                result.written_files.append(
                    generated_file.path
                )

                print(f"✅ Wrote: {generated_file.path}")

            except Exception as e:

                result.failed_files.append(
                    generated_file.path
                )

                print(f"❌ Failed: {generated_file.path}")
                print(e)

        print("\n" + "-" * 70)
        print(f"Written : {len(result.written_files)}")
        print(f"Failed  : {len(result.failed_files)}")
        print("-" * 70)

        return result