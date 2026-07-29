"""
Verification Reporter.

Creates final verification summaries from
all verification pipeline results.
"""

from __future__ import annotations

from core.context import AgentContext

from verification.models import (
    VerificationResult,
    VerificationStatus,
)


class Reporter:
    """
    Generates final verification reports.
    """

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Build final verification result.
        """

        self._print_header()

        build_success = self._build_status(
            context
        )

        runtime_success = self._runtime_status(
            context
        )

        api_success = self._api_status(
            context
        )

        issues = getattr(
            context,
            "issues",
            [],
        )

        success = (
            build_success
            and runtime_success
            and api_success
            and len(issues) == 0
        )

        result = VerificationResult(
            status=(
                VerificationStatus.PASSED
                if success
                else VerificationStatus.FAILED
            ),
            success=success,
            issues=issues,
            build_successful=build_success,
            summary=self._create_summary(
                success
            ),
        )

        context.verification_result = result

        self._print_summary(
            result
        )

        return context


    # ==========================================================
    # Status Helpers
    # ==========================================================

    def _build_status(
        self,
        context: AgentContext,
    ) -> bool:
        """
        Check build result.
        """

        result = getattr(
            context,
            "build_result",
            None,
        )

        if result is None:
            return False

        return result.success


    def _runtime_status(
        self,
        context: AgentContext,
    ) -> bool:
        """
        Check runtime result.
        """

        result = getattr(
            context,
            "runtime_result",
            None,
        )

        if result is None:
            return False

        return result.success


    def _api_status(
        self,
        context: AgentContext,
    ) -> bool:
        """
        Check API testing result.
        """

        result = getattr(
            context,
            "api_test_result",
            None,
        )

        # No API testing performed
        if result is None:
            return True

        return result.failed == 0


    # ==========================================================
    # Summary
    # ==========================================================

    def _create_summary(
        self,
        success: bool,
    ) -> str:
        """
        Generate human-readable summary.
        """

        if success:
            return (
                "All verification checks passed successfully."
            )

        return (
            "Verification failed. "
            "Review detected issues and logs."
        )


    # ==========================================================
    # Console Output
    # ==========================================================

    def _print_header(self) -> None:

        print("\n" + "=" * 70)
        print("📊 Verification Reporter")
        print("=" * 70)


    def _print_summary(
        self,
        result: VerificationResult,
    ) -> None:

        print(
            f"Status : {result.status}"
        )

        print(
            f"Success: {result.success}"
        )

        print(
            f"Issues : {len(result.issues)}"
        )