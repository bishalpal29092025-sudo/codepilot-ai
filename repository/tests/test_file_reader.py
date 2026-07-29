from pathlib import Path

import pytest

from repository.file_reader import RepositoryFileReader


def test_read_file(tmp_path: Path):
    file = tmp_path / "hello.txt"
    file.write_text("Hello CodePilot")

    reader = RepositoryFileReader(tmp_path)

    assert reader.read("hello.txt") == "Hello CodePilot"


def test_exists(tmp_path: Path):
    (tmp_path / "demo.txt").write_text("demo")

    reader = RepositoryFileReader(tmp_path)

    assert reader.exists("demo.txt")
    assert not reader.exists("missing.txt")


def test_size(tmp_path: Path):
    (tmp_path / "a.txt").write_text("abcd")

    reader = RepositoryFileReader(tmp_path)

    assert reader.size("a.txt") == 4


def test_read_if_exists(tmp_path: Path):
    reader = RepositoryFileReader(tmp_path)

    assert reader.read_if_exists("missing.txt") is None


def test_large_file(tmp_path: Path):
    reader = RepositoryFileReader(tmp_path)

    file = tmp_path / "big.txt"

    file.write_text("a" * (reader.MAX_FILE_SIZE + 1))

    with pytest.raises(ValueError):
        reader.read("big.txt")