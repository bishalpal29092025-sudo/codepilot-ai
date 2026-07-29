"""
Verification result models.

Defines the final output produced by the
Verification Engine.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from .issue import Issue


class VerificationStatus(str):
    """
    Verification execution status.
    """

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"


class VerificationResult(BaseModel):
    """
    Complete verification report.
    """

    status: str = Field(
        default=VerificationStatus.PASSED,
        description="Overall verification status.",
    )

    success: bool = Field(
        default=True,
        description="Whether verification succeeded.",
    )

    issues: list[Issue] = Field(
        default_factory=list,
        description="Detected verification issues.",
    )

    tests_passed: int = Field(
        default=0,
        description="Number of passed tests.",
    )

    tests_failed: int = Field(
        default=0,
        description="Number of failed tests.",
    )

    build_successful: bool = Field(
        default=True,
        description="Whether project build succeeded.",
    )

    quality_score: float = Field(
        default=100.0,
        ge=0,
        le=100,
        description="Overall quality score.",
    )

    summary: str = Field(
        default="",
        description="Human-readable verification summary.",
    )