"""
Base classes for planning strategies.

Planning strategies encapsulate small, focused pieces of planning logic.
Each strategy has a single responsibility and can be composed by the
ProjectPlanner to build a complete ProjectPlan.
"""

from __future__ import annotations

from abc import ABC


class Strategy(ABC):
    """
    Base class for all planning strategies.

    The base strategy intentionally contains no behaviour.
    It exists to provide a common type for all planning strategies and
    allows future shared functionality (logging, metrics, caching,
    configuration, AI inference, etc.) to be added without changing
    individual strategy implementations.
    """

    __slots__ = ()