from config import DEFAULT_REPOSITORY

from core.coder import CodeGenerator
from core.executor import CodeExecutor
from core.explorer import RepositoryExplorer
from core.planner import Planner
from core.reader import RepositoryReader
from core.summarizer import Summarizer


class CodePilotAgent:
    """
    Main orchestrator for CodePilot AI.
    """

    def __init__(self, repository_path: str):

        self.repository_path = repository_path

        self.explorer = RepositoryExplorer(repository_path)
        self.planner = Planner()
        self.reader = RepositoryReader(repository_path)
        self.coder = CodeGenerator()
        self.executor = CodeExecutor(repository_path)
        self.summarizer = Summarizer()

    # -------------------------------------------------
    # Run Agent
    # -------------------------------------------------

    def run(self, user_request: str):

        print("\n" + "=" * 70)
        print("🚀 CodePilot AI")
        print("=" * 70)

        # -----------------------------------------
        # Repository Analysis
        # -----------------------------------------

        self.explorer.summary()

        repository_context = self.explorer.get_context()

        repository_context_text = f"""
Language: {repository_context['language']}
Framework: {repository_context['framework']}
Database: {repository_context['database']}
Package Manager: {repository_context['package_manager']}
"""

        repository_files = "\n".join(
            repository_context["files"]
        )

        # -----------------------------------------
        # Planner
        # -----------------------------------------

        plan = self.planner.create_plan(
            repository_context=repository_context_text,
            repository_files=repository_files,
            user_request=user_request,
        )

        # -----------------------------------------
        # Reader
        # -----------------------------------------

        source_context = self.reader.read(plan)

        # -----------------------------------------
        # Code Generator
        # -----------------------------------------

        generated_code = self.coder.generate(
            plan,
            source_context,
        )

        # -----------------------------------------
        # Executor
        # -----------------------------------------

        execution = self.executor.execute(
            generated_code
        )

        # -----------------------------------------
        # Summarizer
        # -----------------------------------------

        summary = self.summarizer.summarize(
            plan,
            generated_code,
            execution,
        )

        # -----------------------------------------
        # Final Report
        # -----------------------------------------

        self.print_summary(summary)

    # -------------------------------------------------
    # Final Output
    # -------------------------------------------------

    @staticmethod
    def print_summary(summary):

        print("\n")
        print("=" * 70)
        print("🎉 Completed")
        print("=" * 70)

        print("\n📂 Files Changed")

        if summary.files_changed:
            for file in summary.files_changed:
                print(f"✓ {file}")
        else:
            print("No files changed.")

        print("\n✨ Features")

        if summary.features_added:
            for feature in summary.features_added:
                print(f"• {feature}")
        else:
            print("No new features.")

        print("\n🧪 Testing")

        if summary.testing:
            for test in summary.testing:
                print(f"• {test}")
        else:
            print("No testing information.")

        print("\n📝 Notes")

        if summary.notes:
            for note in summary.notes:
                print(f"• {note}")
        else:
            print("No additional notes.")


# -------------------------------------------------
# Interactive CLI
# -------------------------------------------------

def print_banner():
    print("\n" + "=" * 70)
    print("🤖 CodePilot AI")
    print("=" * 70)
    print("Interactive Coding Agent")
    print()
    print("Type your software request.")
    print("Commands:")
    print("  exit / quit  -> Close CodePilot")
    print("  clear        -> Clear terminal")
    print("=" * 70)


def main():

    print_banner()

    agent = CodePilotAgent(DEFAULT_REPOSITORY)

    while True:

        try:

            request = input("\n💬 Request\n> ").strip()

            if not request:
                continue

            command = request.lower()

            if command in {"exit", "quit"}:
                print("\n👋 Shutting down CodePilot AI...")
                break

            if command == "clear":
                import os

                os.system("cls" if os.name == "nt" else "clear")
                print_banner()
                continue

            agent.run(request)

            print("\n" + "-" * 70)
            print("✅ Ready for the next request.")
            print("-" * 70)

        except KeyboardInterrupt:
            print("\n\n👋 CodePilot AI stopped.")
            break

        except Exception as e:
            print("\n❌ An unexpected error occurred.")
            print(e)
            print("\n🔄 CodePilot AI is still running...")


if __name__ == "__main__":
    main()