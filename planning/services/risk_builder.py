"""
Risk builder service.

Builds structured implementation risks from project analysis.

The builder converts planning assumptions and repository characteristics
into Risk models that can be consumed by the planning, verification,
execution and reporting packages.
"""

from __future__ import annotations

from core.models import (
    ProjectAnalysis,
    Risk,
    Severity,
)


class RiskBuilder:
    """
    Builds implementation risks from a project analysis.
    """

    def build(
        self,
        analysis: ProjectAnalysis,
    ) -> list[Risk]:
        """
        Build implementation risks.

        Parameters
        ----------
        analysis:
            Project analysis.

        Returns
        -------
        list[Risk]
        """

        risks: list[Risk] = []

        risks.extend(
            self._build_assumption_risks(
                analysis,
            )
        )

        risks.extend(
            self._build_file_impact_risks(
                analysis,
            )
        )

        risks.extend(
            self._build_project_risks(
                analysis,
            )
        )

        return risks

    # ------------------------------------------------------------------ #
    # Assumptions
    # ------------------------------------------------------------------ #

    def _build_assumption_risks(
        self,
        analysis: ProjectAnalysis,
    ) -> list[Risk]:

        risks: list[Risk] = []

        for assumption in analysis.assumptions:
            risks.append(
                Risk(
                    title="Planning Assumption",
                    description=assumption,
                    severity=Severity.MEDIUM,
                    mitigation=(
                        "Validate this assumption before implementation."
                    ),
                )
            )

        return risks

    # ------------------------------------------------------------------ #
    # File Impact
    # ------------------------------------------------------------------ #

    def _build_file_impact_risks(
        self,
        analysis: ProjectAnalysis,
    ) -> list[Risk]:

        file_count = len(
            analysis.affected_files,
        )

        if file_count < 10:
            return []

        return [
            Risk(
                title="Large Change Surface",
                description=(
                    f"{file_count} files may require modification."
                ),
                severity=Severity.HIGH,
                mitigation=(
                    "Implement changes incrementally and validate each step."
                ),
            )
        ]

    # ------------------------------------------------------------------ #
    # Project Risks
    # ------------------------------------------------------------------ #

    def _build_project_risks(
        self,
        analysis: ProjectAnalysis,
    ) -> list[Risk]:

        project = analysis.project_type.lower()

        risks: list[Risk] = []

        if "microservice" in project:
            risks.append(
                Risk(
                    title="Distributed System Complexity",
                    description=(
                        "Changes may affect multiple services."
                    ),
                    severity=Severity.HIGH,
                    mitigation=(
                        "Validate service contracts before deployment."
                    ),
                )
            )

        if "full stack" in project:
            risks.append(
                Risk(
                    title="Cross-Layer Changes",
                    description=(
                        "Frontend and backend may require coordinated updates."
                    ),
                    severity=Severity.MEDIUM,
                    mitigation=(
                        "Implement backend changes before frontend integration."
                    ),
                )
            )

        if "rest api" in project:
            risks.append(
                Risk(
                    title="API Compatibility",
                    description=(
                        "Changes may impact existing API consumers."
                    ),
                    severity=Severity.MEDIUM,
                    mitigation=(
                        "Maintain backward compatibility whenever possible."
                    ),
                )
            )

        return risks