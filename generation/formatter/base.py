"""
Base formatter interface.

Defines the contract for all language-specific
code formatters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseFormatter(ABC):
    """
    Abstract formatter interface.

    Every formatter implementation must provide
    a format method.
    """

    @abstractmethod
    def format(
        self,
        content: str,
    ) -> str:
        """
        Format source code content.

        Args:
            content:
                Raw generated source code.

        Returns:
            Formatted source code.
        """

        raise NotImplementedError