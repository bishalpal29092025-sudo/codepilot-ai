from config import DEFAULT_REPOSITORY

from core.context import AgentContext
from core.coder import CodeGenerator
from core.executor import CodeExecutor
from core.explorer import RepositoryExplorer
from core.planner import Planner
from core.reader import RepositoryReader
from core.summarizer import Summarizer


def main():

    print("=" * 80)
    print("🚀 CodePilot AI")
    print("=" * 80)

    user_request = input("\nEnter your request:\n> ")

    context = AgentContext(
        user_request=user_request
    )

    # =====================================================
    # Repository Analysis
    # =====================================================

    explorer = RepositoryExplorer(DEFAULT_REPOSITORY)

    context.repository_info = explorer.get_context()

    explorer.summary()

    # =====================================================
    # Planner
    # =====================================================

    planner = Planner()

    context.plan = planner.create_plan(
        repository_context=str(context.repository_info),
        repository_files="\n".join(
            context.repository_info["files"]
        ),
        user_request=context.user_request,
    )

    # =====================================================
    # Reader
    # =====================================================

    reader = RepositoryReader(DEFAULT_REPOSITORY)

    context.repository_context = reader.read(
        context.plan
    )

    # =====================================================
    # Code Generator
    # =====================================================

    generator = CodeGenerator()

    context.generated_code = generator.generate(
        context.plan,
        context.repository_context,
    )

    # =====================================================
    # Executor
    # =====================================================

    executor = CodeExecutor(DEFAULT_REPOSITORY)

    context.execution_result = executor.execute(
        context.generated_code
    )

    # =====================================================
    # Summarizer
    # =====================================================

    summarizer = Summarizer()

    context.summary = summarizer.generate(
        context.plan,
        context.execution_result,
    )

    # =====================================================
    # Finish
    # =====================================================

    print("\n")
    print("=" * 80)
    print("✅ CodePilot AI Finished Successfully")
    print("=" * 80)


if __name__ == "__main__":
    main()