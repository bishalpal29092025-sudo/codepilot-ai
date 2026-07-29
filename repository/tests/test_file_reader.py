from pathlib import Path

import pytest

from repository.exceptions import RepositoryReadError
from repository.file_reader import RepositoryFileReader


def test_read_file(tmp_path: Path) -> None:
    reader = RepositoryFileReader(tmp_path)

    file = tmp_path / "hello.txt"
    file.write_text("Hello CodePilot")

    assert reader.read("hello.txt") == "Hello CodePilot"


def test_exists(tmp_path: Path) -> None:
    reader = RepositoryFileReader(tmp_path)

    (tmp_path / "demo.txt").write_text("demo")

    assert reader.exists("demo.txt")
    assert not reader.exists("missing.txt")


def test_size(tmp_path: Path) -> None:
    reader = RepositoryFileReader(tmp_path)

    file = tmp_path / "size.txt"
    file.write_text("12345")

    assert reader.size("size.txt") == 5


def test_read_if_exists(tmp_path: Path) -> None:
    reader = RepositoryFileReader(tmp_path)

    assert reader.read_if_exists("missing.txt") is None

    (tmp_path / "demo.txt").write_text("Hello")

    assert reader.read_if_exists("demo.txt") == "Hello"


def test_large_file(tmp_path: Path) -> None:
    reader = RepositoryFileReader(tmp_path)

    file = tmp_path / "big.txt"

    file.write_text("a" * (reader.max_file_size + 1))

    with pytest.raises(RepositoryReadError):
        reader.read("big.txt")