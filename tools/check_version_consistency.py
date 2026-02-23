#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


VERSION_LINE_RE = re.compile(r"(?m)^Version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$")
PYPROJECT_VERSION_RE = re.compile(r'(?m)^version\s*=\s*"([^"]+)"\s*$')
CHANGELOG_TOP_RE = re.compile(r"(?m)^##\s+([0-9]+\.[0-9]+\.[0-9]+)\s+\(")
DEFAULT_VERSION_RE = re.compile(r'(?m)^DEFAULT_VERSION\s*=\s*"([^"]+)"\s*$')


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _extract(pattern: re.Pattern[str], text: str, *, label: str) -> str:
    match = pattern.search(text)
    if not match:
        raise ValueError(f"{label} not found")
    return str(match.group(1)).strip()


def check_versions(
    *,
    readme_path: Path,
    pyproject_path: Path,
    changelog_path: Path,
    versioning_path: Path,
) -> dict[str, str]:
    readme_ver = _extract(VERSION_LINE_RE, _read(readme_path), label="README Version")
    pyproject_ver = _extract(PYPROJECT_VERSION_RE, _read(pyproject_path), label="pyproject version")
    changelog_ver = _extract(CHANGELOG_TOP_RE, _read(changelog_path), label="CHANGELOG top version")
    default_ver = _extract(DEFAULT_VERSION_RE, _read(versioning_path), label="DEFAULT_VERSION")
    return {
        "README": readme_ver,
        "pyproject.toml": pyproject_ver,
        "CHANGELOG": changelog_ver,
        "versioning.DEFAULT_VERSION": default_ver,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check version consistency across README/pyproject/changelog/code.")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--pyproject", default="pyproject.toml")
    parser.add_argument("--changelog", default="CHANGELOG.md")
    parser.add_argument("--versioning", default="src/federlicht/versioning.py")
    args = parser.parse_args()

    versions = check_versions(
        readme_path=Path(args.readme),
        pyproject_path=Path(args.pyproject),
        changelog_path=Path(args.changelog),
        versioning_path=Path(args.versioning),
    )
    unique = sorted(set(versions.values()))
    print("version-sources:")
    for key, value in versions.items():
        print(f"- {key}: {value}")
    if len(unique) == 1:
        print(f"version-consistency | PASS | version={unique[0]}")
        return 0
    print(f"version-consistency | FAIL | versions={unique}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

