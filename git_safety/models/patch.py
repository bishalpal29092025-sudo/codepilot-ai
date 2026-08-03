"""
Patch Models.

Defines structures used by CodePilot
to safely apply file changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PatchOperation(str, Enum):
    """
    Type of file operation.
    """

    CREATE = "create"

    MODIFY = "modify"

    DELETE = "delete"



@dataclass(frozen=True)
class FilePatch:
    """
    Represents a single file change.
    """

    file_path: str

    operation: PatchOperation

    old_content: str = ""

    new_content: str = ""



@dataclass(frozen=True)
class PatchSet:
    """
    Collection of file patches.
    """

    patches: list[FilePatch]
