"""
Project planner.

Coordinates planning services and strategies to transform a ProjectAnalysis
into a ProjectPlan.

The planner contains no business logic. All engineering intelligence is
delegated to services and strategies.
"""

from __future__ import annotations

from core.models import (
    ProjectAnalysis,
    ProjectPlan,
)

from planning.services.task_builder import TaskBuilder
from planning.strategies.risk import RuleBasedRiskStrategy
from planning.strategies.summary import RuleBasedSummaryStrategy
from planning.strategies.testing import RuleBasedTestingStrategy


class ProjectPlanner:
    """
    Orchestrates the planning process.
    """

    def __init__(
        self,
        task_builder: TaskBuilder | None = None,
        summary_strategy: RuleBasedSummaryStrategy | None = None,
        risk_strategy: RuleBasedRiskStrategy | None = None,
        testing_strategy: RuleBasedTestingStrategy | None = None,
    ) -> None:
        self._task_builder = task_builder or TaskBuilder()
        self._summary_strategy = (
            summary_strategy or RuleBasedSummaryStrategy()
        )
        self._risk_strategy = (
            risk_strategy or RuleBasedRiskStrategy()
        )
        self._testing_strategy = (
            testing_strategy or RuleBasedTestingStrategy()
        )

    def create_plan(
        self,
        analysis: ProjectAnalysis,
    ) -> ProjectPlan:
        """
        Create a project implementation plan.

        Parameters
        ----------
        analysis:
            Repository analysis.

        Returns
        -------
        ProjectPlan
        """

        summary = self._summary_strategy.build(
            analysis,
        )

        tasks = [
            self._task_builder.build(
                feature,
                analysis,
            )
            for feature in analysis.missing_features
        ]

        categories = [
            task.category
            for task in tasks
        ]

        risks = self._risk_strategy.build(
            analysis,
        )

        testing = self._testing_strategy.build(
            categories,
        )

        return ProjectPlan(
            summary=summary,
            tasks=tasks,
            risks=risks,
            testing_checklist=testing,
        )