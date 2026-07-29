"""
Repository detector.

Analyses repository metadata and detects project information such as
programming language, framework, database, and package manager.
"""

from __future__ import annotations

import logging
from collections import Counter
from pathlib import Path
from typing import Any

from core.models import RepositoryInfo
from repository.constants import (
    DATABASE_MAP,
    FRAMEWORK_MAP,
    LANGUAGE_EXTENSIONS,
    PACKAGE_MANAGER_FILES,
)
from repository.loader import RepositoryLoader

logger = logging.getLogger(__name__)


class RepositoryDetector:
    """
    Detect repository metadata.

    This class performs analysis only.
    It does not access the filesystem.
    """

    def __init__(
        self,
        files: list[str],
        loader: RepositoryLoader,
    ) -> None:
        self.files = files
        self.loader = loader

    def detect(self) -> RepositoryInfo:
        """
        Analyse the repository and return detected metadata.
        """

        info = RepositoryInfo(
            language=self._detect_language(),
            framework=self._detect_framework(),
            database=self._detect_database(),
            package_manager=self._detect_package_manager(),
            files=self.files,
            total_files=len(self.files),
        )

        logger.info("Repository detection completed.")

        return info

    def _detect_language(self) -> str:
        """
        Detect the primary programming language.
        """

        counter: Counter[str] = Counter()

        for file in self.files:
            language = LANGUAGE_EXTENSIONS.get(Path(file).suffix)

            if language:
                counter[language] += 1

        if not counter:
            return "Unknown"

        return counter.most_common(1)[0][0]

    def _detect_framework(self) -> str:
        """
        Detect framework.
        """

        return self._find_dependency(
            FRAMEWORK_MAP,
            self.loader.package_json,
            self.loader.requirements,
        )

    def _detect_database(self) -> str:
        """
        Detect database technology.
        """

        return self._find_dependency(
            DATABASE_MAP,
            self.loader.package_json,
            self.loader.requirements,
        )

    def _detect_package_manager(self) -> str:
        """
        Detect package manager.
        """

        for filename, manager in PACKAGE_MANAGER_FILES.items():
            if filename in self.files:
                return manager

        return "Unknown"

    def _find_dependency(
        self,
        mapping: dict[str, str],
        package_json: dict[str, Any],
        requirements: str,
    ) -> str:
        """
        Detect dependencies from JavaScript and Python projects.
        """

        dependencies = {
            **package_json.get("dependencies", {}),
            **package_json.get("devDependencies", {}),
        }

        for dependency, detected in mapping.items():
            if dependency in dependencies:
                return detected

        requirements_lower = requirements.lower()

        for dependency, detected in mapping.items():
            if dependency.lower() in requirements_lower:
                return detected

        return "Unknown"