"""
Verification orchestrator.

Coordinates all verification stages in the CodePilot pipeline.

Pipeline:

Dependency Check
        |
        v
Build Validation
        |
        v
Runtime Validation
        |
        v
API Testing
        |
        v
Root Cause Analysis
        |
        v
Verification Report
"""

from __future__ import annotations

from pathlib import Path

from core.context import AgentContext

from verification.api_tester import ApiTester
from verification.build_validator import BuildValidator
from verification.dependency_checker import DependencyChecker
from verification.reporter import Reporter
from verification.root_cause import RootCauseAnalyzer
from verification.runtime_validator import RuntimeValidator


class Verifier:
    """
    Main Verification Engine.

    Executes complete verification workflow
    and returns enriched AgentContext.
    """

    def __init__(
        self,
        repository_path: str,
        base_url: str = "http://localhost:3000",
    ) -> None:

        self.repository_path = Path(
            repository_path
        )

        self.dependency_checker = DependencyChecker(
            str(self.repository_path)
        )

        self.build_validator = BuildValidator(
            str(self.repository_path)
        )

        self.runtime_validator = RuntimeValidator(
            str(self.repository_path)
        )

        self.api_tester = ApiTester(
            str(self.repository_path),
            base_url,
        )

        self.root_cause = RootCauseAnalyzer()

        self.reporter = Reporter()


    # ==========================================================
    # Public API
    # ==========================================================

    def verify(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Execute complete verification pipeline.
        """

        self._print_header()


        stages = [
            (
                "Dependency Analysis",
                self.dependency_checker,
            ),
            (
                "Build Validation",
                self.build_validator,
            ),
            (
                "Runtime Validation",
                self.runtime_validator,
            ),
            (
                "API Testing",
                self.api_tester,
            ),
            (
                "Root Cause Analysis",
                self.root_cause,
            ),
            (
                "Report Generation",
                self.reporter,
            ),
        ]


        for name, stage in stages:

            print(
                f"\n▶ Running: {name}"
            )

            context = stage.run(
                context
            )


        self._print_footer()

        return context


    # ==========================================================
    # Console
    # ==========================================================

    def _print_header(self) -> None:

        print("\n")
        print("=" * 70)
        print("🔍 CodePilot Verification Engine")
        print("=" * 70)


    def _print_footer(self) -> None:

        print("\n")
        print("=" * 70)
        print("✅ Verification Completed")
        print("=" * 70)