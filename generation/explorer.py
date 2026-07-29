"""
Generation repository explorer.

Discovers repository information required
for code generation.
"""

from __future__ import annotations

from pathlib import Path

from core.models.generation import RepositoryContext


class GenerationExplorer:
    """
    Explores repositories and builds
    RepositoryContext.
    """

    IGNORE_DIRECTORIES = {
        ".git",
        "node_modules",
        "__pycache__",
        ".next",
        "dist",
        "build",
    }

    # =========================================================
    # Public API
    # =========================================================

    def explore(
        self,
        root_path: str,
    ) -> RepositoryContext:
        """
        Analyze repository.

        Args:
            root_path:
                Repository location.

        Returns:
            RepositoryContext.
        """

        root = Path(root_path)

        files = self._collect_files(
            root
        )

        language = self._detect_language(
            files
        )

        framework = self._detect_framework(
            root,
            files,
        )

        return RepositoryContext(
            name=root.name,
            root_path=str(root),
            project_type=self._detect_project_type(
                files
            ),
            primary_language=language,
            frameworks=(
                [framework]
                if framework
                else []
            ),
            entry_points=self._find_entry_points(
                files
            ),
            source_directories=self._find_source_directories(
                files
            ),
            ignored_directories=list(
                self.IGNORE_DIRECTORIES
            ),
            repository_tree="\n".join(
                str(file)
                for file in files
            ),
            metadata={
                "total_files": len(files),
            },
        )

    # =========================================================
    # File Discovery
    # =========================================================

    def _collect_files(
        self,
        root: Path,
    ) -> list[Path]:
        """
        Collect repository files.
        """

        files = []

        for path in root.rglob("*"):

            if not path.is_file():
                continue

            if any(
                directory in path.parts
                for directory in self.IGNORE_DIRECTORIES
            ):
                continue

            files.append(
                path.relative_to(root)
            )

        return sorted(files)

    # =========================================================
    # Detection
    # =========================================================

    @staticmethod
    def _detect_language(
        files: list[Path],
    ) -> str:
        """
        Detect primary language.
        """

        extensions = {
            ".py": "Python",
            ".ts": "TypeScript",
            ".tsx": "TypeScript",
            ".js": "JavaScript",
            ".java": "Java",
            ".rs": "Rust",
        }

        count = {}

        for file in files:

            language = extensions.get(
                file.suffix
            )

            if language:
                count[language] = (
                    count.get(language, 0)
                    + 1
                )

        if not count:
            return "Unknown"

        return max(
            count,
            key=count.get,
        )

    @staticmethod
    def _detect_framework(
        root: Path,
        files: list[Path],
    ) -> str | None:
        """
        Detect common frameworks.
        """

        names = {
            "package.json": "JavaScript",
            "next.config.js": "Next.js",
            "next.config.mjs": "Next.js",
            "requirements.txt": "Python",
            "manage.py": "Django",
        }

        for file in files:

            if file.name in names:
                return names[file.name]

        return None

    @staticmethod
    def _detect_project_type(
        files: list[Path],
    ) -> str:
        """
        Detect project category.
        """

        paths = {
            file.name
            for file in files
        }

        if "package.json" in paths:
            return "web"

        if "main.py" in paths:
            return "backend"

        return "unknown"

    # =========================================================
    # Helpers
    # =========================================================

    @staticmethod
    def _find_entry_points(
        files: list[Path],
    ) -> list[str]:
        """
        Find common application entry points.
        """

        entry_names = {
            "main.py",
            "index.ts",
            "index.js",
            "app.ts",
            "app.py",
        }

        return [
            str(file)
            for file in files
            if file.name in entry_names
        ]

    @staticmethod
    def _find_source_directories(
        files: list[Path],
    ) -> list[str]:
        """
        Detect source directories.
        """

        directories = {
            file.parts[0]
            for file in files
            if len(file.parts) > 1
        }

        return sorted(directories)