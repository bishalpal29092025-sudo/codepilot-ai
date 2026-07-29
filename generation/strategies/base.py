"""
Base strategy interface.

Defines contracts for generation strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """
    Abstract strategy interface.

    All generation strategies must implement
    the execute method.
    """

    @abstractmethod
    def execute(
        self,
        *args,
        **kwargs,
    ):
        """
        Execute strategy logic.
        """

        raise NotImplementedError