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
        - Build coding prompt
        - Call LLM
        - Normalize LLM response
        - Validate generated code
        - Store CodeResponse in AgentContext

    It does NOT:
        - Write files
        - Execute commands
        - Build the project
        - Verify output
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
        Generate code changes from implementation plan.
        """

        self._print_header()


        prompt = self._build_prompt(
            context
        )


        response = self._generate_code(
            prompt
        )


        context.code_response = (
            self._validate_response(
                response
            )
        )


        self._print_summary(
            context.code_response
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
        Build prompt for code generation.
        """

        plan = context.plan
        repository = context.repository_context


        if plan is None:
            raise ValueError(
                "Implementation plan missing."
            )


        if repository is None:
            raise ValueError(
                "Repository context missing."
            )


        sections = []


        sections.append(
            f"""
Project Goal

{plan.objective or plan.summary}
"""
        )


        sections.append(
            """
Implementation Tasks

"""
        )


        for task in plan.tasks:

            sections.append(
                f"""
Task:
{task.title}

Description:
{task.description}

Affected Files:
{task.affected_files}

"""
            )


        sections.append(
            """
Relevant Files

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


        return "\n".join(
            sections
        )


    # ==========================================================
    # LLM
    # ==========================================================

    def _generate_code(
        self,
        prompt: str,
    ) -> dict:
        """
        Generate code using LLM.
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
    # Validation + Normalization
    # ==========================================================

    def _validate_response(
        self,
        response: dict,
    ) -> CodeResponse:
        """
        Normalize and validate LLM response.

        Supports both:

        New format:
        {
            success,
            status,
            provider,
            files:[]
        }


        Old/simple format:
        {
            files:[]
        }
        """

        try:

            # --------------------------------------------------
            # Default metadata
            # --------------------------------------------------

            response.setdefault(
                "success",
                True,
            )


            response.setdefault(
                "status",
                "completed",
            )


            response.setdefault(
                "provider",
                "cerebras",
            )


            # --------------------------------------------------
            # Normalize files
            # --------------------------------------------------

            files = []


            for file in response.get(
                "files",
                [],
            ):

                file = dict(
                    file
                )


                path = file.get(
                    "path",
                    "",
                )


                # Detect language

                if "language" not in file:

                    extension = (
                        Path(path)
                        .suffix
                        .replace(
                            ".",
                            "",
                        )
                        .lower()
                    )


                    language_map = {

                        "js": "javascript",
                        "jsx": "javascript",

                        "ts": "typescript",
                        "tsx": "typescript",

                        "py": "python",

                        "rs": "rust",

                        "java": "java",

                        "json": "json",

                        "md": "markdown",

                    }


                    file["language"] = (
                        language_map.get(
                            extension,
                            "unknown",
                        )
                    )


                # Default operation

                file.setdefault(
                    "operation",
                    "create",
                )


                files.append(
                    file
                )


            response["files"] = files


            return CodeResponse.model_validate(
                response
            )


        except Exception as e:

            raise RuntimeError(
                f"Invalid code generation response: {e}"
            ) from e



    # ==========================================================
    # Console Output
    # ==========================================================

    def _print_header(
        self,
    ) -> None:

        print("\n" + "=" * 70)
        print("💻 Code Generator")
        print("=" * 70)



    def _print_summary(
        self,
        code: CodeResponse,
    ) -> None:

        print(
            f"✅ Generated {len(code.files)} file(s)."
        )