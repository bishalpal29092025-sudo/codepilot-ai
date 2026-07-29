"""
OpenAI generation provider.

Provides LLM code generation through OpenAI models.
"""

from __future__ import annotations

import os

from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    """
    OpenAI based generation provider.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4.1",
        temperature: float = 0.2,
    ) -> None:
        """
        Initialize OpenAI provider.

        Args:
            api_key:
                OpenAI API key.

            model:
                Model identifier.

            temperature:
                Generation randomness.
        """

        self.api_key = (
            api_key
            or os.getenv("OPENAI_API_KEY")
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
        Generate code using OpenAI.

        Args:
            prompt:
                Rendered generation prompt.

        Returns:
            Generated response text.
        """

        client = self._get_client()

        response = client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert "
                        "software engineer."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return (
            response
            .choices[0]
            .message
            .content
            or ""
        )

    # =========================================================
    # Helpers
    # =========================================================

    def _get_client(self):
        """
        Lazy initialize OpenAI client.

        This avoids importing OpenAI SDK
        when the provider is not used.
        """

        if self._client is None:

            try:
                from openai import OpenAI

            except ImportError as exc:
                raise ImportError(
                    "OpenAI package is required. "
                    "Install with: pip install openai"
                ) from exc

            if not self.api_key:
                raise ValueError(
                    "OPENAI_API_KEY is required"
                )

            self._client = OpenAI(
                api_key=self.api_key
            )

        return self._client