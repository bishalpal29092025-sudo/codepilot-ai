import json
from pathlib import Path

from repository.detector import RepositoryDetector
from repository.loader import RepositoryLoader


def create_loader(tmp_path: Path) -> RepositoryLoader:
    """
    Helper to create and load a RepositoryLoader.
    """
    loader = RepositoryLoader(tmp_path)
    loader.load()
    return loader


def test_detect_python_language(tmp_path: Path) -> None:
    """Detector should identify Python as the primary language."""

    files = [
        "main.py",
        "utils.py",
        "config.py",
    ]

    loader = create_loader(tmp_path)

    detector = RepositoryDetector(files, loader)
    info = detector.detect()

    assert info.language == "Python"


def test_detect_nextjs_framework(tmp_path: Path) -> None:
    """Detector should identify Next.js from package.json."""

    package = {
        "dependencies": {
            "next": "^15.0.0",
            "react": "^19.0.0",
        }
    }

    (tmp_path / "package.json").write_text(json.dumps(package))

    loader = create_loader(tmp_path)

    detector = RepositoryDetector(
        files=["package.json"],
        loader=loader,
    )

    info = detector.detect()

    assert info.framework == "Next.js"


def test_detect_fastapi_framework(tmp_path: Path) -> None:
    """Detector should identify FastAPI from requirements.txt."""

    (tmp_path / "requirements.txt").write_text(
        "fastapi\nuvicorn\n"
    )

    loader = create_loader(tmp_path)

    detector = RepositoryDetector(
        files=["requirements.txt"],
        loader=loader,
    )

    info = detector.detect()

    assert info.framework == "FastAPI"


def test_detect_mongodb_database(tmp_path: Path) -> None:
    """Detector should identify MongoDB."""

    package = {
        "dependencies": {
            "mongoose": "^8.0.0",
        }
    }

    (tmp_path / "package.json").write_text(json.dumps(package))

    loader = create_loader(tmp_path)

    detector = RepositoryDetector(
        files=["package.json"],
        loader=loader,
    )

    info = detector.detect()

    assert info.database == "MongoDB"


def test_detect_package_manager(tmp_path: Path) -> None:
    """Detector should identify npm."""

    loader = create_loader(tmp_path)

    detector = RepositoryDetector(
        files=[
            "package.json",
            "package-lock.json",
        ],
        loader=loader,
    )

    info = detector.detect()

    assert info.package_manager == "npm"


def test_unknown_repository(tmp_path: Path) -> None:
    """Unknown repositories should return Unknown values."""

    loader = create_loader(tmp_path)

    detector = RepositoryDetector(
        files=[],
        loader=loader,
    )

    info = detector.detect()

    assert info.language == "Unknown"
    assert info.framework == "Unknown"
    assert info.database == "Unknown"
    assert info.package_manager == "Unknown"