"""
Git Safety Patch Engine.

Responsible for:
- Creating patches
- Validating patches
- Applying patches safely
"""

from __future__ import annotations

from pathlib import Path

from git_safety.models import (
    FilePatch,
    PatchOperation,
    PatchSet,
)


class PatchError(Exception):
    """
    Patch operation error.
    """

    pass



class PatchEngine:
    """
    Safe patch application engine.

    Workflow:

    Create Patch
          |
          v
    Validate Patch
          |
          v
    Apply Patch
    """


    def __init__(
        self,
        repository_path: str,
    ) -> None:

        self.repository_path = Path(
            repository_path
        ).resolve()



    # ==========================================================
    # Create Patch
    # ==========================================================

    def create_patch(
        self,
        file_path: str,
        new_content: str,
    ) -> FilePatch:
        """
        Create a patch from a file change.
        """

        path = self._resolve_path(
            file_path
        )


        if path.exists():

            return FilePatch(
                file_path=file_path,
                operation=PatchOperation.MODIFY,
                old_content=path.read_text(
                    encoding="utf-8"
                ),
                new_content=new_content,
            )


        return FilePatch(
            file_path=file_path,
            operation=PatchOperation.CREATE,
            old_content="",
            new_content=new_content,
        )



    # ==========================================================
    # Validation
    # ==========================================================

    def validate_patch(
        self,
        patch: FilePatch,
    ) -> bool:
        """
        Validate patch safety.
        """

        path = self._resolve_path(
            patch.file_path
        )


        if patch.operation == PatchOperation.MODIFY:

            if not path.exists():

                raise PatchError(
                    "Cannot modify missing file."
                )


        if patch.operation == PatchOperation.DELETE:

            if not path.exists():

                raise PatchError(
                    "Cannot delete missing file."
                )


        return True



    # ==========================================================
    # Apply Patch
    # ==========================================================

    def apply_patch(
        self,
        patch: FilePatch,
    ) -> None:
        """
        Apply single file patch.
        """

        self.validate_patch(
            patch
        )


        path = self._resolve_path(
            patch.file_path
        )


        if patch.operation in (
            PatchOperation.CREATE,
            PatchOperation.MODIFY,
        ):

            path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )


            path.write_text(
                patch.new_content,
                encoding="utf-8",
            )


        elif patch.operation == PatchOperation.DELETE:

            path.unlink()



    def apply_patch_set(
        self,
        patch_set: PatchSet,
    ) -> None:
        """
        Apply multiple patches.
        """

        for patch in patch_set.patches:

            self.apply_patch(
                patch
            )



    # ==========================================================
    # Security
    # ==========================================================

    def _resolve_path(
        self,
        file_path: str,
    ) -> Path:
        """
        Prevent writing outside repository.
        """

        path = (
            self.repository_path
            /
            file_path
        ).resolve()


        if not str(path).startswith(
            str(self.repository_path)
        ):

            raise PatchError(
                "Unsafe path detected."
            )


        return path