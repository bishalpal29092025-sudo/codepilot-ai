"""
Git Diff Engine.

Analyzes repository changes after CodePilot modifications.

Responsibilities:
- Detect changed files
- Detect new files
- Detect deleted files
- Count additions/deletions
- Generate DiffReport
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from git_safety.models import (
    ChangeType,
    DiffEntry,
    DiffReport,
)


class DiffEngine:
    """
    Analyzes git repository differences.
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

    def generate_diff(self) -> DiffReport:
        """
        Generate complete repository diff report.
        """

        files: list[DiffEntry] = []


        # Tracked file changes
        files.extend(
            self._get_tracked_changes()
        )


        # New untracked files
        files.extend(
            self._get_untracked_files()
        )


        return DiffReport(
            files=files,

            total_additions=sum(
                file.additions
                for file in files
            ),

            total_deletions=sum(
                file.deletions
                for file in files
            ),
        )


    # ==========================================================
    # Tracked Changes
    # ==========================================================

    def _get_tracked_changes(self) -> list[DiffEntry]:
        """
        Detect modified, added and deleted tracked files.
        """

        result = subprocess.run(
            [
                "git",
                "diff",
                "--numstat",
                "--name-status",
            ],

            cwd=self.repository_path,

            capture_output=True,

            text=True,
        )


        if result.returncode != 0:
            return []


        entries: list[DiffEntry] = []


        for line in result.stdout.splitlines():

            if not line.strip():
                continue


            parts = line.split("\t")


            if len(parts) < 3:
                continue


            additions = self._parse_number(
                parts[0]
            )

            deletions = self._parse_number(
                parts[1]
            )


            status = parts[2][0]

            path = parts[-1]


            change_type = (
                ChangeType.ADDED
                if status == "A"

                else ChangeType.DELETED
                if status == "D"

                else ChangeType.MODIFIED
            )


            entries.append(
                DiffEntry(
                    path=path,
                    change_type=change_type,
                    additions=additions,
                    deletions=deletions,
                )
            )


        return entries



    # ==========================================================
    # Untracked Files
    # ==========================================================

    def _get_untracked_files(self) -> list[DiffEntry]:
        """
        Detect new files created by CodePilot.

        Example:
            ?? new_file.py
        """

        result = subprocess.run(
            [
                "git",
                "status",
                "--short",
            ],

            cwd=self.repository_path,

            capture_output=True,

            text=True,
        )


        if result.returncode != 0:
            return []


        entries: list[DiffEntry] = []


        for line in result.stdout.splitlines():

            if not line.startswith(
                "??"
            ):
                continue


            path = line[3:]


            additions = self._count_file_lines(
                path
            )


            entries.append(
                DiffEntry(
                    path=path,
                    change_type=ChangeType.ADDED,
                    additions=additions,
                    deletions=0,
                )
            )


        return entries



    # ==========================================================
    # Helpers
    # ==========================================================

    @staticmethod
    def _parse_number(
        value: str,
    ) -> int:
        """
        Convert git numstat values.

        Binary files return '-'.
        """

        if value == "-":
            return 0


        return int(value)



    def _count_file_lines(
        self,
        relative_path: str,
    ) -> int:
        """
        Count lines for newly created files.
        """

        file_path = (
            self.repository_path
            / relative_path
        )


        if not file_path.exists():
            return 0


        try:

            with file_path.open(
                "r",
                encoding="utf-8",
            ) as file:

                return len(
                    file.readlines()
                )

        except Exception:

            return 0