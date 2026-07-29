from pathlib import Path

from core.context import AgentContext
from core.models import DependencyReport


class DependencyChecker:
    """
    Detects repository language, framework, package manager,
    and common build commands.
    """

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)

    # ==========================================================
    # Public API
    # ==========================================================

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:

        self._print_header()

        report = DependencyReport()

        files = self._scan_repository()

        report.detected_files = sorted(files)

        report.language = self._detect_language(files)

        report.framework = self._detect_framework(files)

        report.package_manager = self._detect_package_manager(files)

        self._build_commands(report)

        self._validate(report)

        context.dependency_report = report

        self._print_summary(report)

        return context

    # ==========================================================
    # Repository Scan
    # ==========================================================

    def _scan_repository(self) -> set[str]:

        detected = set()

        for path in self.repository_path.rglob("*"):

            if path.is_file():
                detected.add(path.name)

        return detected

    # ==========================================================
    # Detection
    # ==========================================================

    def _detect_language(
        self,
        files: set[str],
    ) -> str:

        if "Cargo.toml" in files:
            return "Rust"

        if (
            "requirements.txt" in files
            or "pyproject.toml" in files
        ):
            return "Python"

        if "tsconfig.json" in files:
            return "TypeScript"

        if "package.json" in files:
            return "JavaScript"

        return "Unknown"

    def _detect_framework(
        self,
        files: set[str],
    ) -> str:

        if (
            "next.config.js" in files
            or "next.config.ts" in files
        ):
            return "Next.js"

        if (
            "vite.config.js" in files
            or "vite.config.ts" in files
        ):
            return "React (Vite)"

        if "manage.py" in files:
            return "Django"

        if (
            "app.py" in files
            or "wsgi.py" in files
        ):
            return "Flask"

        if "Cargo.toml" in files:
            return "Rust"

        if "package.json" in files:
            return "Node.js"

        return "Unknown"

    def _detect_package_manager(
        self,
        files: set[str],
    ) -> str:

        if "pnpm-lock.yaml" in files:
            return "pnpm"

        if "yarn.lock" in files:
            return "yarn"

        if "package-lock.json" in files:
            return "npm"

        if "Cargo.toml" in files:
            return "cargo"

        if (
            "requirements.txt" in files
            or "pyproject.toml" in files
        ):
            return "pip"

        return "Unknown"

    # ==========================================================
    # Commands
    # ==========================================================

    def _build_commands(
        self,
        report: DependencyReport,
    ) -> None:

        pm = report.package_manager

        if pm == "pnpm":

            report.install_command = "pnpm install"
            report.build_command = "pnpm build"
            report.run_command = "pnpm dev"

        elif pm == "npm":

            report.install_command = "npm install"
            report.build_command = "npm run build"
            report.run_command = "npm run dev"

        elif pm == "yarn":

            report.install_command = "yarn"
            report.build_command = "yarn build"
            report.run_command = "yarn dev"

        elif pm == "cargo":

            report.install_command = "cargo fetch"
            report.build_command = "cargo build"
            report.run_command = "cargo run"

        elif pm == "pip":

            report.install_command = (
                "pip install -r requirements.txt"
            )
            report.build_command = None
            report.run_command = "python app.py"

    # ==========================================================
    # Validation
    # ==========================================================

    def _validate(
        self,
        report: DependencyReport,
    ) -> None:

        if report.framework == "Unknown":
            report.warnings.append(
                "Framework could not be detected."
            )

        if report.package_manager == "Unknown":
            report.warnings.append(
                "Package manager could not be detected."
            )

    # ==========================================================
    # Console Output
    # ==========================================================

    def _print_header(self) -> None:

        print("\n" + "=" * 70)
        print("📦 Dependency Checker")
        print("=" * 70)

    def _print_summary(
        self,
        report: DependencyReport,
    ) -> None:

        print(f"Language         : {report.language}")
        print(f"Framework        : {report.framework}")
        print(f"Package Manager  : {report.package_manager}")
        print(f"Install Command  : {report.install_command}")
        print(f"Build Command    : {report.build_command}")
        print(f"Run Command      : {report.run_command}")
        print(f"Warnings         : {len(report.warnings)}")