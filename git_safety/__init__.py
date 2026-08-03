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


from .patch import (
    PatchEngine,
    PatchError,
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
    PatchOperation,
    FilePatch,
    PatchSet,
)



__all__ = [

    # Snapshot
    "GitSnapshot",
    "SnapshotManager",


    # Diff
    "DiffEngine",
    "ChangeType",
    "DiffEntry",
    "DiffReport",


    # Patch
    "PatchEngine",
    "PatchError",
    "PatchOperation",
    "FilePatch",
    "PatchSet",


    # Exceptions
    "GitError",
    "GitCommandError",
    "NotAGitRepositoryError",
    "SnapshotError",

]