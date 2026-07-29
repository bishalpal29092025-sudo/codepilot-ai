"""
Repository domain models.

These models represent metadata discovered while exploring a source code
repository. They are shared across the repository exploration, planning,
and generation stages of the CodePilot AI pipeline.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# Enums
# ============================================================================


class ProgrammingLanguage(StrEnum):
    UNKNOWN = "unknown"
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    RUST = "rust"
    GO = "go"


class ProjectType(StrEnum):
    UNKNOWN = "unknown"
    WEB = "web"
    BACKEND = "backend"
    CLI = "cli"
    LIBRARY = "library"
    MOBILE = "mobile"


# ============================================================================
# Base Model
# ============================================================================


class ImmutableModel(BaseModel):
    """
    Immutable base model used by repository models.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        use_enum_values=True,
    )


# ============================================================================
# Repository Model
# ============================================================================


class RepositoryInfo(ImmutableModel):
    """
    Complete snapshot of repository metadata discovered during exploration.
    """

    name: str = Field(
        ...,
        description="Repository name.",
    )

    root_path: str = Field(
        ...,
        description="Repository root directory.",
    )

    project_type: ProjectType = Field(
        default=ProjectType.UNKNOWN,
        description="Detected project type.",
    )

    primary_language: ProgrammingLanguage = Field(
        default=ProgrammingLanguage.UNKNOWN,
        description="Primary programming language.",
    )

    frameworks: list[str] = Field(
        default_factory=list,
        description="Detected frameworks.",
    )

    database: str = Field(
        default="Unknown",
        description="Detected database.",
    )

    package_manager: str = Field(
        default="Unknown",
        description="Detected package manager.",
    )

    entry_points: list[str] = Field(
        default_factory=list,
        description="Repository entry points.",
    )

    source_directories: list[str] = Field(
        default_factory=list,
        description="Source code directories.",
    )

    ignored_directories: list[str] = Field(
        default_factory=list,
        description="Ignored directories.",
    )

    repository_files: list[str] = Field(
        default_factory=list,
        description="Repository-relative file paths.",
    )

    total_files: int = Field(
        default=0,
        ge=0,
        description="Total number of repository files.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional repository metadata.",
    )