"""
Repository file reader.

Provides safe utilities for reading repository files while protecting
against binary files, oversized files, and encoding issues.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class RepositoryFileReader:
    """
    Safely reads repository files.

    This class is responsible only for reading file contents.
    It performs no repository detection or analysis.
    """

    DEFAULT_ENCODING = "utf-8"
    MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB

    def __init__(self, repository_path: str | Path) -> None:
        self.repository_path = Path(repository_path).resolve()

    def read(self, relative_path: str | Path) -> str:
        """
        Read a repository file.

        Args:
            relative_path:
                Repository-relative file path.

        Returns:
            File contents.

        Raises:
            FileNotFoundError:
                If the file does not exist.

            ValueError:
                If the file exceeds the maximum size.
        """

        file_path = self.repository_path / relative_path

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        size = file_path.stat().st_size

        if size > self.MAX_FILE_SIZE:
            raise ValueError(
                f"File exceeds maximum size ({self.MAX_FILE_SIZE} bytes): "
                f"{relative_path}"
            )

        try:
            content = file_path.read_text(
                encoding=self.DEFAULT_ENCODING,
                errors="ignore",
            )

            logger.debug("Read file: %s", relative_path)

            return content

        except Exception:
            logger.exception("Failed to read %s", relative_path)
            raise

    def exists(self, relative_path: str | Path) -> bool:
        """
        Check whether a repository file exists.
        """

        return (self.repository_path / relative_path).exists()

    def size(self, relative_path: str | Path) -> int:
        """
        Return file size in bytes.
        """

        return (self.repository_path / relative_path).stat().st_size

    def read_if_exists(self, relative_path: str | Path) -> str | None:
        """
        Read a file if it exists.

        Returns None when the file is absent.
        """

        if not self.exists(relative_path):
            return None

        return self.read(relative_path)