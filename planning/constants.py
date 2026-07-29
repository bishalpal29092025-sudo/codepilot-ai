"""
Planning configuration.

This module contains configuration values used by the planning package.
It intentionally contains no business logic. Strategies and services should
consume these values rather than hardcoding planning rules.

The configuration is designed to be deterministic, testable and easy to
extend as CodePilot AI evolves.
"""

from __future__ import annotations

from core.models import (
    Complexity,
    Priority,
    TaskCategory,
)

# =============================================================================
# Category Keywords
# =============================================================================

CATEGORY_KEYWORDS: dict[TaskCategory, tuple[str, ...]] = {
    TaskCategory.IMPLEMENTATION: (
        "implement",
        "add",
        "create",
        "build",
        "develop",
        "feature",
        "endpoint",
        "module",
        "function",
        "logic",
    ),
    TaskCategory.REFACTOR: (
        "refactor",
        "cleanup",
        "clean",
        "optimize",
        "simplify",
        "improve",
        "restructure",
        "rewrite",
        "rename",
    ),
    TaskCategory.CONFIGURATION: (
        "config",
        "configuration",
        "configure",
        "environment",
        "env",
        "settings",
        "setup",
        "initialize",
        "init",
    ),
    TaskCategory.DEPENDENCY: (
        "dependency",
        "dependencies",
        "install",
        "package",
        "library",
        "framework",
        "upgrade",
        "downgrade",
    ),
    TaskCategory.TESTING: (
        "test",
        "testing",
        "unit test",
        "integration test",
        "e2e",
        "coverage",
        "pytest",
        "jest",
        "vitest",
    ),
    TaskCategory.DOCUMENTATION: (
        "documentation",
        "document",
        "docs",
        "readme",
        "guide",
        "tutorial",
        "comment",
        "api docs",
    ),
}

# =============================================================================
# Complexity Keywords
# =============================================================================

COMPLEXITY_KEYWORDS: dict[Complexity, tuple[str, ...]] = {
    Complexity.VERY_HIGH: (
        "authentication",
        "authorization",
        "oauth",
        "jwt",
        "payment",
        "billing",
        "microservice",
        "distributed",
        "security",
        "encryption",
        "kubernetes",
    ),
    Complexity.HIGH: (
        "database",
        "migration",
        "docker",
        "cache",
        "redis",
        "api",
        "graphql",
        "queue",
        "websocket",
        "background job",
    ),
    Complexity.MEDIUM: (
        "frontend",
        "dashboard",
        "component",
        "ui",
        "crud",
        "form",
        "upload",
        "search",
        "pagination",
    ),
    Complexity.LOW: (
        "documentation",
        "readme",
        "comment",
        "style",
        "format",
        "lint",
        "typo",
    ),
}

# =============================================================================
# File Complexity Thresholds
# =============================================================================

FILE_COMPLEXITY_THRESHOLDS: dict[Complexity, int] = {
    Complexity.VERY_HIGH: 15,
    Complexity.HIGH: 10,
    Complexity.MEDIUM: 5,
    Complexity.LOW: 2,
}

# =============================================================================
# Project Complexity Modifiers
# =============================================================================

PROJECT_COMPLEXITY_SCORES: dict[str, int] = {
    "microservice": 3,
    "distributed": 3,
    "full stack": 2,
    "rest api": 2,
    "graphql": 2,
    "backend": 2,
    "frontend": 1,
    "library": 1,
    "cli": 1,
}

# =============================================================================
# Risk Thresholds
# =============================================================================

RISK_THRESHOLDS: dict[str, int] = {
    "large_change": 10,
    "critical_change": 20,
}

# =============================================================================
# Acceptance Criteria
# =============================================================================

DEFAULT_ACCEPTANCE_CRITERIA: tuple[str, ...] = (
    "Project builds successfully.",
    "Existing functionality remains unaffected.",
)

CATEGORY_ACCEPTANCE_CRITERIA: dict[TaskCategory, tuple[str, ...]] = {
    TaskCategory.IMPLEMENTATION: (
        "Implementation satisfies the requested behaviour.",
        "Public interfaces remain consistent.",
    ),
    TaskCategory.REFACTOR: (
        "Behaviour remains unchanged.",
        "Code quality is improved.",
    ),
    TaskCategory.CONFIGURATION: (
        "Configuration is valid.",
        "Application starts successfully.",
    ),
    TaskCategory.DEPENDENCY: (
        "Required dependency is installed.",
        "Dependency is correctly configured.",
    ),
    TaskCategory.TESTING: (
        "All new tests pass.",
        "Existing tests continue to pass.",
    ),
    TaskCategory.DOCUMENTATION: (
        "Documentation accurately reflects implementation.",
        "Examples are correct and up to date.",
    ),
}

# =============================================================================
# Testing Checklist
# =============================================================================

DEFAULT_TESTING_CHECKLIST: tuple[str, ...] = (
    "Run the project's automated test suite.",
    "Verify the modified functionality.",
    "Review code quality and formatting.",
)

# =============================================================================
# Planner Defaults
# =============================================================================

DEFAULT_PRIORITY: Priority = Priority.MEDIUM

DEFAULT_COMPLEXITY: Complexity = Complexity.MEDIUM

MAX_TASKS: int = 100

MAX_RISKS: int = 20

# =============================================================================
# Summary Templates
# =============================================================================

SUMMARY_TEMPLATE = (
    "{project_type}: "
    "{feature_count} planned feature(s), "
    "{affected_files} affected file(s), "
    "estimated overall complexity: {complexity}."
)

# =============================================================================
# Miscellaneous
# =============================================================================

DEFAULT_TASK_PREFIX = "TASK"

DEFAULT_RISK_TITLE = "Planning Risk"

DEFAULT_SUMMARY = "No implementation work identified."