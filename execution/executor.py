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

    Responsibilities:

    - Prepare environment
    - Execute generated commands
    - Collect execution results
    - Store result inside AgentContext

    Pipeline compatible:
        run(context) -> context
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
    # Pipeline API
    # ==========================================================

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Pipeline entry point.

        Executes generated project commands
        and stores result in context.
        """

        commands = self._get_commands(
            context
        )


        result = self.execute(
            context,
            commands,
        )


        context.execution_result = result


        return context


    # ==========================================================
    # Command Selection
    # ==========================================================

    def _get_commands(
        self,
        context: AgentContext,
    ) -> list[str]:
        """
        Decide which commands should be executed.
        """

        commands = []


        if context.dependency_report:

            if (
                context.dependency_report.build_command
            ):
                commands.append(
                    context.dependency_report.build_command
                )


        # fallback for demo projects

        if not commands:

            commands.append(
                "npm run build"
            )


        return commands


    # ==========================================================
    # Execution Engine
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

            self.environment.prepare(
                context
            )


            self.sandbox.create()


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


            return ExecutionResult(
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


    def _print_header(self):

        print("\n" + "=" * 70)
        print("⚡ Runtime Execution Engine")
        print("=" * 70)