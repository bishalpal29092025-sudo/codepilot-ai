"""
Rule-based task category strategy.

Determines the most appropriate task category for a requested feature.

The strategy uses configurable keyword rules and delegates text matching
to the KeywordMatcher service.
"""

from __future__ import annotations

from core.models import TaskCategory

from planning.constants import CATEGORY_KEYWORDS
from planning.services.keyword_matcher import KeywordMatcher

from .base import Strategy


class RuleBasedCategoryStrategy(Strategy):
    """
    Rule-based strategy for determining task categories.
    """

    def __init__(
        self,
        matcher: KeywordMatcher | None = None,
    ) -> None:
        self._matcher = matcher or KeywordMatcher()

    def determine(
        self,
        feature: str,
    ) -> TaskCategory:
        """
        Determine the category for a feature.

        Parameters
        ----------
        feature:
            Feature request.

        Returns
        -------
        TaskCategory
            The detected task category.
        """

        normalized_feature = feature.strip().lower()

        for category, keywords in CATEGORY_KEYWORDS.items():
            if self._matcher.contains_any(
                normalized_feature,
                keywords,
            ):
                return category

        return TaskCategory.IMPLEMENTATION