"""
Anthropic generation provider.

Provides LLM code generation through Anthropic Claude models.
"""

from __future__ import annotations

import os

from .base import BaseProvider


class AnthropicProvider(BaseProvider):
    """
    Anthropic based generation provider.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-3-5-sonnet-latest",
        temperature: float = 0.2,
    ) -> None:
        """
        Initialize Anthropic provider.

        Args:
            api_key:
                Anthropic API key.

            model:
                Claude model identifier.

            temperature:
                Generation randomness.
        """

        self.api_key = (
            api_key
            or os.getenv("ANTHROPIC_API_KEY")
        )

        self.model = model
        self.temperature = temperature

        self._client = None

    # =========================================================
    # Public API
    # =========================================================

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate code using Anthropic.

        Args:
            prompt:
                Rendered generation prompt.

        Returns:
            Generated response text.
        """

        client = self._get_client()

        response = client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=self.temperature,
            system=(
                "You are an expert "
                "software engineer."
            ),
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return self._extract_content(
            response
        )

    # =========================================================
    # Helpers
    # =========================================================

    def _get_client(self):
        """
        Lazy initialize Anthropic client.
        """

        if self._client is None:

            try:
                from anthropic import Anthropic

            except ImportError as exc:
                raise ImportError(
                    "Anthropic package is required. "
                    "Install with: pip install anthropic"
                ) from exc

            if not self.api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY is required"
                )

            self._client = Anthropic(
                api_key=self.api_key
            )

        return self._client

    @staticmethod
    def _extract_content(
        response,
    ) -> str:
        """
        Extract text content from Anthropic response.
        """

        if not response.content:
            return ""

        return "\n".join(
            block.text
            for block in response.content
            if hasattr(block, "text")
        )