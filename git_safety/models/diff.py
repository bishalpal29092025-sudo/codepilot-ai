"""
Git Diff Models.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ChangeType(str, Enum):
    """
    Type of repository change.
    """

    ADDED = "added"

    MODIFIED = "modified"

    DELETED = "deleted"



@dataclass(frozen=True)
class DiffEntry:
    """
    Represents a single changed file.
    """

    path: str

    change_type: ChangeType

    additions: int = 0

    deletions: int = 0



@dataclass(frozen=True)
class DiffReport:
    """
    Complete repository diff report.
    """

    files: list[DiffEntry]

    total_additions: int = 0

    total_deletions: int = 0
