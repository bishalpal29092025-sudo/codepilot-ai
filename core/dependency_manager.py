"""
Dependency Manager.

Analyzes repository dependencies and creates
a DependencyReport used by execution stages.
"""

from __future__ import annotations

import json
from pathlib import Path

from core.context import AgentContext
from core.models import DependencyReport


class DependencyManager:
    """
    Detects project dependencies and runtime commands.

    Responsibilities:

    - Detect language
    - Detect package manager
    - Detect install command
    - Detect build command
    - Detect run command
    - Store DependencyReport in AgentContext

    It does NOT:
        - Install packages
        - Execute commands
        - Modify repository
    """


    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Pipeline entry point.
        """

        self._print_header()


        repository = context.repository_info

        if repository is None:
            raise ValueError(
                "Repository information missing."
            )


        report = self._analyze(
            repository.root_path
        )


        context.dependency_report = report


        self._print_summary(
            report
        )


        return context



    # ==========================================================
    # Analysis
    # ==========================================================

    def _analyze(
        self,
        repository_path: str,
    ) -> DependencyReport:

        root = Path(
            repository_path
        )


        package_json = root / "package.json"


        if package_json.exists():

            return self._analyze_node(
                package_json
            )


        requirements = root / "requirements.txt"


        if requirements.exists():

            return DependencyReport(
                language="Python",
                framework="Unknown",
                package_manager="pip",
                install_command="pip install -r requirements.txt",
                build_command="",
                run_command="",
                warnings=[],
            )


        return DependencyReport(
            language="Unknown",
            framework="Unknown",
            package_manager="Unknown",
            install_command="",
            build_command="",
            run_command="",
            warnings=[
                "Unable to detect dependency manager."
            ],
        )



    # ==========================================================
    # Node.js Detection
    # ==========================================================

    def _analyze_node(
        self,
        package_json: Path,
    ) -> DependencyReport:

        with package_json.open(
            "r",
            encoding="utf-8",
        ) as file:

            package = json.load(
                file
            )


        scripts = package.get(
            "scripts",
            {}
        )


        dependencies = {}

        dependencies.update(
            package.get(
                "dependencies",
                {}
            )
        )

        dependencies.update(
            package.get(
                "devDependencies",
                {}
            )
        )


        framework = "Node.js"


        if "next" in dependencies:
            framework = "Next.js"

        elif "express" in dependencies:
            framework = "Express.js"

        elif "react" in dependencies:
            framework = "React"



        build_command = ""

        if "build" in scripts:
            build_command = (
                "npm run build"
            )


        run_command = ""

        if "dev" in scripts:
            run_command = (
                "npm run dev"
            )

        elif "start" in scripts:
            run_command = (
                "npm start"
            )


        return DependencyReport(
            language="JavaScript",
            framework=framework,
            package_manager="npm",
            install_command="npm install",
            build_command=build_command,
            run_command=run_command,
            warnings=[],
        )



    # ==========================================================
    # Console
    # ==========================================================

    def _print_header(self):

        print("\n" + "=" * 70)
        print("📦 Dependency Manager")
        print("=" * 70)



    def _print_summary(
        self,
        report: DependencyReport,
    ):

        print(
            f"Language         : {report.language}"
        )

        print(
            f"Framework        : {report.framework}"
        )

        print(
            f"Package Manager  : {report.package_manager}"
        )

        print(
            f"Install Command  : {report.install_command}"
        )

        print(
            f"Build Command    : {report.build_command}"
        )

        print(
            f"Run Command      : {report.run_command}"
        )

        print(
            f"Warnings         : {len(report.warnings)}"
        )