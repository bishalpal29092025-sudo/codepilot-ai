"""
CodePilot Pipeline Controller.

Controls execution order of all
AI coding agent stages.
"""

from __future__ import annotations

from core.context import AgentContext


class Pipeline:
    """
    Executes CodePilot workflow.
    """


    def __init__(
        self,
        stages: list,
    ) -> None:

        self.stages = stages


    # ==========================================================
    # Public API
    # ==========================================================

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Execute all pipeline stages.
        """

        self._print_header()


        for name, stage in self.stages:

            print(
                f"\n▶ Running Stage: {name}"
            )


            context = stage.run(
                context
            )


        self._print_footer()


        return context


    # ==========================================================
    # Console
    # ==========================================================

    def _print_header(self):

        print("\n")
        print("=" * 70)
        print("🤖 CodePilot Agent Pipeline")
        print("=" * 70)


    def _print_footer(self):

        print("\n")
        print("=" * 70)
        print("✅ Pipeline Completed")
        print("=" * 70)