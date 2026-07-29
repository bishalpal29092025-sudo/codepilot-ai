"""
Repository package exceptions.
"""

from __future__ import annotations


class RepositoryError(Exception):
    """
    Base exception for all repository-related operations.
    """


class RepositoryScanError(RepositoryError):
    """
    Raised when repository scanning fails.
    """


class RepositoryReadError(RepositoryError):
    """
    Raised when reading repository files fails.
    """


class RepositoryDetectionError(RepositoryError):
    """
    Raised when repository detection fails.
    """