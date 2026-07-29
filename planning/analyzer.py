"""
Planning analyzer.

Coordinates the planning analysis pipeline by combining multiple specialised
analysers into a single ProjectAnalysis.
"""

from __future__ import annotations

from core.models import (
    ProjectAnalysis,
    ProjectRequest,
    RepositoryInfo,
)

from .analysis.feature import FeatureAnalyzer
from .analysis.impact import ImpactAnalyzer
from .analysis.project import ProjectAnalyzer


class PlanningAnalyzer:
    """
    Coordinates the planning analysis pipeline.

    The analyzer itself contains no business logic. Instead, it delegates
    responsibility to specialised analysers.
    """

    def __init__(self) -> None:
        self._project_analyzer = ProjectAnalyzer()
        self._feature_analyzer = FeatureAnalyzer()
        self._impact_analyzer = ImpactAnalyzer()

    def analyze(
        self,
        repository: RepositoryInfo,
        request: ProjectRequest,
    ) -> ProjectAnalysis:
        """
        Analyse a repository and engineering request.

        Parameters
        ----------
        repository:
            Repository metadata.

        request:
            User engineering request.

        Returns
        -------
        ProjectAnalysis
        """

        analysis = self._project_analyzer.analyze(
            repository,
        )

        analysis = self._feature_analyzer.analyze(
            repository,
            analysis,
        )

        analysis = self._impact_analyzer.analyze(
            repository,
            request,
            analysis,
        )

        return analysis