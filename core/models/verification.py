"""
Verification domain models.

These models describe the verification phase of the CodePilot AI pipeline,
including dependency analysis, build validation, runtime validation,
API testing, root cause analysis, and the final engineering report.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from core.models.reporting import Summary
from core.models.repository import RepositoryInfo


class DependencyReport(BaseModel):
    """
    Repository dependency and build configuration.
    """

    language: str = Field(
        default="Unknown",
        description="Detected programming language.",
    )

    framework: str = Field(
        default="Unknown",
        description="Detected application framework.",
    )

    package_manager: str = Field(
        default="Unknown",
        description="Detected package manager.",
    )

    install_command: str | None = Field(
        default=None,
        description="Command used to install dependencies.",
    )

    build_command: str | None = Field(
        default=None,
        description="Command used to build the project.",
    )

    run_command: str | None = Field(
        default=None,
        description="Command used to start the application.",
    )

    detected_files: list[str] = Field(
        default_factory=list,
        description="Configuration files used during dependency detection.",
    )

    warnings: list[str] = Field(
        default_factory=list,
        description="Repository warnings.",
    )


class BuildResult(BaseModel):
    """
    Result of building the project.
    """

    success: bool = False

    command: str = ""

    exit_code: int = 0

    duration: float = 0.0

    logs: str = ""

    errors: list[str] = Field(default_factory=list)


class RuntimeResult(BaseModel):
    """
    Result of starting the application.
    """

    success: bool = False

    command: str = ""

    duration: float = 0.0

    logs: str = ""

    errors: list[str] = Field(default_factory=list)


class DiscoveredRoute(BaseModel):
    """
    Route discovered before API testing.
    """

    method: str

    path: str

    source_file: str


class ApiEndpoint(BaseModel):
    """
    Result of testing a single API endpoint.
    """

    method: str

    path: str

    status_code: int | None = None

    response_time: float | None = None

    passed: bool = False

    error: str | None = None


class ApiTestResult(BaseModel):
    """
    API testing report.
    """

    total: int = 0

    passed: int = 0

    failed: int = 0

    duration: float = 0.0

    endpoints: list[ApiEndpoint] = Field(default_factory=list)


class RootCause(BaseModel):
    """
    AI-generated root cause analysis.
    """

    summary: str = ""

    probable_causes: list[str] = Field(default_factory=list)

    suggested_fixes: list[str] = Field(default_factory=list)

    confidence: float = 0.0


class EngineeringReport(BaseModel):
    """
    Final engineering report produced after the verification pipeline.
    """

    generated_at: datetime = Field(default_factory=datetime.utcnow)

    repository: RepositoryInfo | None = None

    dependency: DependencyReport | None = None

    build: BuildResult | None = None

    runtime: RuntimeResult | None = None

    api: ApiTestResult | None = None

    root_cause: RootCause | None = None

    summary: Summary | None = None