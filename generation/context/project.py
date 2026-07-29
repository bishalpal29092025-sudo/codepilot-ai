"""
Project context builder.

Transforms a ProjectPlan domain model into a Generation
ProjectContext.

This layer only maps planning output into generation input.
It does not perform analysis, planning, or generation logic.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from core.models.generation import ProjectContext
from core.models.planning import ProjectPlan


class ProjectContextBuilder:
    """
    Builds immutable ProjectContext objects from ProjectPlan.

    Responsibilities:
        - Normalize project information
        - Preserve planning metadata
        - Prepare generation-ready context

    Does NOT:
        - Create plans
        - Analyze repositories
        - Generate code
    """

    def build(
        self,
        project: ProjectPlan,
    ) -> ProjectContext:
        """
        Convert ProjectPlan into ProjectContext.

        Args:
            project:
                Immutable planning output.

        Returns:
            Generation-ready ProjectContext.
        """

        return ProjectContext(
            name=project.name,
            summary=project.summary,
            objective=project.objective,
            architecture=project.architecture,
            coding_standards=self._normalize(
                project.coding_standards
            ),
            constraints=self._normalize(
                project.constraints
            ),
            assumptions=self._normalize(
                project.assumptions
            ),
            relevant_files=self._normalize(
                project.relevant_files
            ),
            metadata=self._build_metadata(project),
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
        project: ProjectPlan,
    ) -> dict[str, Any]:
        """
        Build generation metadata from planning data.
        """

        metadata = deepcopy(
            project.metadata
        )

        metadata.update(
            {
                "task_count": len(
                    project.tasks
                ),
                "risk_count": len(
                    project.risks
                ),
                "testing_item_count": len(
                    project.testing
                ),
                "relevant_file_count": len(
                    project.relevant_files
                ),
                "constraint_count": len(
                    project.constraints
                ),
                "assumption_count": len(
                    project.assumptions
                ),
            }
        )

        return metadata