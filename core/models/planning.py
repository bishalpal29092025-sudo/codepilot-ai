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
        │
        ▼
GenerationContext

The planning engine transforms a user's engineering request into a
structured implementation plan consumed by generation, verification,
execution, and reporting stages.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# Base Model
# ============================================================================


class ImmutableModel(BaseModel):
    """
    Base model for immutable planning domain objects.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )


# ============================================================================
# Enumerations
# ============================================================================


class Priority(StrEnum):
    """
    Task priority levels.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"



class Severity(StrEnum):
    """
    Risk severity levels.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"



class Complexity(StrEnum):
    """
    Implementation complexity.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"



class TaskCategory(StrEnum):
    """
    Engineering task categories.
    """

    DEPENDENCY = "dependency"

    IMPLEMENTATION = "implementation"

    CONFIGURATION = "configuration"

    REFACTOR = "refactor"

    TESTING = "testing"

    VALIDATION = "validation"

    DOCUMENTATION = "documentation"



# ============================================================================
# Request Models
# ============================================================================


class ProjectRequest(ImmutableModel):
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


class ProjectAnalysis(ImmutableModel):
    """
    Represents the planner's understanding of the repository.
    """

    project_type: str = Field(
        default="unknown",
        description="Detected project type.",
    )


    existing_features: list[str] = Field(
        default_factory=list,
        description="Existing repository capabilities.",
    )


    missing_features: list[str] = Field(
        default_factory=list,
        description="Required missing capabilities.",
    )


    affected_files: list[str] = Field(
        default_factory=list,
        description="Files likely affected.",
    )


    assumptions: list[str] = Field(
        default_factory=list,
        description="Planning assumptions.",
    )



# ============================================================================
# Task Models
# ============================================================================


class Task(ImmutableModel):
    """
    Represents a single engineering implementation task.
    """

    id: str = Field(
        ...,
        description="Unique task identifier.",
    )


    title: str = Field(
        ...,
        description="Task title.",
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
        description="Implementation complexity.",
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
        description="Task completion criteria.",
    )



# ============================================================================
# Risk Models
# ============================================================================


class Risk(ImmutableModel):
    """
    Represents an implementation risk.
    """

    title: str = Field(
        ...,
        description="Risk title.",
    )


    description: str = Field(
        ...,
        description="Risk description.",
    )


    severity: Severity = Field(
        default=Severity.MEDIUM,
        description="Risk severity.",
    )


    mitigation: str | None = Field(
        default=None,
        description="Risk mitigation strategy.",
    )



# ============================================================================
# Project Plan
# ============================================================================


class ProjectPlan(ImmutableModel):
    """
    Complete implementation blueprint produced by the planning engine.

    This model is the handoff contract between Planning and Generation.
    """

    name: str = Field(
        default="Unnamed Project",
        description="Project name.",
    )


    summary: str = Field(
        ...,
        description="High-level implementation summary.",
    )


    objective: str = Field(
        default="",
        description="Primary project objective.",
    )


    architecture: str = Field(
        default="",
        description="Architecture overview.",
    )


    coding_standards: list[str] = Field(
        default_factory=list,
        description="Coding standards to follow.",
    )


    constraints: list[str] = Field(
        default_factory=list,
        description="Implementation constraints.",
    )


    assumptions: list[str] = Field(
        default_factory=list,
        description="Planning assumptions.",
    )


    relevant_files: list[str] = Field(
        default_factory=list,
        description="Important files for implementation.",
    )


    tasks: list[Task] = Field(
        default_factory=list,
        description="Implementation tasks.",
    )


    risks: list[Risk] = Field(
        default_factory=list,
        description="Implementation risks.",
    )


    testing: list[str] = Field(
        default_factory=list,
        description="Testing strategy/checklist.",
    )


    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional planning metadata.",
    )


    # ==============================================================
    # Backward Compatibility Layer
    # ==============================================================


    @property
    def goal(self) -> str:
        """
        Compatibility with older CodePilot modules.

        Old:
            plan.goal

        New:
            plan.objective
        """

        return (
            self.objective
            if self.objective
            else self.summary
        )


    @property
    def implementation_steps(self) -> list[str]:
        """
        Compatibility with old planner/coder pipeline.

        Converts structured tasks into
        simple implementation steps.
        """

        return [
            task.description
            for task in self.tasks
        ]



# ============================================================================
# Backward Compatibility
# ============================================================================


Plan = ProjectPlan