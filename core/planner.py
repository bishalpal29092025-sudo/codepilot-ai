from pathlib import Path

from core.context import AgentContext
from core.models import Plan
from llm import llm

PROMPT_PATH = Path("prompts/planner.txt")


class Planner:
    """
    Planner is responsible for converting a user's request and
    repository metadata into a structured implementation plan.

    Responsibilities:
        - Build the planner prompt
        - Call the LLM
        - Validate the response
        - Store the plan inside AgentContext

    It does NOT:
        - Read repository files
        - Generate code
        - Execute commands
        - Modify the repository
    """

    def __init__(self) -> None:
        self.system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    # ==========================================================
    # Public API
    # ==========================================================

    def run(self, context: AgentContext) -> AgentContext:
        """
        Generate an implementation plan and store it in the context.

        Args:
            context: Shared AgentContext

        Returns:
            Updated AgentContext containing a validated Plan.
        """

        self._print_header()

        prompt = self._build_prompt(context)

        response = self._generate_plan(prompt)

        context.plan = self._validate_plan(response)

        self._print_summary(context.plan)

        return context

    # ==========================================================
    # Private Methods
    # ==========================================================

    def _build_prompt(self, context: AgentContext) -> str:
        """Construct the user prompt sent to the LLM."""

        repository = context.repository_info

        files = "\n".join(repository.files)

        return f"""
Repository Context

Language: {repository.language}
Framework: {repository.framework}
Database: {repository.database}
Package Manager: {repository.package_manager}

--------------------------------------------------

Repository Files

{files}

--------------------------------------------------

User Request

{context.user_request}
"""

    def _generate_plan(self, prompt: str) -> dict:
        """
        Generate a plan using the configured LLM.
        """

        try:
            return llm.chat_json(
                system_prompt=self.system_prompt,
                user_prompt=prompt,
            )

        except Exception as e:
            raise RuntimeError(
                f"Planner failed while generating implementation plan: {e}"
            ) from e

    def _validate_plan(self, response: dict) -> Plan:
        """
        Validate the LLM response against the Plan model.
        """

        try:
            return Plan.model_validate(response)

        except Exception as e:
            raise RuntimeError(
                f"Planner returned an invalid response: {e}"
            ) from e

    # ==========================================================
    # Console Output
    # ==========================================================

    def _print_header(self) -> None:
        print("\n" + "=" * 70)
        print("🧠 Planner")
        print("=" * 70)

    def _print_summary(self, plan: Plan) -> None:
        print("✅ Plan generated.")
        print(f"Goal : {plan.goal}")
        print(f"Files: {len(plan.relevant_files)}")