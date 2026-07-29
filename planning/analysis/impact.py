"""
Impact analysis.

Responsible for determining which parts of a project are likely to be
affected by an engineering request.
"""

from __future__ import annotations

from core.models import (
    ProjectAnalysis,
    ProjectRequest,
    RepositoryInfo,
)


class ImpactAnalyzer:
    """
    Analyses the potential impact of a user's engineering request.

    This analyser identifies:

    - Missing features
    - Affected files
    - Planning assumptions

    It does NOT create implementation tasks.
    """

    def analyze(
        self,
        repository: RepositoryInfo,
        request: ProjectRequest,
        analysis: ProjectAnalysis,
    ) -> ProjectAnalysis:
        """
        Update the project analysis with impact information.

        Parameters
        ----------
        repository:
            Repository metadata.

        request:
            User engineering request.

        analysis:
            Existing project analysis.

        Returns
        -------
        ProjectAnalysis
        """

        goal = request.goal.lower()

        self._analyse_authentication(goal, analysis)
        self._analyse_database(goal, analysis)
        self._analyse_api(goal, analysis)

        return analysis

    def _analyse_authentication(
        self,
        goal: str,
        analysis: ProjectAnalysis,
    ) -> None:
        """
        Analyse authentication-related requests.
        """

        if "jwt" in goal or "authentication" in goal:

            analysis.missing_features.append(
                "JWT Authentication"
            )

            analysis.affected_files.extend(
                [
                    "app.py",
                    "auth.py",
                    "routes.py",
                    "config.py",
                ]
            )

            analysis.assumptions.append(
                "Authentication flow may require updates."
            )

    def _analyse_database(
        self,
        goal: str,
        analysis: ProjectAnalysis,
    ) -> None:
        """
        Analyse database-related requests.
        """

        if "database" in goal:

            analysis.missing_features.append(
                "Database Changes"
            )

            analysis.affected_files.extend(
                [
                    "models.py",
                    "database.py",
                ]
            )

    def _analyse_api(
        self,
        goal: str,
        analysis: ProjectAnalysis,
    ) -> None:
        """
        Analyse API-related requests.
        """

        if "api" in goal:

            analysis.assumptions.append(
                "Existing API contracts should remain compatible."
            )

            analysis.affected_files.extend(
                [
                    "routes.py",
                    "api.py",
                ]
            )

        #
        # Remove duplicates
        #

        analysis.missing_features = sorted(
            set(analysis.missing_features)
        )

        analysis.affected_files = sorted(
            set(analysis.affected_files)
        )

        analysis.assumptions = sorted(
            set(analysis.assumptions)
        )