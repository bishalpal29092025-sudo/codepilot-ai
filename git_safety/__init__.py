"""
CodePilot Git Safety Layer.
"""

from .snapshot import (
    GitSnapshot,
    SnapshotManager,
)

from .diff import (
    DiffEngine,
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
    # Snapshot
    "GitSnapshot",
    "SnapshotManager",

    # Diff Engine
    "DiffEngine",

    # Exceptions
    "GitError",
    "GitCommandError",
    "NotAGitRepositoryError",
    "SnapshotError",

    # Models
    "ChangeType",
    "DiffEntry",
    "DiffReport",
]