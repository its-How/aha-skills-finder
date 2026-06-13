#!/usr/bin/env python3
"""Validate bundled examples against the shipped JSON Schema subset.

This is intentionally dependency-free for release gating. It supports the
schema features used by this package and fails closed on unsupported keywords.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path


IGNORED_KEYS = {
    "$schema",
    "$id",
    "title",
    "description",
    "default",
}


def fail(message: str) -> None:
    print(f"schema compatibility failed: {message}", file=sys.stderr)
    sys.exit(1)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON: {exc}")


def type_matches(value: object, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    fail(f"unsupported schema type {expected!r}")


def assert_supported(schema: dict, path: str) -> None:
    supported = {
        *IGNORED_KEYS,
        "type",
        "additionalProperties",
        "required",
        "properties",
        "const",
        "enum",
        "items",
        "minItems",
        "minLength",
        "pattern",
        "minimum",
        "anyOf",
        "format",
    }
    for key in schema:
        if key not in supported:
            fail(f"{path}: unsupported schema keyword {key!r}")


def validate(value: object, schema: object, path: str) -> None:
    if not isinstance(schema, dict):
        fail(f"{path}: schema node is not an object")
    assert_supported(schema, path)

    if "anyOf" in schema:
        errors = []
        for option in schema["anyOf"]:
            try:
                validate(value, option, path)
                return
            except ValueError as exc:
                errors.append(str(exc))
        raise ValueError(f"{path}: did not match anyOf: {'; '.join(errors)}")

    if "const" in schema and value != schema["const"]:
        raise ValueError(f"{path}: expected const {schema['const']!r}, got {value!r}")

    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{path}: expected one of {schema['enum']!r}, got {value!r}")

    if "type" in schema:
        expected = schema["type"]
        expected_types = expected if isinstance(expected, list) else [expected]
        if not any(type_matches(value, item) for item in expected_types):
            raise ValueError(f"{path}: expected type {expected!r}, got {type(value).__name__}")

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                raise ValueError(f"{path}: missing required key {key!r}")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(properties))
            if extra:
                raise ValueError(f"{path}: additional properties {extra!r}")

        for key, subschema in properties.items():
            if key in value:
                validate(value[key], subschema, f"{path}.{key}")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ValueError(f"{path}: expected at least {schema['minItems']} item(s)")
        if "items" in schema:
            for index, item in enumerate(value):
                validate(item, schema["items"], f"{path}[{index}]")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise ValueError(f"{path}: shorter than minLength {schema['minLength']}")
        if "pattern" in schema and re.match(schema["pattern"], value) is None:
            raise ValueError(f"{path}: does not match pattern {schema['pattern']!r}")
        if schema.get("format") == "date":
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError as exc:
                raise ValueError(f"{path}: invalid date format") from exc

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise ValueError(f"{path}: below minimum {schema['minimum']}")


def validate_file(example: Path, schema: Path) -> None:
    data = load_json(example)
    schema_data = load_json(schema)
    try:
        validate(data, schema_data, str(example))
    except ValueError as exc:
        fail(str(exc))


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    skill_dir = root / "aha-skills-finder"
    candidate_schema = skill_dir / "schemas" / "candidate-pool.schema.json"
    brief_schema = skill_dir / "schemas" / "research-brief.schema.json"

    example_dirs = sorted((skill_dir / "examples").glob("find-skill-*"))
    if not example_dirs:
        fail("no example directories found")

    for example_dir in example_dirs:
        validate_file(example_dir / "candidate-pool.json", candidate_schema)
        validate_file(example_dir / "research-brief.json", brief_schema)

    print(f"schema compatibility validated for {len(example_dirs)} example set(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
