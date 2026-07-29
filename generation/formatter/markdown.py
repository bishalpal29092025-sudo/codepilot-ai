"""
Markdown formatter.

Formats generated markdown documents before
writing them into the repository.
"""

from __future__ import annotations

from .base import BaseFormatter


class MarkdownFormatter(BaseFormatter):
    """
    Markdown document formatter.

    Performs basic markdown cleanup.
    """

    def format(
        self,
        content: str,
    ) -> str:
        """
        Format markdown content.

        Args:
            content:
                Raw generated markdown.

        Returns:
            Clean markdown document.
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
        Prevent unnecessary consecutive
        empty lines.
        """

        lines = content.splitlines()

        result = []

        previous_empty = False

        for line in lines:

            empty = not line.strip()

            if empty and previous_empty:
                continue

            result.append(line)

            previous_empty = empty

        return "\n".join(result)