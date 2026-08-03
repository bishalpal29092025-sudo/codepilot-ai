from pathlib import Path

from git_safety import (
    SnapshotManager,
    RollbackEngine,
)



def test_rollback():

    test_file = Path(
        "rollback_test.txt"
    )


    test_file.write_text(
        "original",
        encoding="utf-8",
    )


    snapshot_manager = SnapshotManager(".")

    snapshot = snapshot_manager.create_snapshot()



    test_file.write_text(
        "changed",
        encoding="utf-8",
    )


    assert (
        test_file.read_text()
        == "changed"
    )


    rollback = RollbackEngine(".")

    result = rollback.restore_snapshot(
        snapshot
    )


    assert result.success


    assert (
        test_file.read_text()
        == "original"
    )


    test_file.unlink()