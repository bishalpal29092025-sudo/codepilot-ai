from pathlib import Path

from core.context import AgentContext
from core.models import CodeResponse
from llm import llm

PROMPT_PATH = Path("prompts/coder.txt")


class CodeGenerator:
    """
    Generates code modifications using the implementation plan
    and repository context.

    Responsibilities:
        - Build the coding prompt
        - Call the LLM
        - Validate the generated response
        - Store the generated code in AgentContext

    It does NOT:
        - Write files
        - Execute commands
        - Build the project
        - Summarize results
    """

    def __init__(self) -> None:
        self.system_prompt = PROMPT_PATH.read_text(
            encoding="utf-8"
        )

    # ==========================================================
    # Public API
    # ==========================================================

    def run(self, context: AgentContext) -> AgentContext:
        """
        Generate code changes from the implementation plan.

        Args:
            context: Shared AgentContext

        Returns:
            Updated AgentContext containing CodeResponse.
        """

        self._print_header()

        prompt = self._build_prompt(context)

        response = self._generate_code(prompt)

        context.code_response = self._validate_response(response)

        self._print_summary(context.code_response)

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
        repository = context.repository_context

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

    # ==========================================================
    # LLM
    # ==========================================================

    def _generate_code(
        self,
        prompt: str,
    ) -> dict:
        """
        Generate code using the configured LLM.
        """

        try:

            return llm.chat_json(
                system_prompt=self.system_prompt,
                user_prompt=prompt,
                temperature=0.1,
            )

        except Exception as e:

            raise RuntimeError(
                f"Code generation failed: {e}"
            ) from e

    # ==========================================================
    # Validation
    # ==========================================================

    def _validate_response(
        self,
        response: dict,
    ) -> CodeResponse:
        """
        Validate the LLM response.
        """

        try:

            return CodeResponse.model_validate(response)

        except Exception as e:

            raise RuntimeError(
                f"Invalid code generation response: {e}"
            ) from e

    # ==========================================================
    # Console Output
    # ==========================================================

    def _print_header(self) -> None:

        print("\n" + "=" * 70)
        print("💻 Code Generator")
        print("=" * 70)

    def _print_summary(
        self,
        code: CodeResponse,
    ) -> None:

        print(f"✅ Generated {len(code.files)} file(s).")