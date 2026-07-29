"""
Route Discovery Module.

This module is responsible for discovering API endpoints from a repository.

Version 1 supports:
- Next.js App Router

Future versions will support:
- Express.js
- FastAPI
- Flask
- Django
- Spring Boot
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from core.models import DiscoveredRoute

logger = logging.getLogger(__name__)


class RouteDiscovery:
    """
    Discovers API routes inside a repository.

    The discovery process is framework-aware. Each supported framework
    has its own discovery method while exposing a single public API.

    Example:
        >>> discovery = RouteDiscovery("/projects/my-app")
        >>> routes = discovery.discover()

    Returns:
        List[DiscoveredRoute]
    """

    HTTP_METHODS = (
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "HEAD",
        "OPTIONS",
    )

    def __init__(self, repository_path: str | Path):
        self.repository_path = Path(repository_path)

    # ==========================================================
    # Public API
    # ==========================================================

    def discover(self) -> list[DiscoveredRoute]:
        """
        Discover all API routes supported by the repository.

        Returns
        -------
        list[DiscoveredRoute]
            List of discovered routes.
        """

        logger.info("Starting route discovery...")

        routes: list[DiscoveredRoute] = []

        routes.extend(self._discover_nextjs_routes())

        routes = self._remove_duplicates(routes)

        logger.info("Discovered %d API route(s).", len(routes))

        return sorted(
            routes,
            key=lambda route: (route.path, route.method),
        )

    # ==========================================================
    # Next.js Discovery
    # ==========================================================

    def _discover_nextjs_routes(self) -> list[DiscoveredRoute]:
        """
        Discover routes from Next.js App Router.

        Example:

            app/
                api/
                    users/
                        route.ts

        becomes

            GET /api/users
        """

        api_root = self.repository_path / "app" / "api"

        if not api_root.exists():
            logger.debug("No Next.js App Router detected.")
            return []

        routes: list[DiscoveredRoute] = []

        for route_file in api_root.rglob("route.ts"):

            try:
                methods = self._extract_http_methods(route_file)

                relative = route_file.relative_to(api_root)

                route_path = self._build_route_path(relative)

                for method in methods:

                    routes.append(
                        DiscoveredRoute(
                            method=method,
                            path=route_path,
                            source_file=str(route_file),
                        )
                    )

            except Exception:
                logger.exception(
                    "Failed to parse route file: %s",
                    route_file,
                )

        return routes

    # ==========================================================
    # Helpers
    # ==========================================================

    def _extract_http_methods(
        self,
        route_file: Path,
    ) -> list[str]:
        """
        Parse exported HTTP methods from a route.ts file.

        Example:

            export async function GET() {}
            export async function POST() {}

        Returns:

            ["GET", "POST"]
        """

        try:

            content = route_file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        except OSError:

            logger.warning(
                "Unable to read %s",
                route_file,
            )

            return ["GET"]

        discovered: list[str] = []

        for method in self.HTTP_METHODS:

            pattern = (
                rf"export\s+"
                rf"(?:async\s+)?"
                rf"function\s+{method}\s*\("
            )

            if re.search(pattern, content):
                discovered.append(method)

        if not discovered:
            logger.debug(
                "No exported HTTP methods found in %s. "
                "Defaulting to GET.",
                route_file,
            )
            discovered.append("GET")

        return discovered

    def _build_route_path(
        self,
        relative_path: Path,
    ) -> str:
        """
        Convert a route.ts file path into an API route.

        Example:

            users/route.ts

        →

            /api/users

        Example:

            posts/[id]/route.ts

        →

            /api/posts/{id}
        """

        parent = str(relative_path.parent)

        if parent == ".":
            return "/api"

        parent = parent.replace("\\", "/")

        parent = re.sub(
            r"\[(.+?)\]",
            r"{\1}",
            parent,
        )

        return f"/api/{parent}"

    def _remove_duplicates(
        self,
        routes: list[DiscoveredRoute],
    ) -> list[DiscoveredRoute]:
        """
        Remove duplicated routes.
        """

        unique: dict[tuple[str, str], DiscoveredRoute] = {}

        for route in routes:
            unique[(route.method, route.path)] = route

        return list(unique.values())