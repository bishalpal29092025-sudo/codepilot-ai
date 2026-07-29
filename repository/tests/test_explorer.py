import json
from pathlib import Path

from repository.explorer import RepositoryExplorer


def test_explore_python_repository(tmp_path: Path) -> None:
    """Explorer should analyse a simple Python repository."""

    (tmp_path / "main.py").write_text("print('hello')")
    (tmp_path / "requirements.txt").write_text("fastapi\nuvicorn\n")

    explorer = RepositoryExplorer(tmp_path)

    info = explorer.explore()

    assert info.language == "Python"
    assert info.framework == "FastAPI"
    assert info.package_manager == "pip"
    assert info.total_files == 2


def test_explore_nextjs_repository(tmp_path: Path) -> None:
    """Explorer should analyse a Next.js repository."""

    package = {
        "dependencies": {
            "next": "^15.0.0",
            "react": "^19.0.0",
        }
    }

    (tmp_path / "package.json").write_text(json.dumps(package))
    (tmp_path / "package-lock.json").write_text("{}")
    (tmp_path / "index.ts").write_text("console.log('hello');")

    explorer = RepositoryExplorer(tmp_path)

    info = explorer.explore()

    assert info.language == "TypeScript"
    assert info.framework == "Next.js"
    assert info.package_manager == "npm"


def test_explore_empty_repository(tmp_path: Path) -> None:
    """Explorer should handle an empty repository."""

    explorer = RepositoryExplorer(tmp_path)

    info = explorer.explore()

    assert info.language == "Unknown"
    assert info.framework == "Unknown"
    assert info.database == "Unknown"
    assert info.package_manager == "Unknown"
    assert info.total_files == 0