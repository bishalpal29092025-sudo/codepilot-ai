"""
Prompt builder.

Builds LLM-ready prompts from GenerationContext.
"""

from __future__ import annotations

from core.models.generation import GenerationContext

from .renderer import PromptRenderer
from .templates import (
    CODE_GENERATION_TEMPLATE,
    DEPENDENCY_TEMPLATE,
    PROJECT_TEMPLATE,
    REPOSITORY_TEMPLATE,
    SYSTEM_TEMPLATE,
    TASK_TEMPLATE,
)


class PromptBuilder:
    """
    Builds complete generation prompts.

    Flow:

    GenerationContext
            |
            ▼
    PromptBuilder
            |
            ▼
    Rendered Prompt
    """

    def __init__(
        self,
        renderer: PromptRenderer | None = None,
    ) -> None:
        """
        Initialize prompt builder.
        """

        self.renderer = (
            renderer
            or PromptRenderer()
        )

    def build(
        self,
        context: GenerationContext,
    ) -> str:
        """
        Build final LLM prompt.

        Args:
            context:
                Generation context containing
                repository, project, task,
                and dependency information.

        Returns:
            Complete prompt string.
        """

        sections = [
            SYSTEM_TEMPLATE,
            self._build_repository_section(
                context
            ),
            self._build_project_section(
                context
            ),
            self._build_task_section(
                context
            ),
            self._build_dependency_section(
                context
            ),
            self._build_instruction_section(
                context
            ),
        ]

        return "\n\n".join(sections)

    # =========================================================
    # Sections
    # =========================================================

    def _build_repository_section(
        self,
        context: GenerationContext,
    ) -> str:
        """
        Render repository information.
        """

        return self.renderer.render(
            REPOSITORY_TEMPLATE,
            repository_name=context.repository.name,
            language=context.language,
            frameworks=", ".join(
                context.frameworks
            ),
            repository_files="\n".join(
                context.repository.repository_files
            ),
        )

    def _build_project_section(
        self,
        context: GenerationContext,
    ) -> str:
        """
        Render project information.
        """

        return self.renderer.render(
            PROJECT_TEMPLATE,
            project_name=context.project_name,
            summary=context.project.summary,
            objective=context.project.objective,
            architecture=context.project.architecture,
            constraints="\n".join(
                context.project.constraints
            ),
            coding_standards="\n".join(
                context.project.coding_standards
            ),
        )

    def _build_task_section(
        self,
        context: GenerationContext,
    ) -> str:
        """
        Render task information.
        """

        return self.renderer.render(
            TASK_TEMPLATE,
            task_title=context.task_title,
            task_description=context.task_description,
            priority=context.task.priority,
            complexity=context.task.complexity,
            acceptance_criteria="\n".join(
                context.task.acceptance_criteria
            ),
            relevant_files="\n".join(
                context.task.relevant_files
            ),
        )

    def _build_dependency_section(
        self,
        context: GenerationContext,
    ) -> str:
        """
        Render dependency information.
        """

        return self.renderer.render(
            DEPENDENCY_TEMPLATE,
            internal_modules="\n".join(
                context.dependencies.internal_modules
            ),
            external_packages="\n".join(
                context.dependencies.external_packages
            ),
            imports="\n".join(
                context.dependencies.imports
            ),
        )

    def _build_instruction_section(
        self,
        context: GenerationContext,
    ) -> str:
        """
        Render final generation instruction.
        """

        return self.renderer.render(
            CODE_GENERATION_TEMPLATE,
            task=context.task_description,
        )