"""
Repository explorer.

Coordinates repository scanning, metadata loading, and detection.
"""

from __future__ import annotations

import logging
from pathlib import Path

from core.models import RepositoryInfo
from repository.detector import RepositoryDetector
from repository.loader import RepositoryLoader
from repository.scanner import RepositoryScanner

logger = logging.getLogger(__name__)


class RepositoryExplorer:
    """
    Explore a repository and produce RepositoryInfo.

    This class orchestrates the repository pipeline.
    """

    def __init__(
        self,
        repository_path: str | Path,
    ) -> None:
        self.repository_path = Path(repository_path).resolve()

    def explore(self) -> RepositoryInfo:
        """
        Explore the repository and return detected metadata.
        """

        scanner = RepositoryScanner(self.repository_path)
        files = scanner.scan()

        loader = RepositoryLoader(self.repository_path)
        loader.load()

        detector = RepositoryDetector(
            files=files,
            loader=loader,
        )

        info = detector.detect()

        logger.info("Repository exploration completed.")

        return info