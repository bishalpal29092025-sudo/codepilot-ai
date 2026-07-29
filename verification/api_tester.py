"""
API Tester.

Discovers API routes and validates endpoint availability.

Responsibilities:
- Discover API routes from repository
- Send HTTP requests
- Collect endpoint results
- Store API test report in AgentContext
"""

from __future__ import annotations

from pathlib import Path

from core.context import AgentContext
from core.models import ApiTestResult

from verification.http_client import HttpClient
from verification.route_discovery import RouteDiscovery


class ApiTester:
    """
    Tests discovered API endpoints.
    """

    def __init__(
        self,
        repository_path: str,
        base_url: str = "http://localhost:3000",
    ) -> None:

        self.repository_path = Path(
            repository_path
        )

        self.base_url = base_url.rstrip("/")


    # ==========================================================
    # Public API
    # ==========================================================

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Discover and test API endpoints.
        """

        self._print_header()


        # ------------------------------------------------------
        # Route Discovery
        # ------------------------------------------------------

        discovery = RouteDiscovery(
            self.repository_path
        )

        routes = discovery.discover()


        if not routes:

            print(
                "No API routes discovered."
            )

            context.api_test_result = ApiTestResult(
                total=0,
                passed=0,
                failed=0,
                endpoints=[],
            )

            return context


        # ------------------------------------------------------
        # HTTP Testing
        # ------------------------------------------------------

        client = HttpClient(
            self.base_url
        )


        endpoints = []


        for route in routes:

            result = client.request(
                route
            )

            endpoints.append(
                result
            )


        client.close()


        # ------------------------------------------------------
        # Build API Result
        # ------------------------------------------------------

        api_result = ApiTestResult(
            total=len(endpoints),

            passed=sum(
                1
                for endpoint in endpoints
                if endpoint.passed
            ),

            failed=sum(
                1
                for endpoint in endpoints
                if not endpoint.passed
            ),

            endpoints=endpoints,
        )


        context.api_test_result = api_result


        self._print_summary(
            api_result
        )


        return context


    # ==========================================================
    # Console Output
    # ==========================================================

    def _print_header(self) -> None:

        print("\n" + "=" * 70)
        print("🌐 API Tester")
        print("=" * 70)


    def _print_summary(
        self,
        result: ApiTestResult,
    ) -> None:

        print(
            f"Total     : {result.total}"
        )

        print(
            f"Passed    : {result.passed}"
        )

        print(
            f"Failed    : {result.failed}"
        )