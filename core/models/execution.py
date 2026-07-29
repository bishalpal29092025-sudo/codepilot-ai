"""
Execution domain models.

These models represent the outcome of applying generated changes to the
repository during the execution stage of the CodePilot AI pipeline.
"""

from typing import List

from pydantic import BaseModel, Field


class ExecutionResult(BaseModel):
    """
    Result of writing generated files to the repository.
    """

    written_files: List[str] = Field(
        default_factory=list,
        description="Files successfully written to disk.",
    )

    failed_files: List[str] = Field(
        default_factory=list,
        description="Files that could not be written.",
    )