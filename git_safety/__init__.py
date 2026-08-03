"""
CodePilot Git Safety Layer.
"""

from .snapshot import (
    GitSnapshot,
    SnapshotManager,
)

from .exceptions import (
    GitError,
    GitCommandError,
    NotAGitRepositoryError,
    SnapshotError,
)

from .models import (
    ChangeType,
    DiffEntry,
    DiffReport,
)

__all__ = [
    "GitSnapshot",
    "SnapshotManager",
    "GitError",
    "GitCommandError",
    "NotAGitRepositoryError",
    "SnapshotError",
    "ChangeType",
    "DiffEntry",
    "DiffReport",
]