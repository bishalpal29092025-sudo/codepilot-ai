"""
Execution Engine.

Coordinates environment preparation,
sandbox management and command execution.
"""

from __future__ import annotations

from pathlib import Path

from core.context import AgentContext

from execution.environment.manager import EnvironmentManager
from execution.models.command_result import CommandResult
from execution.models.execution_result import (
    ExecutionResult,
    ExecutionStatus,
)
from execution.runner.command_runner import CommandRunner
from execution.sandbox.sandbox import Sandbox


class Executor:
    """
    Main execution orchestrator.
    """

    def __init__(
        self,
        repository_path: str,
    ) -> None:

        self.repository_path = Path(
            repository_path
        )

        self.environment = EnvironmentManager(
            repository_path
        )

        self.runner = CommandRunner()

        self.sandbox = Sandbox()


    # ==========================================================
    # Public API
    # ==========================================================

    def execute(
        self,
        context: AgentContext,
        commands: list[str],
    ) -> ExecutionResult:
        """
        Execute verified commands.
        """

        self._print_header()


        results: list[CommandResult] = []


        try:

            # Prepare environment

            context = (
                self.environment.prepare(
                    context
                )
            )


            # Create sandbox

            workspace = (
                self.sandbox.create()
            )


            for command in commands:

                result = self.runner.run(
                    command=command,
                    cwd=self.repository_path,
                )


                results.append(
                    result
                )


                if not result.success:
                    break



            success = all(
                result.success
                for result in results
            )


            execution_result = ExecutionResult(
                status=(
                    ExecutionStatus.SUCCESS
                    if success
                    else ExecutionStatus.FAILED
                ),
                success=success,
                commands=results,
                logs=self._collect_logs(
                    results
                ),
                errors=self._collect_errors(
                    results
                ),
                summary=(
                    "Execution completed successfully."
                    if success
                    else
                    "Execution failed."
                ),
            )


            return execution_result


        finally:

            self.sandbox.cleanup()



    # ==========================================================
    # Helpers
    # ==========================================================

    def _collect_logs(
        self,
        results: list[CommandResult],
    ) -> str:

        return "\n".join(
            result.stdout
            for result in results
            if result.stdout
        )


    def _collect_errors(
        self,
        results: list[CommandResult],
    ) -> list[str]:

        return [
            result.stderr
            for result in results
            if result.stderr
        ]


    def _print_header(self) -> None:

        print("\n" + "=" * 70)
        print("⚡ CodePilot Execution Engine")
        print("=" * 70)