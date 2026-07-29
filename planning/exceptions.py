"""
Custom exceptions for the planning package.
"""

from __future__ import annotations


class PlanningError(Exception):
    """
    Base exception for all planning-related errors.
    """


class PlanningAnalysisError(PlanningError):
    """
    Raised when project analysis cannot be completed.
    """


class PlanningValidationError(PlanningError):
    """
    Raised when a generated project plan is invalid.
    """


class UnsupportedProjectError(PlanningAnalysisError):
    """
    Raised when the repository type is unsupported.
    """


class UnsupportedRequestError(PlanningAnalysisError):
    """
    Raised when the user's request cannot be analysed.
    """