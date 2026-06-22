#!/usr/bin/env python3
"""Validate npm package inventory and file-distribution boundaries."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_PATHS = [
    "aha-skills-finder/SKILL.md",
    "aha-skills-finder/sources.yaml",
    "aha-skills-finder/source-registries/curated-skill-lists.yaml",
    "aha-skills-finder/schemas/research-brief.schema.json",
    "aha-skills-finder/schemas/candidate-pool.schema.json",
    "aha-skills-finder/scripts/validate-candidate-pool.py",
    "aha-skills-finder/scripts/validate-skill.py",
    "aha-skills-finder/examples/find-skill-finder/research-brief.json",
    "aha-skills-finder/examples/find-skill-finder/candidate-pool.json",
    "README.md",
    "INSTALL.md",
    "USAGE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "LICENSE",
    "package.json",
]

REQUIRED_FILE_ENTRIES = [
    "aha-skills-finder/",
    "README.md",
    "INSTALL.md",
    "USAGE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "LICENSE",
]

FORBIDDEN_PACKAGE_KEYS = {"bin", "main", "exports"}


def validate(repo_root: Path) -> None:
    package_path = repo_root / "package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))

    forbidden = sorted(FORBIDDEN_PACKAGE_KEYS.intersection(package))
    if forbidden:
        raise ValueError(f"package.json must not define CLI/API keys: {', '.join(forbidden)}")

    files = package.get("files")
    if not isinstance(files, list):
        raise ValueError("package.json files must be an explicit list")
    missing_entries = [entry for entry in REQUIRED_FILE_ENTRIES if entry not in files]
    if missing_entries:
        raise ValueError(f"package.json files missing entries: {', '.join(missing_entries)}")

    missing_paths = [path for path in REQUIRED_PATHS if not (repo_root / path).exists()]
    if missing_paths:
        raise ValueError(f"package inventory missing paths: {', '.join(missing_paths)}")

    adapter_files = list((repo_root / "aha-skills-finder/adapters").glob("**/*"))
    if any(path.is_file() for path in adapter_files):
        raise ValueError("placeholder runtime adapters must not ship")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate-package.py <repo-root>", file=sys.stderr)
        return 2
    try:
        validate(Path(argv[1]))
    except ValueError as exc:
        print(f"package validation failed: {exc}", file=sys.stderr)
        return 1
    print("package inventory validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
