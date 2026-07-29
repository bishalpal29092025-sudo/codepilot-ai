"""
Planning domain models.

These models define the planning stage of the CodePilot AI pipeline.

Pipeline
--------
ProjectRequest
        │
        ▼
ProjectAnalysis
        │
        ▼
ProjectPlan

The planning engine transforms a user's engineering request into a structured
implementation plan that downstream components (generation, verification,
execution, reporting) can consume.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ============================================================================
# Enumerations
# ============================================================================


class Priority(str, Enum):
    """Task priority."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Severity(str, Enum):
    """Risk severity."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Complexity(str, Enum):
    """Estimated implementation complexity."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class TaskCategory(str, Enum):
    """Engineering task categories."""

    DEPENDENCY = "dependency"
    IMPLEMENTATION = "implementation"
    CONFIGURATION = "configuration"
    REFACTOR = "refactor"
    TESTING = "testing"
    DOCUMENTATION = "documentation"


# ============================================================================
# Request Models
# ============================================================================


class ProjectRequest(BaseModel):
    """
    Represents a user's engineering request.
    """

    goal: str = Field(
        ...,
        min_length=1,
        description="Primary engineering objective.",
    )

    constraints: list[str] = Field(
        default_factory=list,
        description="Constraints that must be respected.",
    )


# ============================================================================
# Analysis Models
# ============================================================================


class ProjectAnalysis(BaseModel):
    """
    Represents the planner's understanding of the repository.
    """

    project_type: str = Field(
        default="Unknown",
        description="Detected project type.",
    )

    existing_features: list[str] = Field(
        default_factory=list,
        description="Existing repository capabilities.",
    )

    missing_features: list[str] = Field(
        default_factory=list,
        description="Features required to satisfy the request.",
    )

    affected_files: list[str] = Field(
        default_factory=list,
        description="Files likely to require modification.",
    )

    assumptions: list[str] = Field(
        default_factory=list,
        description="Planning assumptions.",
    )


# ============================================================================
# Planning Models
# ============================================================================


class Task(BaseModel):
    """
    Represents a single engineering task.
    """

    id: str = Field(
        ...,
        description="Unique task identifier.",
    )

    title: str = Field(
        ...,
        description="Short task title.",
    )

    description: str = Field(
        ...,
        description="Detailed task description.",
    )

    category: TaskCategory = Field(
        default=TaskCategory.IMPLEMENTATION,
        description="Task category.",
    )

    priority: Priority = Field(
        default=Priority.MEDIUM,
        description="Task priority.",
    )

    complexity: Complexity = Field(
        default=Complexity.MEDIUM,
        description="Estimated implementation complexity.",
    )

    affected_files: list[str] = Field(
        default_factory=list,
        description="Files affected by this task.",
    )

    dependencies: list[str] = Field(
        default_factory=list,
        description="Task dependencies.",
    )

    acceptance_criteria: list[str] = Field(
        default_factory=list,
        description="Acceptance criteria for task completion.",
    )


class Risk(BaseModel):
    """
    Represents an implementation risk.
    """

    title: str = Field(
        ...,
        description="Risk title.",
    )

    description: str = Field(
        ...,
        description="Detailed description of the risk.",
    )

    severity: Severity = Field(
        default=Severity.MEDIUM,
        description="Risk severity.",
    )

    mitigation: str | None = Field(
        default=None,
        description="Recommended mitigation strategy.",
    )


class ProjectPlan(BaseModel):
    """
    Final implementation plan produced by the planning engine.
    """

    summary: str = Field(
        ...,
        description="High-level implementation summary.",
    )

    tasks: list[Task] = Field(
        default_factory=list,
        description="Engineering tasks.",
    )

    risks: list[Risk] = Field(
        default_factory=list,
        description="Implementation risks.",
    )

    testing: list[str] = Field(
        default_factory=list,
        description="Testing checklist.",
    )


# ============================================================================
# Backward Compatibility
# ============================================================================

Plan = ProjectPlan