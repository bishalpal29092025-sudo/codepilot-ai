"""
Provider selection strategy.

Determines which LLM provider should be used.
"""

from __future__ import annotations

from core.models.generation import ProviderType

from .base import BaseStrategy


class ProviderStrategy(BaseStrategy):
    """
    Selects generation provider.
    """

    def execute(
        self,
        provider: str | None = None,
    ) -> ProviderType:
        """
        Resolve provider.

        Defaults to MOCK for safe development.
        """

        if not provider:
            return ProviderType.MOCK

        try:
            return ProviderType(provider.lower())

        except ValueError:
            raise ValueError(
                f"Unsupported provider: {provider}"
            )