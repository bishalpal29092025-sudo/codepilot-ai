"""
API Tester.

Discovers API routes and validates endpoint availability.

Responsibilities:
- Discover API routes
- Detect running application
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
    Tests discovered application endpoints.
    """



    DEFAULT_PORTS = [
        3000,
        5173,
        8000,
        5000,
    ]



    def __init__(
        self,
        repository_path: str,
        base_url: str | None = None,
    ) -> None:


        self.repository_path = Path(
            repository_path
        )


        self.base_url = base_url



    # ==========================================================
    # Public API
    # ==========================================================

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:


        self._print_header()



        if self.base_url is None:

            self.base_url = (
                self._detect_base_url()
            )



        print(
            f"Base URL : {self.base_url}"
        )



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




        client = HttpClient(
            self.base_url
        )



        endpoints = []



        for route in routes:


            try:


                result = client.request(
                    route
                )


                endpoints.append(
                    result
                )



            except Exception as e:


                print(
                    f"❌ Failed: {route.path}"
                )


                endpoints.append(

                    self._failed_endpoint(
                        route,
                        str(e),
                    )

                )



        client.close()



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
    # URL Detection
    # ==========================================================

    def _detect_base_url(
        self,
    ) -> str:


        runtime = getattr(
            self,
            "_runtime_result",
            None,
        )


        for port in self.DEFAULT_PORTS:

            url = (
                f"http://localhost:{port}"
            )


            if self._check_port(
                port
            ):

                return url



        return "http://localhost:3000"




    def _check_port(
        self,
        port: int,
    ) -> bool:


        import socket


        sock = socket.socket()


        sock.settimeout(
            0.5
        )


        try:

            sock.connect(
                (
                    "localhost",
                    port,
                )
            )

            return True


        except Exception:

            return False


        finally:

            sock.close()



    # ==========================================================
    # Failure Builder
    # ==========================================================

    def _failed_endpoint(
        self,
        route,
        error: str,
    ):


        return {

            "path": route.path,

            "passed": False,

            "error": error,

        }



    # ==========================================================
    # Console
    # ==========================================================

    def _print_header(
        self,
    ) -> None:


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