"""
Keyword matching service.

Provides reusable keyword matching utilities for planning strategies.

The matcher performs simple, case-insensitive keyword matching and is designed
to be easily replaced by more advanced implementations (semantic search,
embeddings, LLM classification, etc.) without changing the strategies that
depend on it.
"""

from __future__ import annotations

from collections.abc import Iterable


class KeywordMatcher:
    """
    Service responsible for keyword matching.

    The implementation is intentionally lightweight and deterministic.
    """

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalize text for comparison.

        Parameters
        ----------
        text:
            Input text.

        Returns
        -------
        str
            Lowercase text with leading/trailing whitespace removed.
        """

        return text.strip().lower()

    def contains(
        self,
        text: str,
        keyword: str,
    ) -> bool:
        """
        Determine whether the text contains the keyword.

        Parameters
        ----------
        text:
            Source text.

        keyword:
            Keyword to search for.

        Returns
        -------
        bool
        """

        return self.normalize(keyword) in self.normalize(text)

    def contains_any(
        self,
        text: str,
        keywords: Iterable[str],
    ) -> bool:
        """
        Determine whether the text contains any keyword.

        Parameters
        ----------
        text:
            Source text.

        keywords:
            Keywords to search for.

        Returns
        -------
        bool
        """

        normalized = self.normalize(text)

        return any(
            self.normalize(keyword) in normalized
            for keyword in keywords
        )

    def contains_all(
        self,
        text: str,
        keywords: Iterable[str],
    ) -> bool:
        """
        Determine whether the text contains every keyword.

        Parameters
        ----------
        text:
            Source text.

        keywords:
            Keywords to search for.

        Returns
        -------
        bool
        """

        normalized = self.normalize(text)

        return all(
            self.normalize(keyword) in normalized
            for keyword in keywords
        )

    def first_match(
        self,
        text: str,
        keywords: Iterable[str],
    ) -> str | None:
        """
        Return the first matching keyword.

        Parameters
        ----------
        text:
            Source text.

        keywords:
            Keywords to search.

        Returns
        -------
        str | None
            First matching keyword or None.
        """

        normalized = self.normalize(text)

        for keyword in keywords:
            if self.normalize(keyword) in normalized:
                return keyword

        return None

    def matching_keywords(
        self,
        text: str,
        keywords: Iterable[str],
    ) -> list[str]:
        """
        Return every matching keyword.

        Parameters
        ----------
        text:
            Source text.

        keywords:
            Keywords to search.

        Returns
        -------
        list[str]
        """

        normalized = self.normalize(text)

        return [
            keyword
            for keyword in keywords
            if self.normalize(keyword) in normalized
        ]