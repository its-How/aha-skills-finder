#!/usr/bin/env python3
"""Validate the minimal portable SKILL.md contract for this repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter must be closed with ---")

    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"frontmatter line is not key:value: {line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in values:
            raise ValueError(f"duplicate frontmatter key: {key}")
        values[key] = value
    return values


def validate(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise ValueError(f"missing SKILL.md at {skill_md}")

    values = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if set(values) != {"name", "description"}:
        raise ValueError("frontmatter must contain exactly name and description")
    if values["name"] != skill_dir.name:
        raise ValueError("frontmatter name must match skill directory name")
    if not NAME_RE.match(values["name"]):
        raise ValueError("frontmatter name must use lowercase letters, digits, and hyphens")
    if len(values["description"]) < 80:
        raise ValueError("frontmatter description is too short to route the skill")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate-skill.py <skill-directory>", file=sys.stderr)
        return 2
    try:
        validate(Path(argv[1]))
    except ValueError as exc:
        print(f"skill validation failed: {exc}", file=sys.stderr)
        return 1
    print("skill validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
