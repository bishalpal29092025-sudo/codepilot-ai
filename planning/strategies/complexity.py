"""
Rule-based complexity strategy.

Determines the implementation complexity for a requested feature.

The strategy delegates complexity estimation to the ComplexityEstimator
service while exposing a consistent strategy interface for the planner.
"""

from __future__ import annotations

from core.models import (
    Complexity,
    ProjectAnalysis,
)

from planning.services.complexity_estimator import ComplexityEstimator

from .base import Strategy


class RuleBasedComplexityStrategy(Strategy):
    """
    Rule-based strategy for estimating implementation complexity.
    """

    def __init__(
        self,
        estimator: ComplexityEstimator | None = None,
    ) -> None:
        self._estimator = estimator or ComplexityEstimator()

    def determine(
        self,
        feature: str,
        analysis: ProjectAnalysis,
    ) -> Complexity:
        """
        Determine the implementation complexity for a feature.

        Parameters
        ----------
        feature:
            Feature to be implemented.

        analysis:
            Repository analysis.

        Returns
        -------
        Complexity
            Estimated implementation complexity.
        """

        return self._estimator.estimate(
            feature=feature,
            analysis=analysis,
        )