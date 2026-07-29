"""
Generation response parser.

Converts raw LLM provider responses into
Generation domain models.
"""

from __future__ import annotations

from core.models.generation import (
    CodeResponse,
    GeneratedFile,
)

from .markdown import MarkdownParser


class ResponseParser:
    """
    Parses provider responses into CodeResponse models.
    """

    def __init__(
        self,
        markdown_parser: MarkdownParser | None = None,
    ) -> None:
        """
        Initialize response parser.
        """

        self.markdown_parser = (
            markdown_parser
            or MarkdownParser()
        )

    # =========================================================
    # Public API
    # =========================================================

    def parse(
        self,
        response: str,
    ) -> CodeResponse:
        """
        Parse raw provider response.

        Args:
            response:
                Raw text returned by LLM provider.

        Returns:
            Structured CodeResponse.
        """

        files_data = self.markdown_parser.parse(
            response
        )

        files = [
            GeneratedFile(
                path=file["path"],
                content=file["content"],
            )
            for file in files_data
        ]

        return CodeResponse(
            files=files
        )