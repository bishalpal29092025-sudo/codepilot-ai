"""
Rollback Models.

Defines structures used by CodePilot
to restore previous repository states.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RollbackResult:
    """
    Result of rollback operation.
    """

    success: bool

    message: str

    restored_files: list[str]

    created_at: datetime