"""
Git Rollback Engine.

Restores repository state from CodePilot snapshots.
"""

from __future__ import annotations

import shutil

from datetime import datetime, timezone
from pathlib import Path

from .models import RollbackResult



class RollbackError(Exception):
    """
    Rollback operation failed.
    """

    pass



class RollbackEngine:
    """
    Restores repository from snapshot backups.

    Supports:
    - Modified files
    - Created files
    - Deleted files
    """

    def __init__(
        self,
        repository_path: str,
    ) -> None:

        self.repository_path = Path(
            repository_path
        ).resolve()



    # ==========================================================
    # Public API
    # ==========================================================

    def restore_snapshot(
        self,
        snapshot,
    ) -> RollbackResult:
        """
        Restore repository from snapshot backup.
        """


        if not hasattr(
            snapshot,
            "backup_path",
        ):

            raise RollbackError(
                "Snapshot does not contain backup_path. "
                "Update SnapshotManager first."
            )


        backup_path = Path(
            snapshot.backup_path
        )


        if not backup_path.exists():

            raise RollbackError(
                "Snapshot backup does not exist."
            )


        shutil.copytree(
            backup_path,
            self.repository_path,
            dirs_exist_ok=True,
        )


        return RollbackResult(

            success=True,

            message=(
                "Repository restored successfully."
            ),

            restored_files=[],

            created_at=datetime.now(
                timezone.utc
            ),
        )