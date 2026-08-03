"""
Git Diff Engine.

Analyzes repository changes after CodePilot modifications.
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
        Generate repository diff report.
        """

        changes = self._get_file_changes()

        stats = self._get_stats()

        return DiffReport(
            files=changes,
            total_additions=stats["additions"],
            total_deletions=stats["deletions"],
        )


    # ==========================================================
    # Git Commands
    # ==========================================================

    def _get_file_changes(self) -> list[DiffEntry]:
        """
        Parse git diff --name-status output.
        """

        result = subprocess.run(
            [
                "git",
                "diff",
                "--name-status",
            ],
            cwd=self.repository_path,
            capture_output=True,
            text=True,
        )


        if result.returncode != 0:
            return []


        entries = []


        for line in result.stdout.splitlines():

            if not line.strip():
                continue


            parts = line.split(
                "\t"
            )


            status = parts[0]

            path = parts[-1]


            if status == "A":

                change_type = ChangeType.ADDED


            elif status == "D":

                change_type = ChangeType.DELETED


            else:

                change_type = ChangeType.MODIFIED



            entries.append(
                DiffEntry(
                    path=path,
                    change_type=change_type,
                )
            )


        return entries



    def _get_stats(self) -> dict[str, int]:
        """
        Get insertion/deletion statistics.
        """

        result = subprocess.run(
            [
                "git",
                "diff",
                "--stat",
            ],

            cwd=self.repository_path,

            capture_output=True,

            text=True,
        )


        additions = 0
        deletions = 0


        if not result.stdout:
            return {
                "additions": 0,
                "deletions": 0,
            }


        for line in result.stdout.splitlines():

            if "insertion" in line:

                parts = line.split(",")

                for part in parts:

                    if "insertion" in part:

                        additions = int(
                            part.strip()
                            .split()[0]
                        )


            if "deletion" in line:

                parts = line.split(",")

                for part in parts:

                    if "deletion" in part:

                        deletions = int(
                            part.strip()
                            .split()[0]
                        )


        return {
            "additions": additions,
            "deletions": deletions,
        }