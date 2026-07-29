"""
Backup writer.

Creates backups of existing repository files
before generated changes are applied.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


class BackupWriter:
    """
    Creates backups of existing files.
    """

    def backup(
        self,
        file_path: Path,
        backup_root: Path,
    ) -> Path | None:
        """
        Create a backup of a file.

        Args:
            file_path:
                Original file path.

            backup_root:
                Directory where backups are stored.

        Returns:
            Backup file path if created,
            otherwise None.
        """

        if not file_path.exists():
            return None

        timestamp = (
            datetime.now()
            .strftime("%Y%m%d_%H%M%S")
        )

        relative_path = file_path.name

        backup_path = (
            backup_root
            / f"{relative_path}.{timestamp}.bak"
        )

        backup_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        backup_path.write_text(
            file_path.read_text(
                encoding="utf-8"
            ),
            encoding="utf-8",
        )

        return backup_path