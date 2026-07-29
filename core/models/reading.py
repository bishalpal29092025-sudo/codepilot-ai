"""
Reading domain models.

These models represent repository content loaded by the reader stage of the
CodePilot AI pipeline.
"""

from typing import Dict, List

from pydantic import BaseModel, Field


class RepositoryContext(BaseModel):
    """
    Source code and metadata loaded from the repository.
    """

    files: Dict[str, str] = Field(
        default_factory=dict,
        description="Mapping of repository-relative file paths to file contents.",
    )

    loaded_files: List[str] = Field(
        default_factory=list,
        description="Files successfully loaded.",
    )

    missing_files: List[str] = Field(
        default_factory=list,
        description="Files requested by the planner but not found.",
    )

    skipped_files: List[str] = Field(
        default_factory=list,
        description="Binary, unreadable, unsupported, or oversized files.",
    )