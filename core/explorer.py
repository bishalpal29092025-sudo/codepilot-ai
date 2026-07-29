"""
Repository Explorer.

Analyzes repository structure and extracts metadata
required by the CodePilot AI pipeline.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from core.context import AgentContext

from core.models import (
    RepositoryInfo,
    ProgrammingLanguage,
    ProjectType,
)


class RepositoryExplorer:
    """
    Explores a repository and extracts metadata required
    by CodePilot AI.
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


    def __init__(
        self,
        repo_path: str,
    ) -> None:

        self.repo_path = repo_path

        self.language = "Unknown"
        self.framework = "Unknown"
        self.database = "Unknown"
        self.package_manager = "Unknown"

        self.files: list[str] = []

        self.scan()
        self.detect_project()



    # =========================================================
    # Pipeline API
    # =========================================================

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Pipeline execution.

        Stores repository information
        inside AgentContext.
        """

        context.repository_info = (
            self.get_repository_info()
        )

        return context



    # =========================================================
    # Scan Repository
    # =========================================================

    def scan(self) -> None:

        self.files.clear()


        for root, dirs, files in os.walk(
            self.repo_path
        ):

            dirs[:] = [
                directory
                for directory in dirs
                if directory not in self.IGNORE_DIRS
            ]


            for file in files:


                if (
                    file.startswith(".")
                    and file not in {
                        ".env",
                        ".gitignore",
                    }
                ):
                    continue


                relative_path = os.path.relpath(
                    os.path.join(
                        root,
                        file,
                    ),
                    self.repo_path,
                )


                extension = Path(file).suffix


                if (
                    extension in self.IMPORTANT_EXTENSIONS
                    or file in self.IMPORTANT_FILES
                ):

                    self.files.append(
                        relative_path
                    )


        self.files.sort()



    # =========================================================
    # Project Detection
    # =========================================================

    def detect_project(self) -> None:


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
                ) as file:

                    package = json.load(file)


                dependencies = {}

                dependencies.update(
                    package.get(
                        "dependencies",
                        {},
                    )
                )

                dependencies.update(
                    package.get(
                        "devDependencies",
                        {},
                    )
                )


                self.detect_framework(
                    dependencies
                )

                self.detect_database(
                    dependencies
                )


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



    # =========================================================
    # Framework Detection
    # =========================================================

    def detect_framework(
        self,
        dependencies: dict,
    ) -> None:


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



    # =========================================================
    # Database Detection
    # =========================================================

    def detect_database(
        self,
        dependencies: dict,
    ) -> None:


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



    # =========================================================
    # Repository Info
    # =========================================================

    def get_repository_info(
        self,
    ) -> RepositoryInfo:
        """
        Convert explorer data into
        RepositoryInfo model.
        """


        language_map = {

            "JavaScript":
                ProgrammingLanguage.JAVASCRIPT,

            "Python":
                ProgrammingLanguage.PYTHON,

            "Rust":
                ProgrammingLanguage.RUST,

            "Unknown":
                ProgrammingLanguage.UNKNOWN,
        }



        project_type = (
            ProjectType.WEB
        )


        if self.framework in {
            "Express.js",
            "FastAPI",
            "Flask",
            "Django",
        }:

            project_type = (
                ProjectType.BACKEND
            )



        entry_points = [

            file
            for file in self.files
            if file in {

                "index.js",

                "main.py",

                "app.py",

                "main.rs",

            }

        ]



        return RepositoryInfo(

            name=Path(
                self.repo_path
            ).name,


            root_path=str(
                Path(
                    self.repo_path
                ).absolute()
            ),


            project_type=project_type,


            primary_language=language_map.get(
                self.language,
                ProgrammingLanguage.UNKNOWN,
            ),


            frameworks=(

                [self.framework]

                if self.framework != "Unknown"

                else []

            ),


            database=self.database,


            package_manager=self.package_manager,


            entry_points=entry_points,


            ignored_directories=list(
                self.IGNORE_DIRS
            ),


            repository_files=self.files,


            total_files=len(
                self.files
            ),


            metadata={

                "detected_language":
                    self.language,

                "detected_framework":
                    self.framework,

            },

        )



    # Backward compatibility

    def get_context(self):

        return self.get_repository_info()



    # =========================================================
    # Console
    # =========================================================

    def summary(self):

        info = self.get_repository_info()


        print("=" * 60)
        print("Repository Analysis")
        print("=" * 60)


        print(
            f"Name              : {info.name}"
        )

        print(
            f"Language          : {info.primary_language}"
        )

        print(
            f"Frameworks        : {info.frameworks}"
        )

        print(
            f"Database          : {info.database}"
        )

        print(
            f"Package Manager   : {info.package_manager}"
        )


        print("\nImportant Files")
        print("-" * 60)


        for file in info.repository_files:

            print(
                f"✓ {file}"
            )


        print(
            f"\nTotal Files: {info.total_files}"
        )