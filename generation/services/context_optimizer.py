"""
Generation context optimizer.

Reduces unnecessary context before prompt generation.
"""

from __future__ import annotations

from core.models.generation import GenerationContext


class ContextOptimizer:
    """
    Optimizes GenerationContext before sending it
    to an LLM provider.
    """

    def __init__(
        self,
        max_files: int = 50,
    ) -> None:
        """
        Initialize optimizer.

        Args:
            max_files:
                Maximum number of files kept in context.
        """

        self.max_files = max_files

    # =========================================================
    # Public API
    # =========================================================

    def optimize(
        self,
        context: GenerationContext,
    ) -> GenerationContext:
        """
        Optimize generation context.

        Args:
            context:
                Original generation context.

        Returns:
            Optimized generation context.
        """

        relevant_files = (
            self._select_files(
                context
            )
        )

        return context.model_copy(
            update={
                "target_files": relevant_files,
                "metadata": {
                    **context.metadata,
                    "optimized": True,
                    "original_file_count": len(
                        context.repository.repository_files
                    ),
                    "optimized_file_count": len(
                        relevant_files
                    ),
                },
            }
        )

    # =========================================================
    # Helpers
    # =========================================================

    def _select_files(
        self,
        context: GenerationContext,
    ) -> list[str]:
        """
        Select most relevant files.

        Priority:
            1. Task relevant files
            2. Project relevant files
            3. Repository files
        """

        candidates = []

        candidates.extend(
            context.task.relevant_files
        )

        candidates.extend(
            context.project.relevant_files
        )

        candidates.extend(
            context.repository.repository_files
        )

        unique_files = {
            file.strip()
            for file in candidates
            if file.strip()
        }

        return sorted(
            unique_files
        )[: self.max_files]
        