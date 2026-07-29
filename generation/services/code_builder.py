"""
Code generation service.

Coordinates prompt creation, provider execution,
and response parsing.
"""

from __future__ import annotations

from core.models.generation import (
    CodeResponse,
    GenerationContext,
)

from generation.parser.response import ResponseParser
from generation.prompt.builder import PromptBuilder
from generation.providers.base import BaseProvider


class CodeBuilder:
    """
    Builds generated code from a GenerationContext.

    Flow:

    GenerationContext
            |
            ▼
    PromptBuilder
            |
            ▼
    Provider
            |
            ▼
    ResponseParser
            |
            ▼
    CodeResponse
    """

    def __init__(
        self,
        prompt_builder: PromptBuilder | None = None,
        response_parser: ResponseParser | None = None,
    ) -> None:
        """
        Initialize code builder.
        """

        self.prompt_builder = (
            prompt_builder
            or PromptBuilder()
        )

        self.response_parser = (
            response_parser
            or ResponseParser()
        )

    # =========================================================
    # Public API
    # =========================================================

    def build(
        self,
        context: GenerationContext,
        provider: BaseProvider,
    ) -> CodeResponse:
        """
        Generate code for a task.

        Args:
            context:
                Complete generation context.

            provider:
                Selected LLM provider.

        Returns:
            Parsed generated code response.
        """

        prompt = self.prompt_builder.build(
            context
        )

        response = provider.generate(
            prompt
        )

        return self.response_parser.parse(
            response
        )