from pathlib import Path

from git_safety import (
    PatchEngine,
    PatchOperation,
)


def test_create_patch():

    file_path = Path(
        "test_patch_file.txt"
    )

    if file_path.exists():
        file_path.unlink()


    engine = PatchEngine(".")


    patch = engine.create_patch(
        "test_patch_file.txt",
        "hello CodePilot",
    )


    assert patch.file_path == "test_patch_file.txt"

    assert patch.operation == (
        PatchOperation.CREATE
    )



def test_apply_patch():

    file_path = Path(
        "test_patch_file.txt"
    )


    if file_path.exists():
        file_path.unlink()


    engine = PatchEngine(".")


    patch = engine.create_patch(
        "test_patch_file.txt",
        "hello CodePilot",
    )


    engine.apply_patch(
        patch
    )


    assert (
        file_path.read_text(
            encoding="utf-8"
        )
        == "hello CodePilot"
    )


    file_path.unlink()