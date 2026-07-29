"""
Planning explorer.

Public entry point for the planning package.
"""

from __future__ import annotations

from core.models import (
    ProjectPlan,
    ProjectRequest,
    RepositoryInfo,
)

from .analyzer import PlanningAnalyzer
from .planner import ProjectPlanner
from .validator import PlanValidator


class PlanningExplorer:
    """
    High-level planning workflow.

    Coordinates analysis, planning and validation.
    """

    def __init__(self) -> None:
        self._analyzer = PlanningAnalyzer()
        self._planner = ProjectPlanner()
        self._validator = PlanValidator()

    def plan(
        self,
        repository: RepositoryInfo,
        request: ProjectRequest,
    ) -> ProjectPlan:
        """
        Generate a validated project plan.
        """

        analysis = self._analyzer.analyze(
            repository,
            request,
        )

        plan = self._planner.create_plan(
            analysis,
        )

        return self._validator.validate(
            plan,
        )