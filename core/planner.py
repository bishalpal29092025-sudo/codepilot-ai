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

        self.system_prompt = PROMPT_PATH.read_text(
            encoding="utf-8"
        )


    # ==========================================================
    # Public API
    # ==========================================================

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Generate implementation plan.
        """

        self._print_header()


        prompt = self._build_prompt(
            context
        )


        response = self._generate_plan(
            prompt
        )


        context.plan = self._validate_plan(
            response
        )


        self._print_summary(
            context.plan
        )


        return context


    # ==========================================================
    # Prompt Builder
    # ==========================================================

    def _build_prompt(
        self,
        context: AgentContext,
    ) -> str:
        """
        Build planner prompt from repository metadata.
        """

        repository = context.repository_info


        if repository is None:
            raise ValueError(
                "Repository information is missing."
            )


        files = "\n".join(
            repository.repository_files
        )


        frameworks = ", ".join(
            repository.frameworks
        )


        return f"""
Repository Context

Name:
{repository.name}

Root Path:
{repository.root_path}

Project Type:
{repository.project_type}

Primary Language:
{repository.primary_language}

Frameworks:
{frameworks}

Database:
{repository.database}

Package Manager:
{repository.package_manager}


--------------------------------------------------

Repository Files

{files}


--------------------------------------------------

User Request

{context.user_request}
"""


    # ==========================================================
    # LLM
    # ==========================================================

    def _generate_plan(
        self,
        prompt: str,
    ) -> dict:
        """
        Generate plan using LLM.
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


    # ==========================================================
    # Validation
    # ==========================================================

    def _validate_plan(
        self,
        response: dict,
    ) -> Plan:
        """
        Validate LLM response.
        """

        try:

            return Plan.model_validate(
                response
            )


        except Exception as e:

            raise RuntimeError(
                f"Planner returned an invalid response: {e}"
            ) from e


    # ==========================================================
    # Console
    # ==========================================================

    def _print_header(self):

        print("\n" + "=" * 70)
        print("🧠 Planner")
        print("=" * 70)


    def _print_summary(
        self,
        plan: Plan,
    ):

        print(
            "✅ Plan generated."
        )

        print(
            f"Objective : {plan.objective}"
        )

        print(
            f"Summary   : {plan.summary}"
        )

        print(
            f"Files     : {len(plan.relevant_files)}"
        )

        print(
            f"Tasks     : {len(plan.tasks)}"
        )

        print(
            f"Risks     : {len(plan.risks)}"
        )