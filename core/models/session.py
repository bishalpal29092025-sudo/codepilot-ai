"""
Agent Session Models.

Stores complete lifecycle information
for a CodePilot execution run.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# Base Model
# ==========================================================


class SessionModel(BaseModel):
    """
    Immutable session base model.
    """

    model_config = ConfigDict(
        extra="forbid",
    )



# ==========================================================
# Agent Session
# ==========================================================


class AgentSession(SessionModel):
    """
    Represents one complete CodePilot execution session.

    Lifecycle:

    Request
        |
        v
    Planning
        |
        v
    Generation
        |
        v
    Execution
        |
        v
    Verification
        |
        v
    Reporting
    """

    id: str = Field(
        ...,
        description="Unique session identifier.",
    )


    user_request: str = Field(
        ...,
        description="Original user request.",
    )


    repository_path: str = Field(
        ...,
        description="Repository being modified.",
    )


    started_at: datetime = Field(
        default_factory=lambda:
            datetime.now(timezone.utc),
        description="Session start time.",
    )


    completed_at: datetime | None = Field(
        default=None,
        description="Session completion time.",
    )


    status: str = Field(
        default="running",
        description="Session status.",
    )


    generated_files: list[str] = Field(
        default_factory=list,
        description="Generated file paths.",
    )


    written_files: list[str] = Field(
        default_factory=list,
        description="Files written to repository.",
    )


    executed_commands: list[str] = Field(
        default_factory=list,
        description="Commands executed.",
    )


    errors: list[str] = Field(
        default_factory=list,
        description="Errors collected.",
    )


    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional session information.",
    )



    # ======================================================
    # Helpers
    # ======================================================

    def complete(
        self,
    ) -> None:
        """
        Mark session completed.
        """

        self.status = "completed"

        self.completed_at = (
            datetime.now(timezone.utc)
        )