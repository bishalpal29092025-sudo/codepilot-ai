"""
Generation package constants.

This module centralizes all immutable configuration values used by the
CodePilot AI generation engine.

Responsibilities:
- Provider configuration
- Prompt configuration
- Context limits
- Token budgets
- File generation rules
- Supported languages
- Parser configuration
- Validation rules
- Formatter configuration
- Writer configuration
- Retry policies
"""

from __future__ import annotations

from typing import Final


# ============================================================================
# Provider Names
# ============================================================================

OPENAI_PROVIDER: Final[str] = "openai"

ANTHROPIC_PROVIDER: Final[str] = "anthropic"

OLLAMA_PROVIDER: Final[str] = "ollama"

MOCK_PROVIDER: Final[str] = "mock"


SUPPORTED_PROVIDERS: Final[tuple[str, ...]] = (
    OPENAI_PROVIDER,
    ANTHROPIC_PROVIDER,
    OLLAMA_PROVIDER,
    MOCK_PROVIDER,
)


DEFAULT_PROVIDER: Final[str] = MOCK_PROVIDER


# ============================================================================
# Provider Models
# ============================================================================

DEFAULT_OPENAI_MODEL: Final[str] = "gpt-4.1"

DEFAULT_ANTHROPIC_MODEL: Final[str] = (
    "claude-3-5-sonnet-latest"
)

DEFAULT_OLLAMA_MODEL: Final[str] = (
    "llama3.1"
)


# ============================================================================
# Prompt Configuration
# ============================================================================

SYSTEM_PROMPT_NAME: Final[str] = "system"

USER_PROMPT_NAME: Final[str] = "user"


DEFAULT_TEMPERATURE: Final[float] = 0.2

DEFAULT_TOP_P: Final[float] = 1.0

DEFAULT_MAX_TOKENS: Final[int] = 4096


MAX_PROMPT_LENGTH: Final[int] = 120_000


# ============================================================================
# Context Configuration
# ============================================================================

MAX_CONTEXT_FILES: Final[int] = 25

MAX_FILE_SIZE_BYTES: Final[int] = 250_000

MAX_DEPENDENCY_DEPTH: Final[int] = 3


DEFAULT_CONTEXT_WINDOW: Final[int] = 128_000

TOKEN_SAFETY_MARGIN: Final[int] = 2_000


MAX_CONTEXT_TOKENS: Final[int] = (
    DEFAULT_CONTEXT_WINDOW
    - TOKEN_SAFETY_MARGIN
)


# ============================================================================
# Generation Limits
# ============================================================================

MAX_GENERATION_ATTEMPTS: Final[int] = 3

MAX_FILES_PER_GENERATION: Final[int] = 25

MAX_FILE_CONTENT_LENGTH: Final[int] = 250_000


# ============================================================================
# File Generation
# ============================================================================

DEFAULT_ENCODING: Final[str] = "utf-8"

DEFAULT_ENCODING_ERRORS: Final[str] = "strict"

DEFAULT_LINE_ENDING: Final[str] = "\n"


BACKUP_EXTENSION: Final[str] = ".bak"

TEMP_FILE_EXTENSION: Final[str] = ".tmp"


DEFAULT_INDENT: Final[str] = "    "


# ============================================================================
# Supported Languages
# ============================================================================

PYTHON_LANGUAGE: Final[str] = "python"

TYPESCRIPT_LANGUAGE: Final[str] = "typescript"

JAVASCRIPT_LANGUAGE: Final[str] = "javascript"

RUST_LANGUAGE: Final[str] = "rust"

JAVA_LANGUAGE: Final[str] = "java"

MARKDOWN_LANGUAGE: Final[str] = "markdown"


SUPPORTED_LANGUAGES: Final[tuple[str, ...]] = (
    PYTHON_LANGUAGE,
    TYPESCRIPT_LANGUAGE,
    JAVASCRIPT_LANGUAGE,
    RUST_LANGUAGE,
    JAVA_LANGUAGE,
    MARKDOWN_LANGUAGE,
)


# ============================================================================
# Supported File Extensions
# ============================================================================

PYTHON_EXTENSION: Final[str] = ".py"

TYPESCRIPT_EXTENSION: Final[str] = ".ts"

TSX_EXTENSION: Final[str] = ".tsx"

JAVASCRIPT_EXTENSION: Final[str] = ".js"

JSX_EXTENSION: Final[str] = ".jsx"

RUST_EXTENSION: Final[str] = ".rs"

JAVA_EXTENSION: Final[str] = ".java"

MARKDOWN_EXTENSION: Final[str] = ".md"


SUPPORTED_FILE_EXTENSIONS: Final[tuple[str, ...]] = (
    PYTHON_EXTENSION,
    TYPESCRIPT_EXTENSION,
    TSX_EXTENSION,
    JAVASCRIPT_EXTENSION,
    JSX_EXTENSION,
    RUST_EXTENSION,
    JAVA_EXTENSION,
    MARKDOWN_EXTENSION,
)


# ============================================================================
# Repository Exploration
# ============================================================================

IGNORED_DIRECTORIES: Final[tuple[str, ...]] = (
    ".git",
    "node_modules",
    "__pycache__",
    ".next",
    "dist",
    "build",
    ".venv",
    "venv",
)


# ============================================================================
# Markdown Parsing
# ============================================================================

CODE_BLOCK_DELIMITER: Final[str] = "```"

DEFAULT_CODE_BLOCK_LANGUAGE: Final[str] = "text"


FILE_MARKER: Final[str] = "FILE:"

CODE_MARKER: Final[str] = "CODE:"


# ============================================================================
# Generation Status
# ============================================================================

STATUS_PENDING: Final[str] = "pending"

STATUS_RUNNING: Final[str] = "running"

STATUS_COMPLETED: Final[str] = "completed"

STATUS_FAILED: Final[str] = "failed"


GENERATION_STATUSES: Final[tuple[str, ...]] = (
    STATUS_PENDING,
    STATUS_RUNNING,
    STATUS_COMPLETED,
    STATUS_FAILED,
)


# ============================================================================
# Validation
# ============================================================================

MIN_GENERATED_FILES: Final[int] = 1

MAX_GENERATED_FILES: Final[int] = 100


# ============================================================================
# Formatter
# ============================================================================

FORMATTER_TIMEOUT_SECONDS: Final[int] = 30


SUPPORTED_FORMATTERS: Final[tuple[str, ...]] = (
    PYTHON_LANGUAGE,
    TYPESCRIPT_LANGUAGE,
    JAVASCRIPT_LANGUAGE,
    MARKDOWN_LANGUAGE,
)


# ============================================================================
# Writer
# ============================================================================

ENABLE_BACKUP_BY_DEFAULT: Final[bool] = True

ENABLE_TRANSACTION_BY_DEFAULT: Final[bool] = True


DEFAULT_BACKUP_DIRECTORY: Final[str] = (
    ".codepilot/backups"
)


# ============================================================================
# Retry Policy
# ============================================================================

DEFAULT_MAX_RETRIES: Final[int] = 3

RETRY_BACKOFF_SECONDS: Final[float] = 2.0


# ============================================================================
# Miscellaneous
# ============================================================================

GENERATION_VERSION: Final[str] = "1.0"

DEFAULT_TIMEOUT_SECONDS: Final[int] = 60