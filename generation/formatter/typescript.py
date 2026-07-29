"""
TypeScript formatter.

Formats generated TypeScript and JavaScript source
code before writing files.
"""

from __future__ import annotations

from .base import BaseFormatter


class TypeScriptFormatter(BaseFormatter):
    """
    TypeScript source formatter.

    Provides basic normalization for generated
    TypeScript/JavaScript code.
    """

    def format(
        self,
        content: str,
    ) -> str:
        """
        Format TypeScript source code.

        Args:
            content:
                Raw generated TypeScript code.

        Returns:
            Clean formatted TypeScript code.
        """

        content = self._normalize_newlines(
            content
        )

        content = self._remove_trailing_spaces(
            content
        )

        content = self._normalize_empty_lines(
            content
        )

        return content.strip() + "\n"

    # =========================================================
    # Helpers
    # =========================================================

    @staticmethod
    def _normalize_newlines(
        content: str,
    ) -> str:
        """
        Normalize line endings.
        """

        return content.replace(
            "\r\n",
            "\n",
        )

    @staticmethod
    def _remove_trailing_spaces(
        content: str,
    ) -> str:
        """
        Remove trailing whitespace.
        """

        return "\n".join(
            line.rstrip()
            for line in content.splitlines()
        )

    @staticmethod
    def _normalize_empty_lines(
        content: str,
    ) -> str:
        """
        Prevent excessive empty lines.
        """

        lines = content.splitlines()

        formatted_lines = []

        previous_empty = False

        for line in lines:

            is_empty = not line.strip()

            if is_empty and previous_empty:
                continue

            formatted_lines.append(line)

            previous_empty = is_empty

        return "\n".join(formatted_lines)