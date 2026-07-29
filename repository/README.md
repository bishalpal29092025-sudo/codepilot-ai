# Repository Package

> Repository discovery, metadata loading, and project analysis for CodePilot AI.

The **Repository** package is the first stage of the CodePilot AI pipeline. It is responsible for scanning a software repository, safely loading project metadata, detecting technologies, and producing a structured `RepositoryInfo` object used by downstream planning and generation components.

---

# Features

- Repository scanning
- Safe file reading
- Metadata loading and caching
- Programming language detection
- Framework detection
- Database detection
- Package manager detection
- Production-ready architecture
- Comprehensive automated testing

---

# Architecture

```
                Repository Path
                        │
                        ▼
              RepositoryScanner
                        │
                Repository Files
                        │
                        ▼
           RepositoryFileReader
                        │
                        ▼
             RepositoryLoader
                        │
             Repository Metadata
                        │
                        ▼
            RepositoryDetector
                        │
                        ▼
             RepositoryInfo
                        │
                        ▼
            RepositoryExplorer
```

---

# Responsibilities

## RepositoryScanner

Responsible for traversing the repository filesystem.

### Input

- Repository path

### Output

- List of repository-relative files

Responsibilities:

- Traverse directories
- Ignore unsupported folders
- Filter hidden files
- Collect relevant source files

---

## RepositoryFileReader

Safely reads repository files.

Responsibilities:

- Validate file paths
- Prevent path traversal
- Detect binary files
- Enforce maximum file size
- Read UTF-8 text files

---

## RepositoryLoader

Loads and caches repository metadata.

Supported files include:

- package.json
- requirements.txt
- pyproject.toml
- Cargo.toml
- go.mod

Responsibilities:

- Read metadata once
- Cache parsed content
- Provide read-only access

---

## RepositoryDetector

Analyses repository metadata.

Detects:

- Primary programming language
- Framework
- Database
- Package manager

The detector contains only business logic and performs no filesystem operations.

---

## RepositoryExplorer

Coordinates the complete repository analysis pipeline.

Responsibilities:

1. Scan repository
2. Load metadata
3. Detect technologies
4. Return RepositoryInfo

---

# Package Structure

```
repository/
│
├── __init__.py
├── constants.py
├── exceptions.py
├── scanner.py
├── file_reader.py
├── loader.py
├── detector.py
├── explorer.py
│
├── tests/
│   ├── test_scanner.py
│   ├── test_file_reader.py
│   ├── test_loader.py
│   ├── test_detector.py
│   ├── test_explorer.py
│   └── test_integration.py
│
└── README.md
```

---

# Usage

```python
from repository.explorer import RepositoryExplorer

explorer = RepositoryExplorer("/path/to/repository")

info = explorer.explore()

print(info.language)
print(info.framework)
print(info.database)
print(info.package_manager)
```

---

# Example

Repository

```
my-app/
│
├── package.json
├── package-lock.json
├── README.md
└── src/
    └── index.ts
```

Detected information

```
Language         : TypeScript
Framework        : Next.js
Database         : MongoDB
Package Manager  : npm
```

---

# Data Flow

```
Repository Path
        │
        ▼
RepositoryScanner
        │
        ▼
RepositoryFileReader
        │
        ▼
RepositoryLoader
        │
        ▼
RepositoryDetector
        │
        ▼
RepositoryInfo
        │
        ▼
RepositoryExplorer
```

---

# Public API

Primary entry point:

```python
RepositoryExplorer.explore() -> RepositoryInfo
```

The returned `RepositoryInfo` contains:

- language
- framework
- database
- package_manager
- files
- total_files

---

# Testing

Run the complete test suite:

```bash
python -m pytest repository/tests
```

Current status:

```
24 Passing Tests
```

Coverage includes:

- Scanner
- File Reader
- Loader
- Detector
- Explorer
- End-to-end integration

---

# Design Principles

The Repository package follows several software engineering principles.

## Single Responsibility Principle

Each class has exactly one responsibility.

## Layered Architecture

The package is divided into distinct layers:

- Infrastructure
- Loading
- Business Logic
- Application

## Separation of Concerns

Filesystem access, metadata loading, analysis, and orchestration are isolated into independent components.

## Testability

Every component can be tested independently.

## Extensibility

Additional metadata loaders, detectors, and repository types can be added with minimal changes to existing code.

---

# Future Improvements

Potential future enhancements include:

- Git repository analysis
- Monorepo support
- Dependency graph generation
- Repository health metrics
- License detection
- CI/CD configuration detection
- Container and Docker analysis
- Build system detection
- Repository complexity metrics
- Plugin-based technology detectors

---

# Status

**Version:** 1.0

**Status:** Stable

The Repository package serves as the foundation of the CodePilot AI pipeline and is considered complete. Future changes should focus on bug fixes and incremental enhancements rather than architectural redesign.