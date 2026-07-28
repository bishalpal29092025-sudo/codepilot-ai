from pathlib import Path

from core.models import (
    CodeResponse,
    ExecutionResult,
    Plan,
    Summary,
)
from llm import llm


class Summarizer:
    """
    Generates a summary of the implementation.
    """

    def __init__(self):

        prompt_path = Path("prompts/summary.txt")

        self.system_prompt = prompt_path.read_text(
            encoding="utf-8"
        )

    # -------------------------------------------------
    # Generate Summary
    # -------------------------------------------------

    def summarize(
        self,
        plan: Plan,
        code: CodeResponse,
        execution: ExecutionResult,
    ) -> Summary:

        print("\n" + "=" * 70)
        print("📋 Summarizer")
        print("=" * 70)

        user_prompt = self._build_prompt(
            plan,
            code,
            execution,
        )

        response = llm.chat_json(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.2,
        )

        summary = Summary.model_validate(response)

        print("✅ Summary generated.")

        return summary

    # -------------------------------------------------
    # Prompt Builder
    # -------------------------------------------------

    def _build_prompt(
        self,
        plan: Plan,
        code: CodeResponse,
        execution: ExecutionResult,
    ) -> str:

        files = "\n".join(
            f"- {file.path}"
            for file in code.files
        )

        written = "\n".join(
            f"- {file}"
            for file in execution.written_files
        )

        failed = "\n".join(
            f"- {file}"
            for file in execution.failed_files
        )

        return f"""
Goal

{plan.goal}

----------------------------------------

Implementation Steps

{chr(10).join("- " + step for step in plan.implementation_steps)}

----------------------------------------

Generated Files

{files}

----------------------------------------

Successfully Written

{written if written else "None"}

----------------------------------------

Failed Writes

{failed if failed else "None"}
"""