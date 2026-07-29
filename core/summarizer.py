from pathlib import Path

from core.context import AgentContext
from core.models import Summary
from llm import llm

PROMPT_PATH = Path("prompts/summary.txt")


class Summarizer:
    """
    Generates a human-readable summary of the completed implementation.

    Responsibilities:
        - Build the summary prompt
        - Call the LLM
        - Validate the response
        - Store the summary inside AgentContext

    It does NOT:
        - Generate code
        - Execute commands
        - Modify files
        - Build the project
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
        Generate the final implementation summary.
        """

        self._print_header()

        prompt = self._build_prompt(context)

        response = self._generate_summary(prompt)

        context.summary = self._validate_summary(response)

        self._print_summary()

        return context

    # ==========================================================
    # Prompt Builder
    # ==========================================================

    def _build_prompt(
        self,
        context: AgentContext,
    ) -> str:
        """
        Construct the prompt sent to the LLM.
        """

        plan = context.plan
        code = context.code_response
        execution = context.execution_result

        generated_files = "\n".join(
            f"- {file.path}"
            for file in code.files
        )

        written_files = "\n".join(
            f"- {file}"
            for file in execution.written_files
        )

        failed_files = "\n".join(
            f"- {file}"
            for file in execution.failed_files
        )

        implementation_steps = "\n".join(
            f"- {step}"
            for step in plan.implementation_steps
        )

        return f"""
Goal

{plan.goal}

--------------------------------------------------

Implementation Steps

{implementation_steps}

--------------------------------------------------

Generated Files

{generated_files}

--------------------------------------------------

Successfully Written

{written_files if written_files else "None"}

--------------------------------------------------

Failed Writes

{failed_files if failed_files else "None"}
"""

    # ==========================================================
    # LLM
    # ==========================================================

    def _generate_summary(
        self,
        prompt: str,
    ) -> dict:
        """
        Generate a summary using the configured LLM.
        """

        try:

            return llm.chat_json(
                system_prompt=self.system_prompt,
                user_prompt=prompt,
                temperature=0.2,
            )

        except Exception as e:

            raise RuntimeError(
                f"Summary generation failed: {e}"
            ) from e

    # ==========================================================
    # Validation
    # ==========================================================

    def _validate_summary(
        self,
        response: dict,
    ) -> Summary:
        """
        Validate the LLM response.
        """

        try:

            return Summary.model_validate(response)

        except Exception as e:

            raise RuntimeError(
                f"Invalid summary response: {e}"
            ) from e

    # ==========================================================
    # Console Output
    # ==========================================================

    def _print_header(self) -> None:

        print("\n" + "=" * 70)
        print("📋 Summarizer")
        print("=" * 70)

    @staticmethod
    def _print_summary() -> None:

        print("✅ Summary generated.")