"""
Execution Sandbox.

Provides isolated workspace management
for running generated code safely.
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path


class Sandbox:
    """
    Manages isolated execution environments.

    Responsibilities:

    - Create temporary workspace
    - Copy project files when required
    - Cleanup after execution
    """

    def __init__(
        self,
        base_directory: str | None = None,
    ) -> None:

        self.base_directory = (
            Path(base_directory)
            if base_directory
            else None
        )

        self.workspace: Path | None = None


    # ==========================================================
    # Public API
    # ==========================================================

    def create(
        self,
    ) -> Path:
        """
        Create isolated workspace.
        """

        self.workspace = Path(
            tempfile.mkdtemp(
                prefix="codepilot_sandbox_",
                dir=self.base_directory,
            )
        )

        return self.workspace


    def copy_project(
        self,
        source: str | Path,
    ) -> Path:
        """
        Copy repository into sandbox.
        """

        if self.workspace is None:
            self.create()


        source_path = Path(
            source
        )

        destination = (
            self.workspace
            / source_path.name
        )


        shutil.copytree(
            source_path,
            destination,
            dirs_exist_ok=True,
        )


        return destination


    def cleanup(
        self,
    ) -> None:
        """
        Remove sandbox workspace.
        """

        if (
            self.workspace
            and self.workspace.exists()
        ):

            shutil.rmtree(
                self.workspace,
                ignore_errors=True,
            )

            self.workspace = None


    # ==========================================================
    # Context Manager Support
    # ==========================================================

    def __enter__(self) -> "Sandbox":

        self.create()

        return self


    def __exit__(
        self,
        exc_type,
        exc,
        traceback,
    ) -> None:

        self.cleanup()