"""
Filesystem writer.

Responsible for writing generated files
into the repository filesystem.
"""

from __future__ import annotations

from pathlib import Path

from core.models.generation import GeneratedFile


class FilesystemWriter:
    """
    Writes generated files to disk.
    """

    def write(
        self,
        root_path: str,
        file: GeneratedFile,
    ) -> Path:
        """
        Write a generated file.

        Args:
            root_path:
                Repository root directory.

            file:
                Generated file information.

        Returns:
            Path of written file.
        """

        target_path = (
            Path(root_path)
            / file.path
        )

        self._ensure_directory(
            target_path
        )

        target_path.write_text(
            file.content,
            encoding="utf-8",
        )

        return target_path

    # =========================================================
    # Helpers
    # =========================================================

    @staticmethod
    def _ensure_directory(
        file_path: Path,
    ) -> None:
        """
        Create parent directories if missing.
        """

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        