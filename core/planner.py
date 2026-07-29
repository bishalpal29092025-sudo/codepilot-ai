from pathlib import Path

from core.context import AgentContext
from core.models import Plan
from llm import llm


class Planner:
    """
    Generates a structured implementation plan
    and stores it inside AgentContext.
    """

    def __init__(self):
        prompt_path = Path("prompts/planner.txt")

        self.system_prompt = prompt_path.read_text(
            encoding="utf-8"
        )

    # -------------------------------------------------
    # Main Entry
    # -------------------------------------------------

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:

        print("\n" + "=" * 70)
        print("🧠 Planner")
        print("=" * 70)

        repository = context.repository_info

        user_prompt = f"""
Repository Context

Language: {repository.language}
Framework: {repository.framework}
Database: {repository.database}
Package Manager: {repository.package_manager}

--------------------------------------------------

Repository Files

{chr(10).join(repository.files)}

--------------------------------------------------

User Request

{context.user_request}
"""

        response = llm.chat_json(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )

        context.plan = Plan.model_validate(response)

        print("✅ Plan generated.")
        print(f"Goal : {context.plan.goal}")
        print(f"Files: {len(context.plan.relevant_files)}")

        return context