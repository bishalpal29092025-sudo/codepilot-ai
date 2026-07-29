"""
Markdown parser.

Extracts generated file information from LLM markdown responses.
"""

from __future__ import annotations

import re

from .code_block import CodeBlockParser


class MarkdownParser:
    """
    Parses markdown formatted generation responses.
    """

    FILE_PATTERN = re.compile(
        r"FILE:\s*(?P<path>[^\n]+)",
        re.IGNORECASE,
    )

    def __init__(
        self,
        code_block_parser: CodeBlockParser | None = None,
    ) -> None:
        """
        Initialize markdown parser.
        """

        self.code_block_parser = (
            code_block_parser
            or CodeBlockParser()
        )

    # =========================================================
    # Public API
    # =========================================================

    def parse(
        self,
        markdown: str,
    ) -> list[dict[str, str]]:
        """
        Parse markdown response.

        Args:
            markdown:
                Raw LLM response.

        Returns:
            Extracted generated files.
        """

        paths = self._extract_paths(
            markdown
        )

        blocks = self.code_block_parser.parse(
            markdown
        )

        results = []

        for index, block in enumerate(blocks):

            path = (
                paths[index]
                if index < len(paths)
                else f"generated_file_{index}.txt"
            )

            results.append(
                {
                    "path": path,
                    "language": block["language"],
                    "content": block["content"],
                }
            )

        return results

    # =========================================================
    # Helpers
    # =========================================================

    @classmethod
    def _extract_paths(
        cls,
        markdown: str,
    ) -> list[str]:
        """
        Extract FILE paths from response.
        """

        matches = cls.FILE_PATTERN.findall(
            markdown
        )

        return [
            path.strip()
            for path in matches
        ]