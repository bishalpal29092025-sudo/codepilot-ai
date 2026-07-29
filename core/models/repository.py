"""
Repository domain models.

These models represent metadata discovered while exploring a source code
repository. They are shared across the repository exploration and planning
stages of the CodePilot AI pipeline.
"""

from typing import List

from pydantic import BaseModel, Field


class RepositoryInfo(BaseModel):
    """
    Metadata about a repository discovered during exploration.
    """

    language: str = Field(
        default="Unknown",
        description="Primary programming language.",
    )

    framework: str = Field(
        default="Unknown",
        description="Detected application framework.",
    )

    database: str = Field(
        default="Unknown",
        description="Detected database technology.",
    )

    package_manager: str = Field(
        default="Unknown",
        description="Detected package manager.",
    )

    files: List[str] = Field(
        default_factory=list,
        description="Important repository files.",
    )

    total_files: int = Field(
        default=0,
        description="Total number of scanned files.",
    )