import json
from pathlib import Path

from repository.loader import RepositoryLoader


def test_load_package_json(tmp_path: Path) -> None:
    """Package.json should be parsed into a dictionary."""

    package = {
        "name": "demo",
        "dependencies": {
            "react": "^19.0.0",
        },
    }

    (tmp_path / "package.json").write_text(json.dumps(package))

    loader = RepositoryLoader(tmp_path)
    loader.load()

    assert loader.package_json["name"] == "demo"
    assert "react" in loader.package_json["dependencies"]


def test_load_requirements(tmp_path: Path) -> None:
    """requirements.txt should be loaded."""

    (tmp_path / "requirements.txt").write_text(
        "fastapi\nuvicorn\n"
    )

    loader = RepositoryLoader(tmp_path)
    loader.load()

    assert "fastapi" in loader.requirements
    assert "uvicorn" in loader.requirements


def test_missing_files(tmp_path: Path) -> None:
    """Missing metadata files should return empty values."""

    loader = RepositoryLoader(tmp_path)
    loader.load()

    assert loader.package_json == {}
    assert loader.requirements == ""
    assert loader.pyproject == ""
    assert loader.cargo_toml == ""
    assert loader.go_mod == ""


def test_invalid_package_json(tmp_path: Path) -> None:
    """Invalid JSON should not raise an exception."""

    (tmp_path / "package.json").write_text("{ invalid json")

    loader = RepositoryLoader(tmp_path)
    loader.load()

    assert loader.package_json == {}


def test_load_all_metadata(tmp_path: Path) -> None:
    """All supported metadata files should be loaded."""

    (tmp_path / "package.json").write_text("{}")
    (tmp_path / "requirements.txt").write_text("fastapi")
    (tmp_path / "pyproject.toml").write_text("[project]")
    (tmp_path / "Cargo.toml").write_text("[package]")
    (tmp_path / "go.mod").write_text("module demo")

    loader = RepositoryLoader(tmp_path)
    loader.load()

    assert loader.package_json == {}
    assert loader.requirements == "fastapi"
    assert loader.pyproject == "[project]"
    assert loader.cargo_toml == "[package]"
    assert loader.go_mod == "module demo"