from git_safety import SnapshotManager


def test_snapshot_creation():

    manager = SnapshotManager(".")

    snapshot = manager.create_snapshot()

    assert snapshot.repository_path
    assert snapshot.commit_hash
    assert snapshot.branch