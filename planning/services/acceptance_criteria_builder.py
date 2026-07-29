"""
Acceptance criteria builder service.

Builds acceptance criteria for engineering tasks.

Acceptance criteria define the expected outcome of a task and act as the
contract between the planning, generation, verification and reporting
packages.
"""

from __future__ import annotations

from core.models import TaskCategory


class AcceptanceCriteriaBuilder:
    """
    Builds acceptance criteria for engineering tasks.
    """

    def build(
        self,
        feature: str,
        category: TaskCategory,
    ) -> list[str]:
        """
        Build acceptance criteria.

        Parameters
        ----------
        feature:
            Feature being implemented.

        category:
            Task category.

        Returns
        -------
        list[str]
        """

        criteria = [
            f"{feature} is fully implemented.",
            "The project builds successfully.",
            "Existing functionality remains unaffected.",
        ]

        criteria.extend(
            self._category_specific_criteria(category)
        )

        return criteria

    # ------------------------------------------------------------------ #
    # Private Helpers
    # ------------------------------------------------------------------ #

    def _category_specific_criteria(
        self,
        category: TaskCategory,
    ) -> list[str]:

        if category is TaskCategory.DEPENDENCY:
            return [
                "Required dependency is installed.",
                "Dependency is correctly configured.",
            ]

        if category is TaskCategory.CONFIGURATION:
            return [
                "Configuration is validated.",
                "Application starts successfully.",
            ]

        if category is TaskCategory.IMPLEMENTATION:
            return [
                "Implementation satisfies the requested behaviour.",
                "Public interfaces remain consistent.",
            ]

        if category is TaskCategory.REFACTOR:
            return [
                "Behaviour remains unchanged.",
                "Code quality is improved.",
            ]

        if category is TaskCategory.TESTING:
            return [
                "All new tests pass.",
                "Existing tests continue to pass.",
            ]

        if category is TaskCategory.DOCUMENTATION:
            return [
                "Documentation is accurate.",
                "Documentation reflects implementation.",
            ]

        return []