"""
Git Safety Layer Models.

Contains data structures used by:
- Diff Engine
- Patch Engine
- Rollback System
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ==========================================================
# Change Type
# ==========================================================


class ChangeType(str, Enum):
    """
    Type of repository change.
    """

    ADDED = "added"

    MODIFIED = "modified"

    DELETED = "deleted"



# ==========================================================
# Diff Entry
# ==========================================================


@dataclass(frozen=True)
class DiffEntry:
    """
    Represents a single file change.
    """

    path: str

    change_type: ChangeType

    additions: int = 0

    deletions: int = 0



# ==========================================================
# Diff Report
# ==========================================================


@dataclass
class DiffReport:
    """
    Complete repository change report.
    """

    files: list[DiffEntry] = field(
        default_factory=list
    )

    total_additions: int = 0

    total_deletions: int = 0


    @property
    def changed_files(self) -> int:
        """
        Number of changed files.
        """

        return len(self.files)


    @property
    def risk_score(self) -> float:
        """
        Estimate modification risk.

        Simple first version:
        - More files = more risk
        - More lines changed = more risk
        """

        score = (
            self.changed_files * 0.1
            + self.total_additions * 0.001
            + self.total_deletions * 0.001
        )

        return min(
            round(score, 2),
            1.0,
        )
