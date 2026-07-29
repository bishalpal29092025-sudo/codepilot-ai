from config import DEFAULT_REPOSITORY

from core.context import AgentContext
from core.coder import CodeGenerator
from core.executor import CodeExecutor
from core.explorer import RepositoryExplorer
from core.planner import Planner
from core.reader import RepositoryReader
from core.summarizer import Summarizer

from verification.dependency_checker import DependencyChecker
from verification.build_validator import BuildValidator


class CodePilotAgent:
    """
    Main orchestration pipeline for CodePilot AI.
    """

    def __init__(self, repository_path: str):
        self.repository_path = repository_path

        # ============================
        # Core Pipeline
        # ============================

        self.explorer = RepositoryExplorer(repository_path)
        self.dependency_checker = DependencyChecker(repository_path)
        self.planner = Planner()
        self.reader = RepositoryReader(repository_path)
        self.coder = CodeGenerator()
        self.executor = CodeExecutor(repository_path)
        self.build_validator = BuildValidator(repository_path)
        self.summarizer = Summarizer()

    def run(self, user_request: str) -> AgentContext:
        """
        Execute the complete CodePilot pipeline.
        """

        context = AgentContext(
            user_request=user_request,
        )

        # =====================================
        # Repository Analysis
        # =====================================

        context = self.explorer.run(context)

        context = self.dependency_checker.run(context)

        # =====================================
        # Planning
        # =====================================

        context = self.planner.run(context)

        # =====================================
        # Repository Understanding
        # =====================================

        context = self.reader.run(context)

        # =====================================
        # Code Generation
        # =====================================

        context = self.coder.run(context)

        # =====================================
        # File Execution
        # =====================================

        context = self.executor.run(context)

        # =====================================
        # Verification
        # =====================================

        context = self.build_validator.run(context)

        # =====================================
        # Summary
        # =====================================

        context = self.summarizer.run(context)

        return context


def main() -> None:
    print("=" * 80)
    print("🚀 CodePilot AI")
    print("=" * 80)

    user_request = input("\nEnter your request:\n> ")

    agent = CodePilotAgent(DEFAULT_REPOSITORY)

    try:
        context = agent.run(user_request)

        print("\n" + "=" * 80)
        print("✅ CodePilot AI Finished Successfully")
        print("=" * 80)

        if context.summary:
            print("\n📋 Summary")
            print("-" * 80)
            print(context.summary)

        if context.build_result:
            print("\n🔨 Build Result")
            print("-" * 80)
            print(f"Success   : {context.build_result.success}")
            print(f"Command   : {context.build_result.command}")
            print(f"Exit Code : {context.build_result.exit_code}")

            if context.build_result.errors:
                print("\nErrors:")
                for error in context.build_result.errors:
                    print(f"  • {error}")

    except KeyboardInterrupt:
        print("\n\n⚠️ Pipeline interrupted by user.")

    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ Pipeline Failed")
        print("=" * 80)
        print(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    main()