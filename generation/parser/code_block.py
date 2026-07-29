"""
Code block parser.

Extracts fenced code blocks from markdown
LLM responses.
"""

from __future__ import annotations

import re


class CodeBlockParser:
    """
    Parses markdown fenced code blocks.
    """

    CODE_BLOCK_PATTERN = re.compile(
        r"```(?P<language>\w*)\n"
        r"(?P<content>.*?)"
        r"```",
        re.DOTALL,
    )

    def parse(
        self,
        markdown: str,
    ) -> list[dict[str, str]]:
        """
        Extract code blocks.

        Args:
            markdown:
                Markdown response from LLM.

        Returns:
            List of extracted code blocks.

        Example result:

        [
            {
                "language": "python",
                "content": "print('hello')"
            }
        ]
        """

        blocks = []

        matches = self.CODE_BLOCK_PATTERN.findall(
            markdown
        )

        for language, content in matches:
            blocks.append(
                {
                    "language": (
                        language.strip()
                        or "text"
                    ),
                    "content": (
                        content.strip()
                    ),
                }
            )

        return blocks