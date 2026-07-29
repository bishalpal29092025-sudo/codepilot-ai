"""
Reporting Engine Test.

Validates:
- Engineering report generation
- Summary creation
- Report formatting
"""

from core.context import AgentContext
from core.models import (
    BuildResult,
    RuntimeResult,
    DependencyReport,
    RootCause,
)

from reporting.reporter import Reporter
from reporting.formatter import ReportFormatter


# ==========================================================
# Create Agent Context
# ==========================================================

context = AgentContext(
    user_request="Generate engineering report"
)


# ==========================================================
# Mock pipeline results
# ==========================================================

context.dependency_report = DependencyReport(
    language="JavaScript",
    framework="Node.js",
    package_manager="npm",
    install_command="npm install",
    build_command="npm run build",
    run_command="npm run dev",
)


context.build_result = BuildResult(
    success=True,
    command="npm run build",
    exit_code=0,
    logs="Build successful",
)


context.runtime_result = RuntimeResult(
    success=True,
    command="npm run dev",
    logs="Application started successfully",
)


context.root_cause = RootCause(
    summary="No issues detected.",
    probable_causes=[],
    suggested_fixes=[],
    confidence=1.0,
)


# ==========================================================
# Run Reporting Engine
# ==========================================================

reporter = Reporter()

context = reporter.run(
    context
)


# ==========================================================
# Format Report
# ==========================================================

formatter = ReportFormatter()

output = formatter.format(
    context.engineering_report
)


print("\nFinal Report:")
print(output)