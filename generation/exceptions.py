"""
Generation engine exceptions.

Defines all custom exceptions raised by the
CodePilot AI generation pipeline.

Exception hierarchy:

GenerationError
│
├── ConfigurationError
├── ContextError
├── PromptError
├── ProviderError
├── ParsingError
├── FormattingError
├── ValidationError
└── WriterError
"""

from __future__ import annotations


# ============================================================================
# Base Exception
# ============================================================================


class GenerationError(Exception):
    """
    Base exception for all generation engine errors.
    """

    def __init__(
        self,
        message: str,
        details: dict | None = None,
    ) -> None:
        super().__init__(message)

        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        return self.message


# ============================================================================
# Configuration Errors
# ============================================================================


class ConfigurationError(GenerationError):
    """
    Raised when generation configuration is invalid.
    """

    pass


class UnsupportedProviderError(ConfigurationError):
    """
    Raised when an unsupported provider is requested.
    """

    pass


class UnsupportedLanguageError(ConfigurationError):
    """
    Raised when an unsupported language is detected.
    """

    pass


# ============================================================================
# Context Errors
# ============================================================================


class ContextError(GenerationError):
    """
    Raised when generation context creation fails.
    """

    pass


class RepositoryContextError(ContextError):
    """
    Raised when repository context is invalid.
    """

    pass


class DependencyContextError(ContextError):
    """
    Raised when dependency context creation fails.
    """

    pass


# ============================================================================
# Prompt Errors
# ============================================================================


class PromptError(GenerationError):
    """
    Raised during prompt construction.
    """

    pass


class TemplateRenderError(PromptError):
    """
    Raised when prompt template rendering fails.
    """

    pass


# ============================================================================
# Provider Errors
# ============================================================================


class ProviderError(GenerationError):
    """
    Raised when an LLM provider fails.
    """

    pass


class ProviderConnectionError(ProviderError):
    """
    Raised when provider connection fails.
    """

    pass


class ProviderResponseError(ProviderError):
    """
    Raised when provider response is invalid.
    """

    pass


# ============================================================================
# Parser Errors
# ============================================================================


class ParsingError(GenerationError):
    """
    Raised when generated response parsing fails.
    """

    pass


class InvalidCodeBlockError(ParsingError):
    """
    Raised when code blocks cannot be parsed.
    """

    pass


class InvalidResponseFormatError(ParsingError):
    """
    Raised when LLM output format is invalid.
    """

    pass


# ============================================================================
# Formatter Errors
# ============================================================================


class FormattingError(GenerationError):
    """
    Raised when code formatting fails.
    """

    pass


class UnsupportedFormatterError(FormattingError):
    """
    Raised when formatter is unavailable.
    """

    pass


# ============================================================================
# Validation Errors
# ============================================================================


class ValidationError(GenerationError):
    """
    Raised when generated code validation fails.
    """

    pass


class UnsafeFilePathError(ValidationError):
    """
    Raised when generated file path is unsafe.
    """

    pass


class SyntaxValidationError(ValidationError):
    """
    Raised when generated code contains syntax errors.
    """

    pass


# ============================================================================
# Writer Errors
# ============================================================================


class WriterError(GenerationError):
    """
    Raised during filesystem operations.
    """

    pass


class BackupError(WriterError):
    """
    Raised when backup creation fails.
    """

    pass


class TransactionError(WriterError):
    """
    Raised when file transaction fails.
    """

    pass