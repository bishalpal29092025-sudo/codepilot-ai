"""
Repository package constants.

This module contains immutable configuration used while scanning and
analysing repositories.
"""

from __future__ import annotations

# Directories ignored during repository traversal.
IGNORE_DIRECTORIES: set[str] = {
    ".git",
    ".idea",
    ".vscode",
    ".next",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "coverage",
}

# Hidden files that should still be scanned.
ALLOWED_HIDDEN_FILES: set[str] = {
    ".env",
    ".env.example",
    ".gitignore",
}

# Files considered important regardless of extension.
IMPORTANT_FILES: set[str] = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "requirements.txt",
    "pyproject.toml",
    "poetry.lock",
    "Cargo.toml",
    "go.mod",
    "README.md",
}

# Extensions worth indexing.
SUPPORTED_EXTENSIONS: set[str] = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".json",
    ".md",
    ".java",
    ".go",
    ".rs",
    ".yaml",
    ".yml",
    ".toml",
    ".sql",
}

FRAMEWORK_MAP: dict[str, str] = {
    "next": "Next.js",
    "react": "React",
    "express": "Express.js",
    "@nestjs/core": "NestJS",
    "vue": "Vue",
    "fastify": "Fastify",
    "flask": "Flask",
    "django": "Django",
    "fastapi": "FastAPI",
}

DATABASE_MAP: dict[str, str] = {
    "mongoose": "MongoDB",
    "mongodb": "MongoDB",
    "pg": "PostgreSQL",
    "mysql2": "MySQL",
    "sqlite3": "SQLite",
    "prisma": "Prisma",
}