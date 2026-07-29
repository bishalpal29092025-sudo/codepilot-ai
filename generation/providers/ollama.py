"""
Ollama generation provider.

Provides local LLM generation through Ollama.
"""

from __future__ import annotations

import os

from .base import BaseProvider


class OllamaProvider(BaseProvider):
    """
    Local Ollama based generation provider.
    """

    def __init__(
        self,
        model: str = "llama3.1",
        base_url: str | None = None,
        temperature: float = 0.2,
    ) -> None:
        """
        Initialize Ollama provider.

        Args:
            model:
                Local Ollama model name.

            base_url:
                Ollama server URL.

            temperature:
                Generation randomness.
        """

        self.model = model

        self.base_url = (
            base_url
            or os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434",
            )
        )

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
        Generate code using Ollama.

        Args:
            prompt:
                Rendered generation prompt.

        Returns:
            Generated response text.
        """

        client = self._get_client()

        response = client.chat(
            model=self.model,
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
            options={
                "temperature": self.temperature,
            },
        )

        return (
            response
            .get("message", {})
            .get("content", "")
        )

    # =========================================================
    # Helpers
    # =========================================================

    def _get_client(self):
        """
        Lazy initialize Ollama client.
        """

        if self._client is None:

            try:
                import ollama

            except ImportError as exc:
                raise ImportError(
                    "Ollama package is required. "
                    "Install with: pip install ollama"
                ) from exc

            self._client = ollama

        return self._client