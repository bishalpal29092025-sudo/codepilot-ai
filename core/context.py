"""
Agent Context.

Shared state container passed through the complete
CodePilot AI pipeline.

Every pipeline stage reads from and writes
to this object.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from core.models import (
    ApiTestResult,
    BuildResult,
    CodeResponse,
    DependencyReport,
    EngineeringReport,
    ExecutionResult,
    Plan,
    RepositoryContext,
    RepositoryInfo,
    RootCause,
    RuntimeResult,
    Summary,
)


class AgentContext(BaseModel):
    """
    Shared state passed through the entire CodePilot AI pipeline.

    Each pipeline stage reads from and writes to this object.
    """


    # ==========================================================
    # User Input
    # ==========================================================

    user_request: str


    # ==========================================================
    # Repository Analysis
    # ==========================================================

    repository_info: RepositoryInfo | None = None


    # ==========================================================
    # Planning
    # ==========================================================

    plan: Plan | None = None


    # ==========================================================
    # Repository Reader
    # ==========================================================

    repository_context: RepositoryContext | None = None


    # ==========================================================
    # Code Generation
    # ==========================================================

    code_response: CodeResponse | None = None


    # ==========================================================
    # Execution
    # ==========================================================

    execution_result: ExecutionResult | None = None


    # ==========================================================
    # Summary
    # ==========================================================

    summary: Summary | None = None


    # ==========================================================
    # Verification
    # ==========================================================

    dependency_report: DependencyReport | None = None

    build_result: BuildResult | None = None

    runtime_result: RuntimeResult | None = None

    api_test_result: ApiTestResult | None = None

    root_cause: RootCause | None = None

    # Verification Engine final result.
    #
    # Stored as object because VerificationResult
    # belongs to verification/models and importing
    # it here can create circular dependencies.
    verification_result: object | None = None


    # ==========================================================
    # Final Report
    # ==========================================================

    engineering_report: EngineeringReport | None = None


    # ==========================================================
    # Metadata
    # ==========================================================

    warnings: list[str] = Field(
        default_factory=list
    )

    errors: list[str] = Field(
        default_factory=list
    )