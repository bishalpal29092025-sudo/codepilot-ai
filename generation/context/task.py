"""
Task context builder.

Transforms a Planning Task model into a Generation
TaskContext model.

This builder only performs data transformation.
It does not analyze tasks, estimate complexity,
or modify planning output.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from core.models.generation import TaskContext
from core.models.planning import Task


class TaskContextBuilder:
    """
    Builds immutable TaskContext objects from planning Task models.
    """

    def build(
        self,
        task: Task,
    ) -> TaskContext:
        """
        Convert Task into TaskContext.

        Args:
            task:
                Planning stage task.

        Returns:
            Generation-ready TaskContext.
        """

        return TaskContext(
            id=task.id,
            title=task.title,
            description=task.description,
            priority=task.priority.value,
            complexity=task.complexity.value,
            acceptance_criteria=self._normalize(
                task.acceptance_criteria
            ),
            dependencies=self._normalize(
                task.dependencies
            ),
            relevant_files=self._normalize(
                task.affected_files
            ),
            metadata=self._build_metadata(task),
        )

    # =========================================================
    # Helpers
    # =========================================================

    @staticmethod
    def _normalize(
        values: list[str],
    ) -> list[str]:
        """
        Normalize string collections.

        Operations:
            - Remove empty values
            - Strip whitespace
            - Remove duplicates
            - Sort values
        """

        return sorted(
            {
                value.strip()
                for value in values
                if value.strip()
            }
        )

    @staticmethod
    def _build_metadata(
        task: Task,
    ) -> dict[str, Any]:
        """
        Build generation metadata from planning task.
        """

        metadata = {}

        metadata.update(
            {
                "category": task.category.value,
                "dependency_count": len(
                    task.dependencies
                ),
                "affected_file_count": len(
                    task.affected_files
                ),
                "acceptance_criteria_count": len(
                    task.acceptance_criteria
                ),
            }
        )

        return metadata