"""
Prompt generation strategy.

Selects prompt style based on task category.
"""

from __future__ import annotations

from core.models.planning import TaskCategory

from .base import BaseStrategy


class PromptStrategy(BaseStrategy):
    """
    Determines prompt instructions based on task type.
    """

    def execute(
        self,
        category: TaskCategory,
    ) -> str:
        """
        Return prompt instructions.
        """

        match category:

            case TaskCategory.IMPLEMENTATION:
                return (
                    "Implement the requested feature "
                    "following existing architecture."
                )

            case TaskCategory.REFACTOR:
                return (
                    "Refactor existing code while "
                    "preserving behaviour."
                )

            case TaskCategory.TESTING:
                return (
                    "Create comprehensive tests "
                    "for the requested functionality."
                )

            case TaskCategory.CONFIGURATION:
                return (
                    "Update configuration safely "
                    "following project conventions."
                )

            case TaskCategory.DOCUMENTATION:
                return (
                    "Create clear technical documentation."
                )

            case TaskCategory.DEPENDENCY:
                return (
                    "Handle dependency changes carefully."
                )

            case _:
                return (
                    "Complete the requested engineering task."
                )