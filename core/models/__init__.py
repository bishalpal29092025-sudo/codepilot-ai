"""
Public exports for the CodePilot AI domain models.
"""


from .execution import ExecutionResult


from .generation import (
    CodeResponse,
    GeneratedFile,
)


from .planning import (
    Plan,
    ProjectAnalysis,
    ProjectPlan,
    ProjectRequest,
    Risk,
    Task,
)


from .reading import RepositoryContext


from .reporting import Summary


from .repository import (
    RepositoryInfo,
    ProgrammingLanguage,
    ProjectType,
)


from .session import AgentSession


from .verification import (
    ApiEndpoint,
    ApiTestResult,
    BuildResult,
    DependencyReport,
    DiscoveredRoute,
    EngineeringReport,
    RootCause,
    RuntimeResult,
)



__all__ = [

    # Execution
    "ExecutionResult",


    # Generation
    "CodeResponse",
    "GeneratedFile",


    # Planning
    "Plan",
    "ProjectAnalysis",
    "ProjectPlan",
    "ProjectRequest",
    "Risk",
    "Task",


    # Repository
    "RepositoryContext",
    "RepositoryInfo",
    "ProgrammingLanguage",
    "ProjectType",


    # Session
    "AgentSession",


    # Reporting
    "Summary",


    # Verification
    "ApiEndpoint",
    "ApiTestResult",
    "BuildResult",
    "DependencyReport",
    "DiscoveredRoute",
    "EngineeringReport",
    "RootCause",
    "RuntimeResult",
]