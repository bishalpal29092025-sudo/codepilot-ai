"""
HTTP Client.

This module provides a reusable HTTP client for API testing.

Responsibilities
----------------
- Send HTTP requests
- Measure response time
- Handle connection failures
- Return ApiEndpoint models

This client is intentionally generic so it can be reused by:

- ApiTester
- Security Scanner
- Performance Analyzer
- Future Load Testing
"""

from __future__ import annotations

import logging
import time
from typing import Any

import requests
from requests import Response
from requests import Session

from core.models import ApiEndpoint, DiscoveredRoute

logger = logging.getLogger(__name__)


class HttpClient:
    """
    Reusable HTTP client.

    Example
    -------
        client = HttpClient("http://localhost:3000")

        result = client.request(route)
    """

    DEFAULT_TIMEOUT = 10

    SUCCESS_CODES = {
        200,
        201,
        202,
        204,
        301,
        302,
        401,
        403,
        405,
    }

    def __init__(
        self,
        base_url: str,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session: Session = requests.Session()

    # ==========================================================
    # Public API
    # ==========================================================

    def request(
        self,
        route: DiscoveredRoute,
    ) -> ApiEndpoint:
        """
        Test a discovered API endpoint.

        Parameters
        ----------
        route:
            Route returned by RouteDiscovery.

        Returns
        -------
        ApiEndpoint
        """

        url = f"{self.base_url}{route.path}"

        logger.info("%s %s", route.method, url)

        start = time.perf_counter()

        try:

            response = self._send_request(
                method=route.method,
                url=url,
            )

            elapsed = time.perf_counter() - start

            return ApiEndpoint(
                method=route.method,
                path=route.path,
                status_code=response.status_code,
                response_time=round(elapsed, 3),
                passed=response.status_code in self.SUCCESS_CODES,
            )

        except requests.Timeout:

            elapsed = time.perf_counter() - start

            logger.warning(
                "Timeout while calling %s",
                url,
            )

            return ApiEndpoint(
                method=route.method,
                path=route.path,
                response_time=round(elapsed, 3),
                passed=False,
                error="Request timed out.",
            )

        except requests.ConnectionError:

            elapsed = time.perf_counter() - start

            logger.warning(
                "Connection failed: %s",
                url,
            )

            return ApiEndpoint(
                method=route.method,
                path=route.path,
                response_time=round(elapsed, 3),
                passed=False,
                error="Unable to connect to server.",
            )

        except Exception as exc:

            elapsed = time.perf_counter() - start

            logger.exception(
                "Unexpected HTTP error."
            )

            return ApiEndpoint(
                method=route.method,
                path=route.path,
                response_time=round(elapsed, 3),
                passed=False,
                error=str(exc),
            )

    # ==========================================================
    # Internal
    # ==========================================================

    def _send_request(
        self,
        method: str,
        url: str,
    ) -> Response:
        """
        Dispatch an HTTP request.
        """

        method = method.upper()

        return self.session.request(
            method=method,
            url=url,
            timeout=self.timeout,
            allow_redirects=True,
        )

    # ==========================================================
    # Convenience Methods
    # ==========================================================

    def get(
        self,
        path: str,
        **kwargs: Any,
    ) -> Response:
        return self.session.get(
            f"{self.base_url}{path}",
            timeout=self.timeout,
            **kwargs,
        )

    def post(
        self,
        path: str,
        **kwargs: Any,
    ) -> Response:
        return self.session.post(
            f"{self.base_url}{path}",
            timeout=self.timeout,
            **kwargs,
        )

    def put(
        self,
        path: str,
        **kwargs: Any,
    ) -> Response:
        return self.session.put(
            f"{self.base_url}{path}",
            timeout=self.timeout,
            **kwargs,
        )

    def patch(
        self,
        path: str,
        **kwargs: Any,
    ) -> Response:
        return self.session.patch(
            f"{self.base_url}{path}",
            timeout=self.timeout,
            **kwargs,
        )

    def delete(
        self,
        path: str,
        **kwargs: Any,
    ) -> Response:
        return self.session.delete(
            f"{self.base_url}{path}",
            timeout=self.timeout,
            **kwargs,
        )

    def head(
        self,
        path: str,
        **kwargs: Any,
    ) -> Response:
        return self.session.head(
            f"{self.base_url}{path}",
            timeout=self.timeout,
            **kwargs,
        )

    def options(
        self,
        path: str,
        **kwargs: Any,
    ) -> Response:
        return self.session.options(
            f"{self.base_url}{path}",
            timeout=self.timeout,
            **kwargs,
        )

    # ==========================================================
    # Lifecycle
    # ==========================================================

    def close(self) -> None:
        """
        Close the underlying HTTP session.
        """

        self.session.close()

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        traceback,
    ) -> None:
        self.close()