"""
Repository context builder.

Transforms a RepositoryInfo domain model into a Generation
RepositoryContext. This builder performs no repository analysis
or filesystem operations. It is responsible only for
normalisation and model construction.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from core.models.generation import RepositoryContext
from core.models.repository import RepositoryInfo


class RepositoryContextBuilder:
    """
    Builds RepositoryContext instances from RepositoryInfo.

    Responsibilities:
        - Normalize repository metadata
        - Remove duplicate framework names
        - Build immutable RepositoryContext models

    Does NOT:
        - Scan repositories
        - Detect frameworks
        - Read files
        - Invoke LLMs
    """

    def build(
        self,
        repository: RepositoryInfo,
    ) -> RepositoryContext:
        """
        Convert RepositoryInfo into RepositoryContext.

        Args:
            repository:
                Repository metadata produced by the repository
                exploration stage.

        Returns:
            Immutable RepositoryContext.
        """

        return RepositoryContext(
            name=repository.name,
            root_path=repository.root_path,
            project_type=repository.project_type,
            primary_language=repository.primary_language,
            frameworks=self._normalize_frameworks(
                repository.frameworks
            ),
            entry_points=sorted(set(repository.entry_points)),
            source_directories=sorted(
                set(repository.source_directories)
            ),
            ignored_directories=sorted(
                set(repository.ignored_directories)
            ),
            repository_files=sorted(
                set(repository.repository_files)
            ),
            metadata=self._build_metadata(repository),
        )

    # ---------------------------------------------------------
    # Private Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _normalize_frameworks(
        frameworks: list[str],
    ) -> list[str]:
        """
        Normalize framework names.

        - Remove empty values
        - Trim whitespace
        - Remove duplicates
        - Return sorted list
        """

        cleaned = {
            framework.strip()
            for framework in frameworks
            if framework.strip()
        }

        return sorted(cleaned)

    @staticmethod
    def _build_metadata(
        repository: RepositoryInfo,
    ) -> dict[str, Any]:
        """
        Build metadata passed into GenerationContext.

        Existing metadata is preserved while repository
        statistics are added.
        """

        metadata = deepcopy(repository.metadata)

        metadata.update(
            {
                "database": repository.database,
                "package_manager": repository.package_manager,
                "total_files": repository.total_files,
            }
        )

        return metadata