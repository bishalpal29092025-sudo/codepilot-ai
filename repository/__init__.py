"""
Repository Intelligence Package.

Public API for repository analysis.

This package provides components responsible for scanning,
reading, detecting, and exploring software repositories.
"""

from __future__ import annotations

from repository.file_reader import RepositoryFileReader
from repository.scanner import RepositoryScanner

__all__ = [
    "RepositoryScanner",
    "RepositoryFileReader",
]