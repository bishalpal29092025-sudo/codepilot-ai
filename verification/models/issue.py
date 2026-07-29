"""
Verification issue models.

Defines issues detected during verification.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class IssueSeverity(StrEnum):
    """
    Severity level of an issue.
    """

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class IssueCategory(StrEnum):
    """
    Category of verification issue.
    """

    BUILD = "build"
    RUNTIME = "runtime"
    API = "api"
    DEPENDENCY = "dependency"
    SECURITY = "security"
    QUALITY = "quality"


class Issue(BaseModel):
    """
    Represents a detected verification issue.
    """

    title: str = Field(
        ...,
        description="Issue title.",
    )

    description: str = Field(
        ...,
        description="Issue description.",
    )

    severity: IssueSeverity = Field(
        default=IssueSeverity.WARNING,
        description="Issue severity.",
    )

    category: IssueCategory = Field(
        default=IssueCategory.QUALITY,
        description="Issue category.",
    )

    file_path: str | None = Field(
        default=None,
        description="Related file path.",
    )

    line_number: int | None = Field(
        default=None,
        description="Related line number.",
    )

    suggestion: str | None = Field(
        default=None,
        description="Suggested fix.",
    )