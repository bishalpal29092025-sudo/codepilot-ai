"""
Provider factory.

Creates LLM provider instances based on
configured ProviderType.
"""

from __future__ import annotations

from core.models.generation import ProviderType

from .base import BaseProvider
from .mock import MockProvider


class ProviderFactory:
    """
    Factory responsible for provider creation.

    Keeps provider selection logic isolated from
    the generation engine.
    """

    @staticmethod
    def create(
        provider_type: ProviderType,
        **kwargs,
    ) -> BaseProvider:
        """
        Create provider instance.

        Args:
            provider_type:
                Requested provider.

            kwargs:
                Provider-specific configuration.

        Returns:
            BaseProvider implementation.

        Raises:
            ValueError:
                If provider is unsupported.
        """

        match provider_type:

            case ProviderType.MOCK:
                return MockProvider(
                    **kwargs
                )

            case ProviderType.OPENAI:
                from .openai import OpenAIProvider

                return OpenAIProvider(
                    **kwargs
                )

            case ProviderType.ANTHROPIC:
                from .anthropic import AnthropicProvider

                return AnthropicProvider(
                    **kwargs
                )

            case ProviderType.OLLAMA:
                from .ollama import OllamaProvider

                return OllamaProvider(
                    **kwargs
                )

            case _:
                raise ValueError(
                    f"Unsupported provider: {provider_type}"
                )