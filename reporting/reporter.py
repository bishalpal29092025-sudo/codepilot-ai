"""
Reporting Engine.

Creates final engineering reports
from CodePilot pipeline results.
"""

from __future__ import annotations

from core.context import AgentContext
from core.models import EngineeringReport, Summary


class Reporter:
    """
    Generates final pipeline reports.
    """

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Generate final engineering report.
        """

        self._print_header()

        summary = Summary(
            files_changed=[],
            features_added=[],
            testing=self._collect_tests(context),
            notes=self._collect_notes(context),
        )

        report = EngineeringReport(
            dependency=context.dependency_report,
            build=context.build_result,
            runtime=context.runtime_result,
            api=context.api_test_result,
            root_cause=context.root_cause,
            summary=summary,
        )

        context.engineering_report = report

        self._print_summary(
            report
        )

        return context


    # ==========================================================
    # Helpers
    # ==========================================================

    def _collect_tests(
        self,
        context: AgentContext,
    ) -> list[str]:

        tests = []

        if context.build_result:
            tests.append(
                "Build validation executed."
            )

        if context.runtime_result:
            tests.append(
                "Runtime validation executed."
            )

        if context.api_test_result:
            tests.append(
                "API validation executed."
            )

        return tests


    def _collect_notes(
        self,
        context: AgentContext,
    ) -> list[str]:

        notes = []

        if context.execution_result:
            notes.append(
                "Execution completed."
            )

        if context.root_cause:
            notes.append(
                "Root cause analysis completed."
            )

        return notes


    # ==========================================================
    # Console
    # ==========================================================

    def _print_header(self):

        print("\n" + "=" * 70)
        print("📊 Reporting Engine")
        print("=" * 70)


    def _print_summary(
        self,
        report: EngineeringReport,
    ):

        print(
            f"Build Available : {report.build is not None}"
        )

        print(
            f"Runtime Available : {report.runtime is not None}"
        )

        print(
            f"Summary Created : {report.summary is not None}"
        )