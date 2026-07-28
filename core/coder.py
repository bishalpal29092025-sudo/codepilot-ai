from pathlib import Path

from core.models import (
    CodeResponse,
    Plan,
    RepositoryContext,
)
from llm import llm


class CodeGenerator:
    """
    Generates code modifications using the LLM.
    """

    def __init__(self):

        prompt_path = Path("prompts/coder.txt")

        self.system_prompt = prompt_path.read_text(
            encoding="utf-8"
        )

    # -------------------------------------------------
    # Generate Code
    # -------------------------------------------------

    def generate(
        self,
        plan: Plan,
        repository: RepositoryContext,
    ) -> CodeResponse:

        print("\n" + "=" * 70)
        print("💻 Code Generator")
        print("=" * 70)

        user_prompt = self._build_prompt(
            plan,
            repository,
        )

        response = llm.chat_json(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            temperature=0.1,
        )

        code = CodeResponse.model_validate(response)

        print(f"✅ Generated {len(code.files)} file(s).")

        return code

    # -------------------------------------------------
    # Prompt Builder
    # -------------------------------------------------

    def _build_prompt(
        self,
        plan: Plan,
        repository: RepositoryContext,
    ) -> str:

        sections = []

        sections.append(
            f"""
Goal

{plan.goal}
"""
        )

        sections.append(
            """
Implementation Steps
"""
        )

        for step in plan.implementation_steps:
            sections.append(f"- {step}")

        sections.append(
            """

Repository Files

"""
        )

        for path, content in repository.files.items():

            sections.append(
                f"""
==================================================
FILE: {path}
==================================================

{content}

"""
            )

        return "\n".join(sections)