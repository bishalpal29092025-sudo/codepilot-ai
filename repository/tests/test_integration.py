import json
from pathlib import Path

from repository.explorer import RepositoryExplorer


def test_repository_pipeline(tmp_path: Path) -> None:
    """
    End-to-end test of the repository analysis pipeline.
    """

    package = {
        "dependencies": {
            "next": "^15.0.0",
            "react": "^19.0.0",
            "mongoose": "^8.0.0",
        }
    }

    (tmp_path / "package.json").write_text(json.dumps(package))
    (tmp_path / "package-lock.json").write_text("{}")
    (tmp_path / "README.md").write_text("# Demo")
    (tmp_path / "index.ts").write_text(
        "console.log('Hello CodePilot');"
    )

    explorer = RepositoryExplorer(tmp_path)

    info = explorer.explore()

    assert info.language == "TypeScript"
    assert info.framework == "Next.js"
    assert info.database == "MongoDB"
    assert info.package_manager == "npm"

    assert info.total_files == 4

    assert sorted(info.files) == [
        "README.md",
        "index.ts",
        "package-lock.json",
        "package.json",
    ]