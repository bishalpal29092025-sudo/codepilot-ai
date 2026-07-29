"""
CodePilot Verification Engine.

Responsible for validating generated changes through:

- Dependency checks
- Build validation
- Runtime validation
- API testing
- Root cause analysis
- Report generation
"""

from __future__ import annotations


from pathlib import Path


from core.context import AgentContext


from verification.dependency_checker import DependencyChecker
from verification.build_validator import BuildValidator
from verification.runtime_validator import RuntimeValidator
from verification.api_tester import ApiTester
from verification.root_cause import RootCauseAnalyzer
from verification.reporter import Reporter



class Verifier:
    """
    Complete verification pipeline.

    Pipeline:

    1. Dependency Analysis
    2. Build Validation
    3. Runtime Validation
    4. API Testing
    5. Root Cause Analysis
    6. Report Generation
    """



    def __init__(
        self,
        repository_path: str,
        base_url: str = "http://localhost:3000",
    ) -> None:


        self.repository_path = Path(
            repository_path
        )


        # DependencyChecker now validates
        # existing DependencyReport created
        # by DependencyManager.
        #
        # It does not need repository_path.
        self.dependency_checker = DependencyChecker()



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
    # Pipeline Entry Point
    # ==========================================================

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Pipeline compatible entry point.

        Every stage in CodePilot uses:

            run(context) -> context
        """

        return self.verify(
            context
        )



    # ==========================================================
    # Verification Workflow
    # ==========================================================

    def verify(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Execute complete verification workflow.
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



        try:


            for name, stage in stages:


                print(
                    f"\n▶ Running: {name}"
                )


                context = stage.run(
                    context
                )



        except Exception as e:


            print(
                "\n❌ Verification Failed"
            )


            print(e)



            context.errors.append(
                str(e)
            )



        finally:


            self._cleanup_runtime()



        self._print_footer()



        return context



    # ==========================================================
    # Runtime Cleanup
    # ==========================================================

    def _cleanup_runtime(
        self,
    ) -> None:
        """
        Cleanup running application process.
        """


        process = getattr(
            self.runtime_validator,
            "process",
            None,
        )


        if process is None:

            return



        try:


            if hasattr(
                process,
                "terminate",
            ):

                process.terminate()



        except Exception as e:


            print(
                f"⚠️ Runtime cleanup failed: {e}"
            )



    # ==========================================================
    # Console
    # ==========================================================

    def _print_header(
        self,
    ) -> None:


        print("\n")

        print("=" * 70)

        print(
            "🔍 CodePilot Verification Engine"
        )

        print("=" * 70)



    def _print_footer(
        self,
    ) -> None:


        print("\n")

        print("=" * 70)

        print(
            "✅ Verification Completed"
        )

        print("=" * 70)