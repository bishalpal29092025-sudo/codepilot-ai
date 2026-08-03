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


from .rollback import (
    RollbackEngine,
    RollbackError,
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

    RollbackResult,
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


    # Rollback
    "RollbackEngine",
    "RollbackError",
    "RollbackResult",


    # Exceptions
    "GitError",
    "GitCommandError",
    "NotAGitRepositoryError",
    "SnapshotError",

]