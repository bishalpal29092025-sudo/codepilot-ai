"""
Execution result models.

Defines the final output produced by
the Execution Engine.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from .command_result import CommandResult


class ExecutionStatus(StrEnum):
    """
    Execution lifecycle status.
    """

    SUCCESS = "success"

    FAILED = "failed"

    TIMEOUT = "timeout"

    CANCELLED = "cancelled"


class ExecutionResult(BaseModel):
    """
    Complete execution report.

    Contains all executed commands,
    logs, errors and final status.
    """

    status: ExecutionStatus = Field(
        default=ExecutionStatus.FAILED,
        description="Overall execution status.",
    )

    success: bool = Field(
        default=False,
        description="Whether execution completed successfully.",
    )

    commands: list[CommandResult] = Field(
        default_factory=list,
        description="Executed command results.",
    )

    logs: str = Field(
        default="",
        description="Combined execution logs.",
    )

    errors: list[str] = Field(
        default_factory=list,
        description="Execution errors.",
    )

    summary: str = Field(
        default="",
        description="Human-readable execution summary.",
    )