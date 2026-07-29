"""
Formatter selection strategy.

Determines the formatter based on file language.
"""

from __future__ import annotations

from generation.formatter.markdown import MarkdownFormatter
from generation.formatter.python import PythonFormatter
from generation.formatter.typescript import TypeScriptFormatter

from generation.formatter.base import BaseFormatter

from .base import BaseStrategy


class FormatterStrategy(BaseStrategy):
    """
    Selects formatter implementation.
    """

    def execute(
        self,
        language: str,
    ) -> BaseFormatter:
        """
        Return formatter for language.
        """

        language = language.lower()

        match language:

            case "python":
                return PythonFormatter()

            case "typescript" | "javascript":
                return TypeScriptFormatter()

            case "markdown" | "md":
                return MarkdownFormatter()

            case _:
                return MarkdownFormatter()