"""
Dependency context builder.

Transforms dependency information into an immutable
Generation DependencyContext.

This builder only prepares dependency data for code
generation. It does not install or resolve packages.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from core.models.generation import DependencyContext


class DependencyContextBuilder:
    """
    Builds DependencyContext objects.
    """

    def build(
        self,
        *,
        internal_modules: list[str] | None = None,
        external_packages: list[str] | None = None,
        related_files: list[str] | None = None,
        imports: list[str] | None = None,
        dependency_graph: dict[str, list[str]] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DependencyContext:
        """
        Build immutable DependencyContext.

        Args:
            internal_modules:
                Internal project modules.

            external_packages:
                External dependencies.

            related_files:
                Files related to the task.

            imports:
                Required imports.

            dependency_graph:
                Dependency relationship map.

            metadata:
                Additional dependency metadata.

        Returns:
            DependencyContext instance.
        """

        return DependencyContext(
            internal_modules=self._normalize(
                internal_modules
            ),
            external_packages=self._normalize(
                external_packages
            ),
            related_files=self._normalize(
                related_files
            ),
            imports=self._normalize(
                imports
            ),
            dependency_graph=self._normalize_graph(
                dependency_graph
            ),
            metadata=self._build_metadata(
                metadata
            ),
        )

    # =========================================================
    # Helpers
    # =========================================================

    @staticmethod
    def _normalize(
        values: list[str] | None,
    ) -> list[str]:
        """
        Normalize string collections.
        """

        if not values:
            return []

        return sorted(
            {
                value.strip()
                for value in values
                if value.strip()
            }
        )

    @staticmethod
    def _normalize_graph(
        graph: dict[str, list[str]] | None,
    ) -> dict[str, list[str]]:
        """
        Normalize dependency graph.
        """

        if not graph:
            return {}

        return {
            key.strip(): sorted(
                {
                    item.strip()
                    for item in values
                    if item.strip()
                }
            )
            for key, values in graph.items()
        }

    @staticmethod
    def _build_metadata(
        metadata: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """
        Preserve dependency metadata.
        """

        return deepcopy(
            metadata or {}
        )