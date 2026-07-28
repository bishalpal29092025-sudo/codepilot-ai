import json
import os


class RepositoryExplorer:
    """
    Explores a repository and extracts metadata required
    by the AI Coding Agent.
    """

    IGNORE_DIRS = {
        ".git",
        "node_modules",
        "__pycache__",
        ".next",
        ".venv",
        "venv",
        "dist",
        "build",
        ".idea",
        ".vscode",
    }

    IMPORTANT_FILES = {
        "package.json",
        "package-lock.json",
        "README.md",
        ".env",
        ".gitignore",
    }

    IMPORTANT_EXTENSIONS = {
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".py",
        ".java",
        ".go",
        ".rs",
        ".json",
        ".md",
    }

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

        self.language = "Unknown"
        self.framework = "Unknown"
        self.database = "Unknown"
        self.package_manager = "Unknown"

        self.files = []

        self.scan()
        self.detect_project()

    # ----------------------------------------
    # Repository Scan
    # ----------------------------------------

    def scan(self):
        """
        Scan the repository recursively.
        """

        self.files.clear()

        for root, dirs, files in os.walk(self.repo_path):

            dirs[:] = [
                d
                for d in dirs
                if d not in self.IGNORE_DIRS
            ]

            for file in files:

                if (
                    file.startswith(".")
                    and file not in {".env", ".gitignore"}
                ):
                    continue

                relative_path = os.path.relpath(
                    os.path.join(root, file),
                    self.repo_path,
                )

                extension = os.path.splitext(file)[1]

                if (
                    extension in self.IMPORTANT_EXTENSIONS
                    or file in self.IMPORTANT_FILES
                ):
                    self.files.append(relative_path)

        self.files.sort()

    # ----------------------------------------
    # Project Detection
    # ----------------------------------------

    def detect_project(self):
        """
        Detect language, framework and database.
        """

        package_json = os.path.join(
            self.repo_path,
            "package.json",
        )

        if os.path.exists(package_json):

            self.language = "JavaScript"
            self.package_manager = "npm"

            try:
                with open(
                    package_json,
                    "r",
                    encoding="utf-8",
                ) as f:
                    package = json.load(f)

                dependencies = {}

                dependencies.update(
                    package.get("dependencies", {})
                )

                dependencies.update(
                    package.get("devDependencies", {})
                )

                self.detect_framework(dependencies)
                self.detect_database(dependencies)

            except Exception:
                pass

            return

        python_files = [
            file
            for file in self.files
            if file.endswith(".py")
        ]

        if python_files:
            self.language = "Python"
            self.package_manager = "pip"

    # ----------------------------------------
    # Framework Detection
    # ----------------------------------------

    def detect_framework(self, dependencies):

        frameworks = {
            "express": "Express.js",
            "next": "Next.js",
            "react": "React",
            "vue": "Vue",
            "fastify": "Fastify",
            "@nestjs/core": "NestJS",
            "flask": "Flask",
            "django": "Django",
            "fastapi": "FastAPI",
        }

        for dependency, framework in frameworks.items():

            if dependency in dependencies:
                self.framework = framework
                return

    # ----------------------------------------
    # Database Detection
    # ----------------------------------------

    def detect_database(self, dependencies):

        databases = {
            "mongoose": "MongoDB",
            "mongodb": "MongoDB",
            "pg": "PostgreSQL",
            "mysql2": "MySQL",
            "sqlite3": "SQLite",
            "prisma": "Prisma",
        }

        for dependency, database in databases.items():

            if dependency in dependencies:
                self.database = database
                return

    # ----------------------------------------
    # Context
    # ----------------------------------------

    def get_context(self):
        """
        Return repository metadata.
        """

        return {
            "language": self.language,
            "framework": self.framework,
            "database": self.database,
            "package_manager": self.package_manager,
            "files": self.files,
            "total_files": len(self.files),
        }

    # ----------------------------------------
    # Pretty Summary
    # ----------------------------------------

    def summary(self):

        print("=" * 60)
        print("Repository Analysis")
        print("=" * 60)

        print(f"Language          : {self.language}")
        print(f"Framework         : {self.framework}")
        print(f"Database          : {self.database}")
        print(f"Package Manager   : {self.package_manager}")

        print("\nImportant Files")
        print("-" * 60)

        for file in self.files:
            print(f"✓ {file}")

        print(f"\nTotal Files: {len(self.files)}")