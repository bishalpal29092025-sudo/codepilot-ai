"""
File selector service.

Selects repository files relevant to the current
generation task.
"""

from __future__ import annotations

from core.models.generation import GenerationContext


class FileSelector:
    """
    Selects files required for code generation.
    """

    def __init__(
        self,
        max_files: int = 25,
    ) -> None:
        """
        Initialize selector.

        Args:
            max_files:
                Maximum files returned.
        """

        self.max_files = max_files

    # =========================================================
    # Public API
    # =========================================================

    def select(
        self,
        context: GenerationContext,
    ) -> list[str]:
        """
        Select relevant repository files.

        Priority:

        1. Task relevant files
        2. Project relevant files
        3. Repository files

        Args:
            context:
                Generation context.

        Returns:
            Selected file paths.
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

        return self._normalize(
            candidates
        )[: self.max_files]

    # =========================================================
    # Helpers
    # =========================================================

    @staticmethod
    def _normalize(
        files: list[str],
    ) -> list[str]:
        """
        Normalize file paths.

        Operations:

        - remove empty paths
        - trim whitespace
        - remove duplicates
        - sort
        """

        return sorted(
            {
                file.strip()
                for file in files
                if file.strip()
            }
        )