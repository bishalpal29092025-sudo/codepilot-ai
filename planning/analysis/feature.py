"""
Feature analysis.

Responsible for identifying the features already implemented
within a repository.
"""

from __future__ import annotations

from core.models import (
    ProjectAnalysis,
    RepositoryInfo,
)


class FeatureAnalyzer:
    """
    Analyses repository metadata to identify existing features.

    This analyser only identifies implemented functionality.
    It never creates implementation plans.
    """

    def analyze(
        self,
        repository: RepositoryInfo,
        analysis: ProjectAnalysis,
    ) -> ProjectAnalysis:
        """
        Populate the existing_features field of a ProjectAnalysis.

        Parameters
        ----------
        repository:
            Repository metadata.

        analysis:
            Existing project analysis.

        Returns
        -------
        ProjectAnalysis
        """

        features: list[str] = []

        framework = (repository.framework or "").lower()

        if framework in {"flask", "fastapi", "django"}:
            features.append("REST API")

        if framework == "next.js":
            features.extend(
                [
                    "Server Side Rendering",
                    "Routing",
                ]
            )

        if framework == "react":
            features.extend(
                [
                    "Component-Based UI",
                    "Client-Side Rendering",
                ]
            )

        database = (repository.database or "").lower()

        if database:
            features.append("Database Integration")

        if repository.package_manager:
            features.append("Package Management")

        analysis.existing_features.extend(
            sorted(set(features))
        )

        return analysis