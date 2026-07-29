from pathlib import Path

from core.context import AgentContext
from core.models import RepositoryContext


class RepositoryReader:
    """
    Reads only the repository files selected by the Planner.

    Responsibilities:
        - Read relevant repository files
        - Ignore missing files
        - Skip directories
        - Skip binary files
        - Skip oversized files
        - Store RepositoryContext inside AgentContext

    It does NOT:
        - Generate code
        - Execute commands
        - Modify files
    """

    MAX_FILE_SIZE = 500_000  # 500 KB

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)

    # ==========================================================
    # Public API
    # ==========================================================

    def run(self, context: AgentContext) -> AgentContext:
        """
        Read all files selected by the Planner and populate
        context.repository_context.
        """

        self._print_header()

        repository_context = RepositoryContext()

        for relative_path in context.plan.relevant_files:
            self._read_file(
                relative_path,
                repository_context,
            )

        context.repository_context = repository_context

        self._print_summary(repository_context)

        return context

    # ==========================================================
    # Private Methods
    # ==========================================================

    def _read_file(
        self,
        relative_path: str,
        repository_context: RepositoryContext,
    ) -> None:
        """
        Read a single repository file.
        """

        absolute_path = self.repository_path / relative_path

        if not absolute_path.exists():
            print(f"❌ Missing : {relative_path}")
            repository_context.missing_files.append(relative_path)
            return

        if absolute_path.is_dir():
            print(f"⚠️ Skipped Directory : {relative_path}")
            repository_context.skipped_files.append(relative_path)
            return

        try:
            if absolute_path.stat().st_size > self.MAX_FILE_SIZE:
                print(f"⚠️ Large File Skipped : {relative_path}")
                repository_context.skipped_files.append(relative_path)
                return

            code = absolute_path.read_text(encoding="utf-8")

            repository_context.files[relative_path] = code
            repository_context.loaded_files.append(relative_path)

            print(f"✅ Loaded : {relative_path}")

        except UnicodeDecodeError:
            print(f"⚠️ Binary File Skipped : {relative_path}")
            repository_context.skipped_files.append(relative_path)

        except Exception as e:
            print(f"❌ Error : {relative_path}")
            print(e)

            repository_context.skipped_files.append(relative_path)

    # ==========================================================
    # Utilities
    # ==========================================================

    @staticmethod
    def format_context(repository_context: RepositoryContext) -> str:
        """
        Convert repository context into a formatted string
        suitable for sending to the LLM.
        """

        sections = []

        for path, content in repository_context.files.items():
            sections.append(
                f"""
==============================
FILE: {path}
==============================

{content}
"""
            )

        return "\n".join(sections)

    # ==========================================================
    # Console Output
    # ==========================================================

    def _print_header(self) -> None:
        print("\n" + "=" * 70)
        print("📖 Repository Reader")
        print("=" * 70)

    def _print_summary(
        self,
        repository_context: RepositoryContext,
    ) -> None:
        print("\n" + "-" * 70)
        print(f"Loaded Files : {len(repository_context.loaded_files)}")
        print(f"Missing      : {len(repository_context.missing_files)}")
        print(f"Skipped      : {len(repository_context.skipped_files)}")
        print("-" * 70)