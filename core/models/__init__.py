"""
Public exports for the CodePilot AI domain models.
"""

from .execution import ExecutionResult
from .generation import CodeResponse, GeneratedFile
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
from .repository import RepositoryInfo
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
    "ApiEndpoint",
    "ApiTestResult",
    "BuildResult",
    "CodeResponse",
    "DependencyReport",
    "DiscoveredRoute",
    "EngineeringReport",
    "ExecutionResult",
    "GeneratedFile",
    "Plan",  # Backward compatibility
    "ProjectAnalysis",
    "ProjectPlan",
    "ProjectRequest",
    "RepositoryContext",
    "RepositoryInfo",
    "Risk",
    "RootCause",
    "RuntimeResult",
    "Summary",
    "Task",
]