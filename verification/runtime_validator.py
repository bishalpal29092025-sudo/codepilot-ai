"""
Runtime Validator.

Validates that the application starts successfully.

Strategy:

1. Start application process
2. Wait for startup
3. Analyse startup logs
4. Detect runtime failures
5. Stop process safely
6. Store RuntimeResult
"""

from __future__ import annotations


import time
from pathlib import Path


from core.context import AgentContext
from core.models import RuntimeResult

from services.process_runner import ProcessRunner



class RuntimeValidator:
    """
    Validates application runtime startup.
    """


    STARTUP_WAIT_SECONDS = 5



    def __init__(
        self,
        repository_path: str,
    ) -> None:


        self.repository_path = Path(
            repository_path
        )


        self.runner = ProcessRunner()



    # ==========================================================
    # Public API
    # ==========================================================

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:


        self._print_header()


        report = context.dependency_report


        if report is None:

            raise ValueError(
                "Dependency report is missing."
            )



        if not report.run_command:


            result = RuntimeResult(
                success=False,
                command="",
                logs="",
                errors=[
                    "No runtime command detected."
                ],
            )


            context.runtime_result = result


            self._print_summary(
                result
            )


            return context



        print(
            f"Starting application: {report.run_command}"
        )



        process = None


        try:


            process = self.runner.start(
                command=report.run_command,
                cwd=self.repository_path,
            )



            print(
                "Waiting for application startup..."
            )


            time.sleep(
                self.STARTUP_WAIT_SECONDS
            )



            stdout = getattr(
                process,
                "stdout",
                "",
            )


            stderr = getattr(
                process,
                "stderr",
                "",
            )



            errors = self._extract_errors(
                stderr
            )



            success = self._detect_startup_success(
                stdout
            )



            if errors:

                success = False



            result = RuntimeResult(

                success=success,

                command=report.run_command,

                logs=stdout,

                errors=errors,

            )



            context.runtime_result = result



            self._print_summary(
                result
            )



            return context



        finally:


            self._stop_process(
                process
            )



    # ==========================================================
    # Startup Detection
    # ==========================================================

    def _detect_startup_success(
        self,
        stdout: str,
    ) -> bool:


        if not stdout:

            return False



        keywords = [

            "ready",

            "started",

            "running",

            "listening",

            "compiled",

            "success",

            "local:",

            "localhost",

        ]



        output = stdout.lower()



        return any(

            keyword in output

            for keyword in keywords

        )



    # ==========================================================
    # Error Extraction
    # ==========================================================

    def _extract_errors(
        self,
        stderr: str,
    ) -> list[str]:


        if not stderr:

            return []



        ignored = [

            "warning",

            "deprecated",

        ]



        errors = []



        for line in stderr.splitlines():


            clean = line.strip()


            if not clean:

                continue



            if any(

                word in clean.lower()

                for word in ignored

            ):

                continue



            errors.append(
                clean
            )



        return errors



    # ==========================================================
    # Process Cleanup
    # ==========================================================

    def _stop_process(
        self,
        process,
    ) -> None:


        if process is None:

            return



        try:


            if hasattr(
                process,
                "terminate",
            ):

                process.terminate()



        except Exception as e:


            print(
                f"⚠️ Process cleanup failed: {e}"
            )



    # ==========================================================
    # Console
    # ==========================================================

    def _print_header(self) -> None:


        print("\n" + "=" * 70)

        print("🚀 Runtime Validator")

        print("=" * 70)



    def _print_summary(
        self,
        result: RuntimeResult,
    ) -> None:


        print(
            f"Command : {result.command}"
        )


        print(
            f"Success : {result.success}"
        )


        print(
            f"Errors  : {len(result.errors)}"
        )