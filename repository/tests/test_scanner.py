from pathlib import Path

from repository.scanner import RepositoryScanner


def test_scan_python_repository(tmp_path: Path) -> None:
    """Scanner should discover supported source files."""

    (tmp_path / "app.py").write_text("print('hello')")
    (tmp_path / "README.md").write_text("# Demo")
    (tmp_path / "package.json").write_text("{}")

    scanner = RepositoryScanner(tmp_path)

    files = scanner.scan()

    assert "app.py" in files
    assert "README.md" in files
    assert "package.json" in files
    assert len(files) == 3


def test_ignore_directories(tmp_path: Path) -> None:
    """Ignored directories should not be scanned."""

    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()

    (node_modules / "index.js").write_text("console.log('ignore')")

    scanner = RepositoryScanner(tmp_path)

    files = scanner.scan()

    assert files == []


def test_ignore_hidden_files(tmp_path: Path) -> None:
    """Hidden files should be ignored unless explicitly allowed."""

    (tmp_path / ".secret").write_text("hidden")
    (tmp_path / ".gitignore").write_text("*.pyc")

    scanner = RepositoryScanner(tmp_path)

    files = scanner.scan()

    assert ".gitignore" in files
    assert ".secret" not in files


def test_scan_nested_directories(tmp_path: Path) -> None:
    """Scanner should return repository-relative paths."""

    src = tmp_path / "src"
    src.mkdir()

    (src / "main.py").write_text("print('nested')")

    scanner = RepositoryScanner(tmp_path)

    files = scanner.scan()

    assert files == ["src/main.py"]