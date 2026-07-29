"""
Summary builder service.

Builds human-readable implementation summaries from project analysis.

The summary is intended for developers, reports, pull requests and future
AI reasoning. The builder contains no planning logic; it only transforms
analysis data into concise summaries.
"""

from __future__ import annotations

from core.models import (
    Complexity,
    ProjectAnalysis,
)

from .complexity_estimator import ComplexityEstimator


class SummaryBuilder:
    """
    Builds implementation summaries.
    """

    def __init__(
        self,
        complexity_estimator: ComplexityEstimator | None = None,
    ) -> None:
        self._complexity_estimator = (
            complexity_estimator or ComplexityEstimator()
        )

    def build(
        self,
        analysis: ProjectAnalysis,
    ) -> str:
        """
        Build an implementation summary.

        Parameters
        ----------
        analysis:
            Repository analysis.

        Returns
        -------
        str
        """

        feature_count = len(analysis.missing_features)
        affected_files = len(analysis.affected_files)

        highest_complexity = self._highest_complexity(analysis)

        project = analysis.project_type

        return (
            f"{project}: "
            f"{feature_count} planned feature(s), "
            f"{affected_files} affected file(s), "
            f"estimated overall complexity: "
            f"{highest_complexity.value.replace('_', ' ')}."
        )

    # ------------------------------------------------------------------ #
    # Private Helpers
    # ------------------------------------------------------------------ #

    def _highest_complexity(
        self,
        analysis: ProjectAnalysis,
    ) -> Complexity:
        """
        Determine the highest complexity among all planned features.
        """

        if not analysis.missing_features:
            return Complexity.LOW

        complexities = [
            self._complexity_estimator.estimate(
                feature,
                analysis,
            )
            for feature in analysis.missing_features
        ]

        order = {
            Complexity.LOW: 1,
            Complexity.MEDIUM: 2,
            Complexity.HIGH: 3,
            Complexity.VERY_HIGH: 4,
        }

        return max(
            complexities,
            key=lambda complexity: order[complexity],
        )