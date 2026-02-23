from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_tool():
    path = Path("tools/check_version_consistency.py")
    spec = importlib.util.spec_from_file_location("check_version_consistency", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tool = _load_tool()


def test_check_versions_reads_current_repo() -> None:
    versions = tool.check_versions(
        readme_path=Path("README.md"),
        pyproject_path=Path("pyproject.toml"),
        changelog_path=Path("CHANGELOG.md"),
        versioning_path=Path("src/federlicht/versioning.py"),
    )
    assert "README" in versions
    assert "pyproject.toml" in versions
    assert "CHANGELOG" in versions
    assert "versioning.DEFAULT_VERSION" in versions

