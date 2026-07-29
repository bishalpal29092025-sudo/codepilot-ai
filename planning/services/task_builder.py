"""
Task builder service.

Builds Task models from project analysis.

The builder coordinates the category strategy, complexity strategy and
acceptance criteria builder to produce complete engineering tasks.

This service contains no planning orchestration logic; it is solely
responsible for constructing Task objects.
"""

from __future__ import annotations

from itertools import count

from core.models import (
    Priority,
    ProjectAnalysis,
    Task,
)

from planning.constants import DEFAULT_PRIORITY
from planning.services.acceptance_criteria_builder import (
    AcceptanceCriteriaBuilder,
)
from planning.strategies.category import RuleBasedCategoryStrategy
from planning.strategies.complexity import (
    RuleBasedComplexityStrategy,
)


class TaskBuilder:
    """
    Builds Task models for implementation features.
    """

    def __init__(
        self,
        category_strategy: RuleBasedCategoryStrategy | None = None,
        complexity_strategy: RuleBasedComplexityStrategy | None = None,
        acceptance_builder: AcceptanceCriteriaBuilder | None = None,
    ) -> None:
        self._category_strategy = (
            category_strategy or RuleBasedCategoryStrategy()
        )
        self._complexity_strategy = (
            complexity_strategy or RuleBasedComplexityStrategy()
        )
        self._acceptance_builder = (
            acceptance_builder or AcceptanceCriteriaBuilder()
        )

        self._counter = count(1)

    def build(
        self,
        feature: str,
        analysis: ProjectAnalysis,
    ) -> Task:
        """
        Build a Task from a requested feature.

        Parameters
        ----------
        feature:
            Requested implementation feature.

        analysis:
            Repository analysis.

        Returns
        -------
        Task
        """

        category = self._category_strategy.determine(
            feature,
        )

        complexity = self._complexity_strategy.determine(
            feature,
            analysis,
        )

        acceptance_criteria = self._acceptance_builder.build(
            feature,
            category,
        )

        task_id = f"TASK-{next(self._counter):03}"

        return Task(
            id=task_id,
            title=feature,
            description=self._build_description(feature),
            category=category,
            priority=self._determine_priority(complexity),
            complexity=complexity,
            affected_files=analysis.affected_files,
            dependencies=[],
            acceptance_criteria=acceptance_criteria,
        )

    @staticmethod
    def _build_description(
        feature: str,
    ) -> str:
        """
        Build a task description.
        """

        return (
            f"Implement the requested feature: '{feature}'. "
            "Ensure the implementation integrates with the existing "
            "project architecture and follows established coding standards."
        )

    @staticmethod
    def _determine_priority(
        complexity,
    ) -> Priority:
        """
        Determine task priority from complexity.
        """

        priority_map = {
            "LOW": Priority.LOW,
            "MEDIUM": Priority.MEDIUM,
            "HIGH": Priority.HIGH,
            "VERY_HIGH": Priority.CRITICAL,
        }

        return priority_map.get(
            complexity.name,
            DEFAULT_PRIORITY,
        )