"""
Project analysis.

Responsible for identifying the overall characteristics of a repository.
"""

from __future__ import annotations

from core.models import (
    ProjectAnalysis,
    RepositoryInfo,
)


class ProjectAnalyzer:
    """
    Analyses a repository and determines its high-level characteristics.

    This analyser focuses only on understanding the project itself.
    """

    def analyze(
        self,
        repository: RepositoryInfo,
    ) -> ProjectAnalysis:
        """
        Analyse a repository.

        Parameters
        ----------
        repository:
            Repository metadata.

        Returns
        -------
        ProjectAnalysis
        """

        project_type = self._detect_project_type(repository)

        analysis = ProjectAnalysis(
            project_type=project_type,
        )

        analysis.assumptions.append(
            f"Detected framework: {repository.framework or 'Unknown'}"
        )

        return analysis

    def _detect_project_type(
        self,
        repository: RepositoryInfo,
    ) -> str:
        """
        Determine the project type from repository metadata.
        """

        framework = (repository.framework or "").lower()

        if framework == "fastapi":
            return "REST API"

        if framework == "flask":
            return "REST API"

        if framework == "django":
            return "Web Application"

        if framework == "next.js":
            return "Full Stack Web Application"

        if framework == "react":
            return "Frontend Application"

        language = (repository.language or "").lower()

        if language == "python":
            return "Python Application"

        if language == "typescript":
            return "TypeScript Application"

        if language == "javascript":
            return "JavaScript Application"

        return "Unknown"