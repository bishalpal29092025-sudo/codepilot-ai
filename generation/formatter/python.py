"""
Python code formatter.

Formats generated Python source code before
writing it into the repository.
"""

from __future__ import annotations

from .base import BaseFormatter


class PythonFormatter(BaseFormatter):
    """
    Python source formatter.

    Responsible for basic Python formatting.
    """

    def format(
        self,
        content: str,
    ) -> str:
        """
        Format Python source code.

        Args:
            content:
                Raw generated Python code.

        Returns:
            Clean formatted Python code.
        """

        content = self._normalize_newlines(
            content
        )

        content = self._remove_trailing_spaces(
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
        Remove trailing whitespace
        from every line.
        """

        return "\n".join(
            line.rstrip()
            for line in content.splitlines()
        )