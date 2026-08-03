"""
Git Snapshot Manager.

Creates safe restore points before CodePilot
modifies a repository.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .exceptions import (
    GitCommandError,
    NotAGitRepositoryError,
)


# ==========================================================
# Snapshot Model
# ==========================================================


@dataclass(frozen=True)
class GitSnapshot:
    """
    Represents repository state.
    """

    repository_path: str

    commit_hash: str

    branch: str

    is_clean: bool

    backup_path: str

    created_at: datetime



# ==========================================================
# Snapshot Manager
# ==========================================================


class SnapshotManager:
    """
    Creates and manages repository snapshots.
    """


    def __init__(
        self,
        repository_path: str,
    ) -> None:

        self.repository_path = Path(
            repository_path
        ).resolve()



    # ======================================================
    # Public API
    # ======================================================

    def create_snapshot(self) -> GitSnapshot:
        """
        Capture current repository state.
        """

        self._validate_repository()


        return GitSnapshot(

            repository_path=str(
                self.repository_path
            ),

            commit_hash=self._current_commit(),

            branch=self._current_branch(),

            is_clean=self._is_clean(),

            backup_path=self._create_backup(),

            created_at=datetime.now(
                timezone.utc
            ),

        )



    # ======================================================
    # Backup
    # ======================================================

    def _create_backup(self) -> str:
        """
        Create complete repository backup.

        Excludes .git directory.
        """

        backup_dir = tempfile.mkdtemp(
            prefix="codepilot_snapshot_"
        )


        shutil.copytree(

            self.repository_path,

            backup_dir,

            dirs_exist_ok=True,

            ignore=shutil.ignore_patterns(
                ".git"
            ),
        )


        return backup_dir



    # ======================================================
    # Git Operations
    # ======================================================

    def _validate_repository(self) -> None:

        result = subprocess.run(

            [
                "git",
                "rev-parse",
                "--git-dir",
            ],

            cwd=self.repository_path,

            capture_output=True,

            text=True,
        )


        if result.returncode != 0:

            raise NotAGitRepositoryError(
                str(self.repository_path)
            )



    def _current_commit(self) -> str:

        return self._run_git(
            [
                "git",
                "rev-parse",
                "HEAD",
            ]
        )



    def _current_branch(self) -> str:

        return self._run_git(
            [
                "git",
                "branch",
                "--show-current",
            ]
        )



    def _is_clean(self) -> bool:

        result = subprocess.run(

            [
                "git",
                "status",
                "--porcelain",
            ],

            cwd=self.repository_path,

            capture_output=True,

            text=True,
        )


        return result.stdout.strip() == ""



    def _run_git(
        self,
        command: list[str],
    ) -> str:

        result = subprocess.run(

            command,

            cwd=self.repository_path,

            capture_output=True,

            text=True,
        )


        if result.returncode != 0:

            raise GitCommandError(
                " ".join(command),
                result.stderr,
            )


        return result.stdout.strip()