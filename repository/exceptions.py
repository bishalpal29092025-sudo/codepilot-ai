"""
Repository package exceptions.
"""


class RepositoryError(Exception):
    """Base exception for repository operations."""


class RepositoryScanError(RepositoryError):
    """Raised when repository scanning fails."""


class RepositoryDetectionError(RepositoryError):
    """Raised when project detection fails."""