"""
Repository metadata loader.

Loads and caches important repository metadata files. This class performs
all file loading so that RepositoryDetector can focus purely on analysis.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from repository.file_reader import RepositoryFileReader

logger = logging.getLogger(__name__)


class RepositoryLoader:
    """
    Load and cache repository metadata.

    Metadata is loaded once and then exposed through read-only
    properties.
    """

    def __init__(
        self,
        repository_path: str | Path,
    ) -> None:
        self._reader = RepositoryFileReader(repository_path)

        self._package_json: dict[str, Any] = {}
        self._requirements: str = ""
        self._pyproject: str = ""
        self._cargo_toml: str = ""
        self._go_mod: str = ""

    def load(self) -> None:
        """
        Load all supported repository metadata.
        """

        self._package_json = self._load_package_json()
        self._requirements = (
            self._reader.read_if_exists("requirements.txt") or ""
        )
        self._pyproject = (
            self._reader.read_if_exists("pyproject.toml") or ""
        )
        self._cargo_toml = (
            self._reader.read_if_exists("Cargo.toml") or ""
        )
        self._go_mod = (
            self._reader.read_if_exists("go.mod") or ""
        )

        logger.info("Repository metadata loaded.")

    @property
    def package_json(self) -> dict[str, Any]:
        """Parsed package.json."""

        return self._package_json

    @property
    def requirements(self) -> str:
        """Contents of requirements.txt."""

        return self._requirements

    @property
    def pyproject(self) -> str:
        """Contents of pyproject.toml."""

        return self._pyproject

    @property
    def cargo_toml(self) -> str:
        """Contents of Cargo.toml."""

        return self._cargo_toml

    @property
    def go_mod(self) -> str:
        """Contents of go.mod."""

        return self._go_mod

    def _load_package_json(self) -> dict[str, Any]:
        """
        Parse package.json.

        Returns an empty dictionary if the file does not exist or cannot
        be parsed.
        """

        content = self._reader.read_if_exists("package.json")

        if not content:
            return {}

        try:
            return json.loads(content)

        except json.JSONDecodeError:
            logger.warning("Invalid package.json")

        return {}