"""
CodePilot Agent.

Main autonomous AI coding agent.

Responsible for orchestrating the complete
CodePilot execution pipeline.
"""

from __future__ import annotations


from uuid import uuid4


from core.context import AgentContext


from core.models import AgentSession


from core.explorer import RepositoryExplorer
from core.dependency_manager import DependencyManager
from core.planner import Planner
from core.reader import RepositoryReader
from core.coder import CodeGenerator
from core.executor import CodeExecutor


from execution.executor import Executor as RuntimeExecutor


from verification.verifier import Verifier


from reporting.reporter import Reporter


from agent.pipeline import Pipeline



class CodePilotAgent:
    """
    Complete CodePilot autonomous agent.

    Pipeline:

    1. Repository Exploration
    2. Dependency Analysis
    3. Planning
    4. Repository Reading
    5. Code Generation
    6. Code Writing
    7. Runtime Execution
    8. Verification
    9. Reporting
    """



    def __init__(
        self,
        repository_path: str,
    ) -> None:


        self.repository_path = repository_path



        self.pipeline = Pipeline(
            stages=[


                (
                    "Repository Exploration",
                    RepositoryExplorer(
                        repository_path
                    ),
                ),



                (
                    "Dependency Analysis",
                    DependencyManager(),
                ),



                (
                    "Planning",
                    Planner(),
                ),



                (
                    "Repository Reading",
                    RepositoryReader(
                        repository_path
                    ),
                ),



                (
                    "Code Generation",
                    CodeGenerator(),
                ),



                (
                    "Code Writing",
                    CodeExecutor(
                        repository_path
                    ),
                ),



                (
                    "Runtime Execution",
                    RuntimeExecutor(
                        repository_path
                    ),
                ),



                (
                    "Verification",
                    Verifier(
                        repository_path
                    ),
                ),



                (
                    "Reporting",
                    Reporter(),
                ),

            ]
        )



    # ==========================================================
    # Public API
    # ==========================================================

    def run(
        self,
        request: str,
    ) -> AgentContext:
        """
        Execute complete CodePilot workflow.

        Creates a new AgentSession and
        passes it through the pipeline.
        """



        session = AgentSession(

            id=str(
                uuid4()
            ),

            user_request=request,

            repository_path=self.repository_path,

        )



        context = AgentContext(

            session=session,

            user_request=request,

        )



        try:


            context = self.pipeline.run(
                context
            )


            if context.session:

                context.session.status = (
                    "completed"
                )


        except Exception as e:


            if context.session:

                context.session.status = (
                    "failed"
                )


                context.session.errors.append(
                    str(e)
                )


            raise



        return context