"""
Root Cause Analyzer.

Analyzes verification failures and provides
possible causes and recommended solutions.
"""

from __future__ import annotations

from core.context import AgentContext
from core.models import RootCause


class RootCauseAnalyzer:
    """
    Analyzes failures detected during verification.
    """

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Analyze available verification results.
        """

        self._print_header()

        analysis = RootCause(
            summary="",
            probable_causes=[],
            suggested_fixes=[],
            confidence=0.0,
        )

        self._analyze_build_failure(
            context,
            analysis,
        )

        self._analyze_runtime_failure(
            context,
            analysis,
        )

        self._analyze_api_failure(
            context,
            analysis,
        )

        analysis.summary = self._create_summary(
            analysis
        )

        if analysis.probable_causes:
            analysis.confidence = 0.8
        else:
            analysis.confidence = 1.0


        context.root_cause = analysis

        self._print_summary(
            analysis
        )

        return context


    # ==========================================================
    # Analysis
    # ==========================================================

    def _analyze_build_failure(
        self,
        context: AgentContext,
        analysis: RootCause,
    ) -> None:

        result = getattr(
            context,
            "build_result",
            None,
        )

        if result and not result.success:

            analysis.probable_causes.append(
                "Project build failed."
            )

            analysis.suggested_fixes.append(
                "Review build logs and fix compilation errors."
            )


    def _analyze_runtime_failure(
        self,
        context: AgentContext,
        analysis: RootCause,
    ) -> None:

        result = getattr(
            context,
            "runtime_result",
            None,
        )

        if result and not result.success:

            analysis.probable_causes.append(
                "Application failed during startup."
            )

            analysis.suggested_fixes.append(
                "Check runtime logs, environment variables, and configuration."
            )


    def _analyze_api_failure(
        self,
        context: AgentContext,
        analysis: RootCause,
    ) -> None:

        results = getattr(
            context,
            "api_results",
            [],
        )

        failed = [
            result
            for result in results
            if not result.passed
        ]

        if failed:

            analysis.probable_causes.append(
                "One or more API endpoints failed."
            )

            analysis.suggested_fixes.append(
                "Check API routes, server availability, and response handling."
            )


    # ==========================================================
    # Helpers
    # ==========================================================

    def _create_summary(
        self,
        analysis: RootCause,
    ) -> str:

        if not analysis.probable_causes:

            return (
                "No verification failures detected."
            )

        return (
            f"Detected {len(analysis.probable_causes)} "
            "possible root cause(s)."
        )


    # ==========================================================
    # Console
    # ==========================================================

    def _print_header(self) -> None:

        print("\n" + "=" * 70)
        print("🧠 Root Cause Analyzer")
        print("=" * 70)


    def _print_summary(
        self,
        analysis: RootCause,
    ) -> None:

        print(
            f"Causes       : {len(analysis.probable_causes)}"
        )

        print(
            f"Suggestions  : {len(analysis.suggested_fixes)}"
        )

        print(
            f"Confidence   : {analysis.confidence}"
        )