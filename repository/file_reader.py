"""
Repository file reader.

Provides safe utilities for reading repository files while protecting
against invalid paths, binary files, oversized files, and encoding issues.
"""

from __future__ import annotations

import logging
from pathlib import Path

from repository.exceptions import RepositoryReadError

logger = logging.getLogger(__name__)


class RepositoryFileReader:
    """
    Safely reads repository files.

    This class is responsible only for reading repository files.
    """

    DEFAULT_ENCODING = "utf-8"
    DEFAULT_MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB

    def __init__(
        self,
        repository_path: str | Path,
        *,
        max_file_size: int = DEFAULT_MAX_FILE_SIZE,
    ) -> None:
        self.repository_path = Path(repository_path).resolve()
        self.max_file_size = max_file_size

    def read(self, relative_path: str | Path) -> str:
        """
        Read a repository file.

        Args:
            relative_path:
                Repository-relative file path.

        Returns:
            File contents.

        Raises:
            RepositoryReadError:
                If the file cannot be read safely.
        """

        file_path = self._resolve_path(relative_path)

        self._validate_file(file_path)

        try:
            content = file_path.read_text(
                encoding=self.DEFAULT_ENCODING,
                errors="ignore",
            )

            logger.debug("Read file: %s", relative_path)

            return content

        except Exception as exc:
            logger.exception("Failed to read %s", relative_path)
            raise RepositoryReadError(str(exc)) from exc

    def exists(self, relative_path: str | Path) -> bool:
        """
        Return True if the repository file exists.
        """

        try:
            path = self._resolve_path(relative_path)
            return path.exists()
        except RepositoryReadError:
            return False

    def size(self, relative_path: str | Path) -> int:
        """
        Return file size in bytes.
        """

        path = self._resolve_path(relative_path)
        self._validate_file(path)

        return path.stat().st_size

    def read_if_exists(
        self,
        relative_path: str | Path,
    ) -> str | None:
        """
        Read a file if it exists.

        Returns:
            File contents or None.
        """

        if not self.exists(relative_path):
            return None

        return self.read(relative_path)

    def _resolve_path(self, relative_path: str | Path) -> Path:
        """
        Resolve and validate a repository-relative path.
        """

        path = (self.repository_path / relative_path).resolve()

        try:
            path.relative_to(self.repository_path)
        except ValueError as exc:
            raise RepositoryReadError(
                f"Invalid repository path: {relative_path}"
            ) from exc

        return path

    def _validate_file(self, path: Path) -> None:
        """
        Validate that a file can be safely read.
        """

        if not path.exists():
            raise RepositoryReadError(
                f"File not found: {path}"
            )

        if not path.is_file():
            raise RepositoryReadError(
                f"Not a file: {path}"
            )

        size = path.stat().st_size

        if size > self.max_file_size:
            raise RepositoryReadError(
                f"File exceeds maximum size ({self.max_file_size} bytes): "
                f"{path.name}"
            )

        if self._is_binary(path):
            raise RepositoryReadError(
                f"Binary files are not supported: {path.name}"
            )

    @staticmethod
    def _is_binary(path: Path) -> bool:
        """
        Perform a lightweight binary file check.
        """

        try:
            with path.open("rb") as file:
                chunk = file.read(1024)

            return b"\x00" in chunk

        except OSError:
            return False