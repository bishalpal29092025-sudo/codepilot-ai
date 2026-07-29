"""
Generation engine.

Orchestrates the complete code generation pipeline.
"""

from __future__ import annotations

from core.models.generation import (
    CodeResponse,
    GenerationContext,
)

from generation.services.code_builder import CodeBuilder
from generation.services.context_optimizer import (
    ContextOptimizer,
)
from generation.strategies.formatter import (
    FormatterStrategy,
)
from generation.strategies.provider import (
    ProviderStrategy,
)
from generation.providers.factory import (
    ProviderFactory,
)
from generation.writer.transaction import (
    TransactionWriter,
)


class Generator:
    """
    Main CodePilot generation engine.

    Coordinates:

    Context
        ↓
    Prompt
        ↓
    Provider
        ↓
    Parser
        ↓
    Formatter
        ↓
    Writer
    """

    def __init__(
        self,
        code_builder: CodeBuilder | None = None,
        context_optimizer: ContextOptimizer | None = None,
        writer: TransactionWriter | None = None,
    ) -> None:
        """
        Initialize generator.
        """

        self.code_builder = (
            code_builder
            or CodeBuilder()
        )

        self.context_optimizer = (
            context_optimizer
            or ContextOptimizer()
        )

        self.writer = (
            writer
            or TransactionWriter()
        )

        self.provider_strategy = (
            ProviderStrategy()
        )

        self.formatter_strategy = (
            FormatterStrategy()
        )

    # =========================================================
    # Public API
    # =========================================================

    def generate(
        self,
        context: GenerationContext,
        provider: str | None = None,
        write: bool = False,
    ) -> CodeResponse:
        """
        Execute generation pipeline.

        Args:

            context:
                Generation context.

            provider:
                Provider name.

            write:
                Whether to write generated files.

        Returns:

            Generated code response.
        """

        optimized_context = (
            self.context_optimizer.optimize(
                context
            )
        )

        provider_type = (
            self.provider_strategy.execute(
                provider
            )
        )

        llm_provider = (
            ProviderFactory.create(
                provider_type
            )
        )

        response = (
            self.code_builder.build(
                optimized_context,
                llm_provider,
            )
        )

        if write:
            self._write_files(
                optimized_context,
                response,
            )

        return response

    # =========================================================
    # Helpers
    # =========================================================

    def _write_files(
        self,
        context: GenerationContext,
        response: CodeResponse,
    ) -> None:
        """
        Format and write generated files.
        """

        formatted_files = []

        for file in response.files:

            formatter = (
                self.formatter_strategy.execute(
                    context.language
                )
            )

            formatted_files.append(
                file.model_copy(
                    update={
                        "content": formatter.format(
                            file.content
                        )
                    }
                )
            )

        self.writer.execute(
            context.repository.root_path,
            formatted_files,
        )