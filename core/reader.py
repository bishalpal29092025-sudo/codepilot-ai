from pathlib import Path

from core.models import Plan, RepositoryContext


class RepositoryReader:
    """
    Reads only the files selected by the Planner.

    Responsibilities:
    - Read relevant repository files
    - Ignore missing files
    - Skip binary/unreadable files
    - Return structured repository context
    """

    MAX_FILE_SIZE = 500_000  # 500 KB

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    def read(self, plan: Plan) -> RepositoryContext:

        print("\n" + "=" * 70)
        print("📖 Repository Reader")
        print("=" * 70)

        context = RepositoryContext()

        for relative_path in plan.relevant_files:

            absolute_path = self.repository_path / relative_path

            if not absolute_path.exists():

                print(f"❌ Missing : {relative_path}")

                context.missing_files.append(relative_path)
                continue

            if absolute_path.is_dir():

                print(f"⚠️ Skipped Directory : {relative_path}")

                context.skipped_files.append(relative_path)
                continue

            try:

                if absolute_path.stat().st_size > self.MAX_FILE_SIZE:

                    print(f"⚠️ Large File Skipped : {relative_path}")

                    context.skipped_files.append(relative_path)
                    continue

                with open(
                    absolute_path,
                    "r",
                    encoding="utf-8",
                ) as f:

                    code = f.read()

                context.files[relative_path] = code
                context.loaded_files.append(relative_path)

                print(f"✅ Loaded : {relative_path}")

            except UnicodeDecodeError:

                print(f"⚠️ Binary File Skipped : {relative_path}")

                context.skipped_files.append(relative_path)

            except Exception as e:

                print(f"❌ Error : {relative_path}")
                print(e)

                context.skipped_files.append(relative_path)

        print("\n" + "-" * 70)
        print(f"Loaded Files : {len(context.loaded_files)}")
        print(f"Missing      : {len(context.missing_files)}")
        print(f"Skipped      : {len(context.skipped_files)}")
        print("-" * 70)

        return context

    # -----------------------------------------------------
    # Helper
    # -----------------------------------------------------

    @staticmethod
    def format_context(context: RepositoryContext) -> str:
        """
        Convert repository context into a prompt
        for the LLM.
        """

        sections = []

        for path, content in context.files.items():

            sections.append(
                f"""
==============================
FILE: {path}
==============================

{content}
"""
            )

        return "\n".join(sections)