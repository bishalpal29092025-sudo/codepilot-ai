from core.context import AgentContext


class DependencyChecker:
    """
    Validates repository dependency analysis.

    Dependency detection is already performed by
    DependencyManager earlier in the pipeline.

    Responsibilities:
        - Validate DependencyReport exists
        - Display detected environment
        - Add verification warnings

    It does NOT:
        - Scan repository again
        - Detect package manager
        - Modify repository
        - Install dependencies
    """


    # ==========================================================
    # Public API
    # ==========================================================

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Validate existing dependency report.
        """

        self._print_header()


        report = context.dependency_report


        if report is None:
            raise ValueError(
                "Dependency report missing. "
                "Run DependencyManager before verification."
            )


        self._validate(report)


        self._print_summary(report)


        return context



    # ==========================================================
    # Validation
    # ==========================================================

    def _validate(
        self,
        report,
    ) -> None:
        """
        Validate dependency information.
        """


        if not report.language:

            report.warnings.append(
                "Programming language not detected."
            )


        if not report.package_manager:

            report.warnings.append(
                "Package manager not detected."
            )


        if (
            report.install_command is None
            or report.install_command == ""
        ):

            report.warnings.append(
                "Install command unavailable."
            )



    # ==========================================================
    # Console Output
    # ==========================================================

    def _print_header(self) -> None:

        print("\n")
        print("=" * 70)
        print("📦 Dependency Checker")
        print("=" * 70)



    def _print_summary(
        self,
        report,
    ) -> None:

        print(
            f"Language         : {report.language}"
        )

        print(
            f"Framework        : {report.framework}"
        )

        print(
            f"Package Manager  : {report.package_manager}"
        )

        print(
            f"Install Command  : {report.install_command}"
        )

        print(
            f"Build Command    : {report.build_command}"
        )

        print(
            f"Run Command      : {report.run_command}"
        )

        print(
            f"Warnings         : {len(report.warnings)}"
        )