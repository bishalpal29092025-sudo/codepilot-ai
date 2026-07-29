"""
Base provider interface.

Defines the contract for all LLM providers
used by CodePilot AI generation engine.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    Abstract interface for generation providers.

    Every provider implementation must provide
    a generate method.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from an LLM.

        Args:
            prompt:
                Rendered generation prompt.

        Returns:
            Raw provider response.
        """

        raise NotImplementedError