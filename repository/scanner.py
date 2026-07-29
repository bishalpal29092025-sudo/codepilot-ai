"""
Repository scanner.

Responsible only for traversing a repository and collecting relevant files.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from repository.constants import (
    ALLOWED_HIDDEN_FILES,
    IGNORE_DIRECTORIES,
    IMPORTANT_FILES,
    SUPPORTED_EXTENSIONS,
)
from repository.exceptions import RepositoryScanError

logger = logging.getLogger(__name__)


class RepositoryScanner:
    """
    Traverses a repository and returns relevant files.

    This class is responsible only for filesystem traversal.
    It performs no framework or language detection.
    """

    def __init__(self, repository_path: str | Path) -> None:
        self.repository_path = Path(repository_path).resolve()

    def scan(self) -> list[str]:
        """
        Scan the repository.

        Returns:
            Sorted list of repository-relative file paths.

        Raises:
            RepositoryScanError:
                If the repository does not exist or scanning fails.
        """

        if not self.repository_path.exists():
            raise RepositoryScanError(
                f"Repository not found: {self.repository_path}"
            )

        collected_files: list[str] = []

        try:
            for root, directories, files in os.walk(self.repository_path):

                directories[:] = [
                    directory
                    for directory in directories
                    if directory not in IGNORE_DIRECTORIES
                ]

                for filename in files:

                    if (
                        filename.startswith(".")
                        and filename not in ALLOWED_HIDDEN_FILES
                    ):
                        continue

                    extension = Path(filename).suffix

                    if (
                        extension not in SUPPORTED_EXTENSIONS
                        and filename not in IMPORTANT_FILES
                    ):
                        continue

                    absolute_path = Path(root) / filename

                    relative_path = absolute_path.relative_to(
                        self.repository_path
                    )

                    collected_files.append(relative_path.as_posix())

            collected_files.sort()

            logger.info(
                "Repository scan completed (%d files found).",
                len(collected_files),
            )

            return collected_files

        except Exception as exc:
            logger.exception("Repository scan failed.")
            raise RepositoryScanError(str(exc)) from exc