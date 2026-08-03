from git_safety import (
    PatchEngine,
    PatchOperation,
)


def test_create_patch():

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

    engine = PatchEngine(".")


    patch = engine.create_patch(
        "test_patch_file.txt",
        "hello CodePilot",
    )


    engine.apply_patch(
        patch
    )


    with open(
        "test_patch_file.txt",
        "r",
        encoding="utf-8",
    ) as file:

        content = file.read()


    assert content == "hello CodePilot"