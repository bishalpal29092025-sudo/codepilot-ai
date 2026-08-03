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


__all__ = [
    "GitSnapshot",
    "SnapshotManager",

    "GitError",
    "GitCommandError",
    "NotAGitRepositoryError",
    "SnapshotError",
]