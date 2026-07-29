"""
Rule-based risk strategy.

Builds implementation risks for a project analysis.

The strategy delegates risk construction to the RiskBuilder service while
providing a consistent interface for the planner.
"""

from __future__ import annotations

from core.models import (
    ProjectAnalysis,
    Risk,
)

from planning.services.risk_builder import RiskBuilder

from .base import Strategy


class RuleBasedRiskStrategy(Strategy):
    """
    Rule-based strategy for generating implementation risks.
    """

    def __init__(
        self,
        builder: RiskBuilder | None = None,
    ) -> None:
        self._builder = builder or RiskBuilder()

    def build(
        self,
        analysis: ProjectAnalysis,
    ) -> list[Risk]:
        """
        Build implementation risks.

        Parameters
        ----------
        analysis:
            Repository analysis.

        Returns
        -------
        list[Risk]
            Generated implementation risks.
        """

        return self._builder.build(analysis)