from pathlib import Path

from core.models import Plan
from llm import llm


class Planner:
    """
    Generates a structured implementation plan.
    """

    def __init__(self):
        prompt_path = Path("prompts/planner.txt")

        self.system_prompt = prompt_path.read_text(
            encoding="utf-8"
        )

    def create_plan(
        self,
        repository_context: str,
        repository_files: str,
        user_request: str,
    ) -> Plan:

        print("\n" + "=" * 70)
        print("🧠 Planner")
        print("=" * 70)

        user_prompt = f"""
Repository Context:

{repository_context}

----------------------------------------

Repository Files:

{repository_files}

----------------------------------------

User Request:

{user_request}
"""

        response = llm.chat_json(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )

        plan = Plan.model_validate(response)

        print("✅ Plan generated.")
        print(f"Goal : {plan.goal}")
        print(f"Files: {len(plan.relevant_files)}")

        return plan