"""
Rule-based summary strategy.

Builds a human-readable implementation summary for a project analysis.

The strategy delegates summary generation to the SummaryBuilder service
while exposing a consistent interface for the planner.
"""

from __future__ import annotations

from core.models import ProjectAnalysis

from planning.services.summary_builder import SummaryBuilder

from .base import Strategy


class RuleBasedSummaryStrategy(Strategy):
    """
    Rule-based strategy for building implementation summaries.
    """

    def __init__(
        self,
        builder: SummaryBuilder | None = None,
    ) -> None:
        self._builder = builder or SummaryBuilder()

    def build(
        self,
        analysis: ProjectAnalysis,
    ) -> str:
        """
        Build an implementation summary.

        Parameters
        ----------
        analysis:
            Repository analysis.

        Returns
        -------
        str
            Human-readable implementation summary.
        """

        return self._builder.build(analysis)