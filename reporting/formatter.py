"""
Report formatter.

Converts engineering reports into
human-readable output.
"""

from core.models import EngineeringReport


class ReportFormatter:
    """
    Formats engineering reports.
    """

    def format(
        self,
        report: EngineeringReport,
    ) -> str:

        lines = []

        lines.append(
            "CodePilot Engineering Report"
        )

        lines.append(
            "-" * 40
        )

        if report.build:

            lines.append(
                f"Build Success: {report.build.success}"
            )

        if report.runtime:

            lines.append(
                f"Runtime Success: {report.runtime.success}"
            )

        if report.summary:

            lines.append(
                "Notes:"
            )

            lines.extend(
                report.summary.notes
            )

        return "\n".join(lines)