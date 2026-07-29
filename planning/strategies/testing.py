"""
Rule-based testing strategy.

Builds the testing checklist for a project plan.

The strategy combines the default testing checklist with
category-specific validation steps.
"""

from __future__ import annotations

from core.models import TaskCategory

from planning.constants import (
    CATEGORY_ACCEPTANCE_CRITERIA,
    DEFAULT_TESTING_CHECKLIST,
)

from .base import Strategy


class RuleBasedTestingStrategy(Strategy):
    """
    Rule-based strategy for building testing checklists.
    """

    def build(
        self,
        categories: list[TaskCategory],
    ) -> list[str]:
        """
        Build a testing checklist.

        Parameters
        ----------
        categories:
            Categories included in the implementation plan.

        Returns
        -------
        list[str]
            Testing checklist.
        """

        checklist = list(DEFAULT_TESTING_CHECKLIST)

        seen = set(checklist)

        for category in categories:
            for item in CATEGORY_ACCEPTANCE_CRITERIA.get(category, ()):
                if item not in seen:
                    checklist.append(item)
                    seen.add(item)

        return checklist