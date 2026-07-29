"""
Generation validator.

Validates generated code before it is written
into the repository.
"""

from __future__ import annotations

import ast
from pathlib import Path

from core.models.generation import CodeResponse


class GenerationValidator:
    """
    Validates generated code output.
    """

    # =========================================================
    # Public API
    # =========================================================

    def validate(
        self,
        response: CodeResponse,
    ) -> bool:
        """
        Validate generated response.

        Args:
            response:
                Generated code response.

        Returns:
            True if valid.

        Raises:
            ValueError:
                If validation fails.
        """

        self._validate_empty_response(
            response
        )

        self._validate_duplicates(
            response
        )

        self._validate_files(
            response
        )

        return True

    # =========================================================
    # Validation Rules
    # =========================================================

    @staticmethod
    def _validate_empty_response(
        response: CodeResponse,
    ) -> None:
        """
        Ensure files exist.
        """

        if not response.files:
            raise ValueError(
                "Generation response contains no files."
            )

    @staticmethod
    def _validate_duplicates(
        response: CodeResponse,
    ) -> None:
        """
        Detect duplicate file paths.
        """

        paths = [
            file.path
            for file in response.files
        ]

        if len(paths) != len(set(paths)):
            raise ValueError(
                "Duplicate file paths detected."
            )

    def _validate_files(
        self,
        response: CodeResponse,
    ) -> None:
        """
        Validate individual files.
        """

        for file in response.files:

            self._validate_path(
                file.path
            )

            self._validate_content(
                file.path,
                file.content,
            )

    # =========================================================
    # Helpers
    # =========================================================

    @staticmethod
    def _validate_path(
        path: str,
    ) -> None:
        """
        Validate file path safety.
        """

        file_path = Path(path)

        if file_path.is_absolute():
            raise ValueError(
                "Absolute paths are not allowed."
            )

        if ".." in file_path.parts:
            raise ValueError(
                "Path traversal detected."
            )

    @staticmethod
    def _validate_content(
        path: str,
        content: str,
    ) -> None:
        """
        Validate generated content.
        """

        if not content.strip():
            raise ValueError(
                f"Empty file content: {path}"
            )

        if path.endswith(".py"):
            GenerationValidator._validate_python(
                content
            )

    @staticmethod
    def _validate_python(
        content: str,
    ) -> None:
        """
        Validate Python syntax.
        """

        try:
            ast.parse(content)

        except SyntaxError as exc:
            raise ValueError(
                "Invalid Python syntax."
            ) from exc