"""
Reporting domain models.

These models represent the final summary produced after the CodePilot AI
pipeline completes successfully.
"""

from typing import List

from pydantic import BaseModel, Field


class Summary(BaseModel):
    """
    Final execution summary.
    """

    files_changed: List[str] = Field(
        default_factory=list,
        description="Files modified during execution.",
    )

    features_added: List[str] = Field(
        default_factory=list,
        description="Features implemented.",
    )

    testing: List[str] = Field(
        default_factory=list,
        description="Recommended testing checklist.",
    )

    notes: List[str] = Field(
        default_factory=list,
        description="Additional implementation notes.",
    )