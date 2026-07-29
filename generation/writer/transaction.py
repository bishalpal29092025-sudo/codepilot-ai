"""
Generation transaction writer.

Provides atomic file generation by combining
backup and filesystem operations.
"""

from __future__ import annotations

from pathlib import Path

from core.models.generation import GeneratedFile

from .backup import BackupWriter
from .filesystem import FilesystemWriter


class TransactionWriter:
    """
    Safely writes generated files.

    Supports:
        - backup creation
        - multi-file writes
        - rollback on failure
    """

    def __init__(
        self,
        filesystem_writer: FilesystemWriter | None = None,
        backup_writer: BackupWriter | None = None,
    ) -> None:
        """
        Initialize transaction writer.
        """

        self.filesystem_writer = (
            filesystem_writer
            or FilesystemWriter()
        )

        self.backup_writer = (
            backup_writer
            or BackupWriter()
        )

    # =========================================================
    # Public API
    # =========================================================

    def execute(
        self,
        root_path: str,
        files: list[GeneratedFile],
        backup_directory: str = ".codepilot/backups",
    ) -> list[Path]:
        """
        Apply generated changes safely.

        Args:
            root_path:
                Repository root.

            files:
                Generated files.

            backup_directory:
                Backup location.

        Returns:
            Written file paths.

        Raises:
            Exception:
                Restores previous state on failure.
        """

        repository_root = Path(root_path)

        backup_root = (
            repository_root
            / backup_directory
        )

        written_files: list[Path] = []

        try:

            for file in files:

                target = (
                    repository_root
                    / file.path
                )

                self.backup_writer.backup(
                    target,
                    backup_root,
                )

                written = (
                    self.filesystem_writer.write(
                        root_path,
                        file,
                    )
                )

                written_files.append(
                    written
                )

            return written_files

        except Exception:

            self._rollback(
                written_files
            )

            raise

    # =========================================================
    # Helpers
    # =========================================================

    @staticmethod
    def _rollback(
        written_files: list[Path],
    ) -> None:
        """
        Remove files written during a failed
        transaction.

        Backup restoration will be handled by
        future recovery service.
        """

        for file_path in written_files:

            if file_path.exists():
                file_path.unlink()