"""
Tests for CodePilot Git Diff Engine.
"""

from git_safety import DiffEngine, DiffReport


def test_diff_engine_creation():

    engine = DiffEngine(".")

    report = engine.generate_diff()

    assert report is not None

    assert isinstance(
        report,
        DiffReport,
    )


def test_diff_report_structure():

    engine = DiffEngine(".")

    report = engine.generate_diff()

    assert hasattr(
        report,
        "files",
    )

    assert hasattr(
        report,
        "total_additions",
    )

    assert hasattr(
        report,
        "total_deletions",
    )

    assert isinstance(
        report.total_additions,
        int,
    )

    assert isinstance(
        report.total_deletions,
        int,
    )