"""
Complexity estimation service.

Provides engineering complexity estimation for implementation tasks.

The estimator is intentionally deterministic and rule-based. It can later be
replaced or extended with AI-powered estimation without changing the planning
strategies that depend on it.
"""

from __future__ import annotations

from core.models import (
    Complexity,
    ProjectAnalysis,
)

from .keyword_matcher import KeywordMatcher


class ComplexityEstimator:
    """
    Estimates implementation complexity.
    """

    def __init__(
        self,
        matcher: KeywordMatcher | None = None,
    ) -> None:
        self._matcher = matcher or KeywordMatcher()

    def estimate(
        self,
        feature: str,
        analysis: ProjectAnalysis,
    ) -> Complexity:
        """
        Estimate implementation complexity.

        Parameters
        ----------
        feature:
            Feature currently being planned.

        analysis:
            Repository analysis.

        Returns
        -------
        Complexity
        """

        score = 0

        score += self._feature_score(feature)
        score += self._project_score(analysis)
        score += self._file_score(analysis)

        return self._score_to_complexity(score)

    # ------------------------------------------------------------------ #
    # Feature Scoring
    # ------------------------------------------------------------------ #

    def _feature_score(
        self,
        feature: str,
    ) -> int:

        feature = feature.lower()

        if self._matcher.contains_any(
            feature,
            (
                "authentication",
                "authorization",
                "oauth",
                "jwt",
                "payment",
                "microservice",
                "distributed",
            ),
        ):
            return 5

        if self._matcher.contains_any(
            feature,
            (
                "database",
                "migration",
                "docker",
                "api",
                "security",
            ),
        ):
            return 4

        if self._matcher.contains_any(
            feature,
            (
                "frontend",
                "ui",
                "component",
                "dashboard",
            ),
        ):
            return 3

        if self._matcher.contains_any(
            feature,
            (
                "documentation",
                "readme",
                "comment",
            ),
        ):
            return 1

        return 2

    # ------------------------------------------------------------------ #
    # Project Scoring
    # ------------------------------------------------------------------ #

    def _project_score(
        self,
        analysis: ProjectAnalysis,
    ) -> int:

        project = analysis.project_type.lower()

        if "microservice" in project:
            return 3

        if "full stack" in project:
            return 2

        if "rest api" in project:
            return 2

        if "frontend" in project:
            return 1

        return 0

    # ------------------------------------------------------------------ #
    # File Impact Scoring
    # ------------------------------------------------------------------ #

    def _file_score(
        self,
        analysis: ProjectAnalysis,
    ) -> int:

        file_count = len(analysis.affected_files)

        if file_count >= 15:
            return 4

        if file_count >= 10:
            return 3

        if file_count >= 5:
            return 2

        if file_count >= 2:
            return 1

        return 0

    # ------------------------------------------------------------------ #
    # Final Mapping
    # ------------------------------------------------------------------ #

    @staticmethod
    def _score_to_complexity(
        score: int,
    ) -> Complexity:

        if score >= 10:
            return Complexity.VERY_HIGH

        if score >= 7:
            return Complexity.HIGH

        if score >= 4:
            return Complexity.MEDIUM

        return Complexity.LOW