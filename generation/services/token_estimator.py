"""
Token estimation service.

Provides approximate token counting for generated
prompts and contexts.
"""

from __future__ import annotations


class TokenEstimator:
    """
    Estimates token usage.

    This implementation uses a lightweight
    approximation. Later it can be replaced
    with tokenizer-based estimation.
    """

    def __init__(
        self,
        characters_per_token: int = 4,
    ) -> None:
        """
        Initialize estimator.

        Args:
            characters_per_token:
                Approximate characters per token.
        """

        self.characters_per_token = (
            characters_per_token
        )

    # =========================================================
    # Public API
    # =========================================================

    def estimate(
        self,
        text: str,
    ) -> int:
        """
        Estimate token count.

        Args:
            text:
                Input text.

        Returns:
            Estimated token count.
        """

        if not text:
            return 0

        return max(
            1,
            len(text)
            // self.characters_per_token,
        )

    def estimate_multiple(
        self,
        texts: list[str],
    ) -> int:
        """
        Estimate tokens for multiple texts.
        """

        return sum(
            self.estimate(text)
            for text in texts
        )

    def exceeds_limit(
        self,
        text: str,
        limit: int,
    ) -> bool:
        """
        Check whether text exceeds token limit.
        """

        return (
            self.estimate(text)
            > limit
        )