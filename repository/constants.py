"""
Repository package constants.

This module contains immutable configuration used while scanning and
analysing repositories.
"""

from __future__ import annotations

# ----------------------------------------------------------------------
# Directories ignored during repository traversal.
# ----------------------------------------------------------------------

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

# ----------------------------------------------------------------------
# Hidden files that are allowed to be scanned.
#
# These files are not ignored simply because they begin with ".".
# They must still pass the IMPORTANT_FILES or extension checks.
# ----------------------------------------------------------------------

ALLOWED_HIDDEN_FILES: set[str] = {
    ".env",
    ".env.example",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
}

# ----------------------------------------------------------------------
# Files considered important regardless of extension.
# ----------------------------------------------------------------------

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
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
}

# ----------------------------------------------------------------------
# Extensions worth indexing.
# ----------------------------------------------------------------------

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

# ----------------------------------------------------------------------
# Programming language detection.
# ----------------------------------------------------------------------

LANGUAGE_EXTENSIONS: dict[str, str] = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
}

# ----------------------------------------------------------------------
# Framework detection.
# ----------------------------------------------------------------------

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

# ----------------------------------------------------------------------
# Database detection.
# ----------------------------------------------------------------------

DATABASE_MAP: dict[str, str] = {
    "mongoose": "MongoDB",
    "mongodb": "MongoDB",
    "pg": "PostgreSQL",
    "mysql2": "MySQL",
    "sqlite3": "SQLite",
    "prisma": "Prisma",
}

# ----------------------------------------------------------------------
# Package manager detection.
# ----------------------------------------------------------------------

PACKAGE_MANAGER_FILES: dict[str, str] = {
    "package-lock.json": "npm",
    "pnpm-lock.yaml": "pnpm",
    "yarn.lock": "yarn",
    "requirements.txt": "pip",
    "pyproject.toml": "poetry",
    "poetry.lock": "poetry",
    "Cargo.toml": "cargo",
    "go.mod": "go",
}