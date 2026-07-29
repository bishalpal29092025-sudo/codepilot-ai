"""
Plan validation.

Validates ProjectPlan instances before they are passed to downstream
components such as the generation and execution engines.
"""

from __future__ import annotations

from core.models import ProjectPlan

from .exceptions import PlanningValidationError


class PlanValidator:
    """
    Validates implementation plans.

    The validator performs structural validation only.
    It never modifies a plan.
    """

    def validate(
        self,
        plan: ProjectPlan,
    ) -> ProjectPlan:
        """
        Validate a project plan.

        Parameters
        ----------
        plan:
            Project plan to validate.

        Returns
        -------
        ProjectPlan

        Raises
        ------
        PlanningValidationError
        """

        self._validate_summary(plan)
        self._validate_tasks(plan)
        self._validate_risks(plan)
        self._validate_testing(plan)

        return plan

    def _validate_summary(
        self,
        plan: ProjectPlan,
    ) -> None:
        if not plan.summary.strip():
            raise PlanningValidationError(
                "Project plan summary cannot be empty."
            )

    def _validate_tasks(
        self,
        plan: ProjectPlan,
    ) -> None:
        if not plan.tasks:
            raise PlanningValidationError(
                "Project plan must contain at least one task."
            )

        ids = set()

        for task in plan.tasks:

            if task.id in ids:
                raise PlanningValidationError(
                    f"Duplicate task id: {task.id}"
                )

            ids.add(task.id)

            if not task.title.strip():
                raise PlanningValidationError(
                    f"Task '{task.id}' has an empty title."
                )

    def _validate_risks(
        self,
        plan: ProjectPlan,
    ) -> None:
        for risk in plan.risks:

            if not risk.title.strip():
                raise PlanningValidationError(
                    "Risk title cannot be empty."
                )

    def _validate_testing(
        self,
        plan: ProjectPlan,
    ) -> None:
        if not plan.testing:
            raise PlanningValidationError(
                "Testing checklist cannot be empty."
            )