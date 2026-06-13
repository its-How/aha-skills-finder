#!/usr/bin/env python3
"""Light red-line checks for aha-skills-finder candidate pool artifacts.

This script is not a full JSON Schema validator and does not judge discovery
quality. It only catches required structural fields and find-stage red lines.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ALLOWED_CANDIDATE_TYPES = {
    "skill",
    "scripted-skill",
    "prompt-only",
    "docs-only",
    "mcp",
    "cli",
    "plugin",
    "registry-search-index",
    "curated-list",
    "extension",
    "saas-provider",
    "repo-tool",
    "native-framework-capability",
}

ALLOWED_CANDIDATE_ROLES = {
    "capability",
    "discovery-source",
    "adjacent-index",
    "adjacent-tooling",
    "registry-index",
}

ALLOWED_QUERY_BRANCHES = {
    "skill-native",
    "runtime-spec",
    "source-code",
    "package-cli",
    "registry-search-index",
    "outcome-native",
    "extension-saas",
    "mcp-agent-tool-catalog",
    "false-positive-mining",
    "curated-community",
    "curated-recommended",
    "package-registry",
    "skill-tooling",
}

ALLOWED_SIGNAL_COMPLETENESS = {"high", "medium", "low", "unknown"}

ALLOWED_ADJACENT_RELATIONSHIPS = {
    "fork",
    "competitor",
    "superset",
    "subset",
    "related-registry-entry",
    "shared-maintainer",
    "shared-ecosystem",
}

ALLOWED_VERIFIED_METHODS = {
    "source_inspection",
    "web_search_corroboration",
    "tool_smoke",
    "docs_only",
}

FORBIDDEN_FIND_STAGE_WORDS = {
    "best overall",
    "top choice",
    "final pick",
    "ranked #1",
    "shortlisted winner",
    "should adopt",
    "adopt this",
    "ready to adopt",
    "adoption verdict",
    "recommend installing",
    "safe to install",
    "approved for use",
    "low risk",
    "maintenance is strong",
    "source quality is high",
    "audit passed",
    "publish now",
}

REGISTRY_STATS_BOUNDARY_TERMS = {
    "not-safety-proof",
    "do-not-treat-registry-clean-as-safety-proof",
    "registry-source-review",
    "registry-native-source-review",
}

SOURCE_ROLE_BOUNDARY_TERMS = {
    "not adoption",
    "not-adoption-proof",
    "curated-label-is-not-adoption-proof",
    "source-only",
    "discovery-source",
}

SOURCE_LIKE_CANDIDATE_TYPES = {
    "registry-search-index",
    "curated-list",
}

SOURCE_LIKE_CANDIDATE_ROLES = {
    "discovery-source",
    "adjacent-index",
    "adjacent-tooling",
    "registry-index",
}

SOURCE_LIKE_CANDIDATE_SURFACES = {
    "registry-index",
    "curated-list",
    "skill-marketplace",
    "skill-installer",
    "skill-manager",
}

PACKAGE_STATS_BOUNDARY_TERMS = {
    "package-stats-raw-only",
    "package-registry-stats-raw-only",
    "not-safety-proof",
    "not-quality-proof",
    "not-adoption-proof",
}

INSTALL_BOUNDARY_TERMS = {
    "install-boundary",
    "no-install",
    "does-not-install",
}

PUBLISH_BOUNDARY_TERMS = {
    "publish-boundary",
    "no-publish",
}

FIND_STAGE_BOUNDARY_REQUIRED_TERMS = {
    "install": ("install",),
    "adopt/use decisions": ("adopt", "use decision"),
    "audit": ("audit",),
    "safety": ("safety",),
    "source": ("source",),
    "permission": ("permission",),
    "maintenance": ("maintenance",),
    "enable": ("enable",),
    "configure": ("configure",),
    "runtime config mutation": ("runtime config", "runtime-config"),
    "publish": ("publish",),
    "deploy": ("deploy",),
    "live": ("live",),
    "external-write": ("external-write", "external write"),
    "provider": ("provider",),
    "browser": ("browser",),
    "credential": ("credential",),
    "login": ("login", "log in"),
}

NEGATION_MARKERS = {
    "does not ",
    "do not ",
    "not ",
    "cannot ",
    "can't ",
    "must not ",
    "no ",
}


def forbidden_find_stage_hits(text: str) -> list[str]:
    hits: list[str] = []
    for word in sorted(FORBIDDEN_FIND_STAGE_WORDS):
        start = 0
        while True:
            index = text.find(word, start)
            if index == -1:
                break

            context = text[max(0, index - 40) : index]
            if not any(marker in context for marker in NEGATION_MARKERS):
                hits.append(word)
                break

            start = index + len(word)
    return hits


def fail(path: Path, message: str) -> None:
    raise ValueError(f"{path}: {message}")


def require_keys(path: Path, obj: dict, keys: list[str], where: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        fail(path, f"{where} missing keys: {', '.join(missing)}")


def validate_candidate_pool(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail(path, "top-level JSON must be an object")

    require_keys(
        path,
        data,
        [
            "schema_version",
            "created",
            "target_outcome",
            "find_stage_boundary",
            "source_gaps",
            "false_positives",
            "candidates",
        ],
        "top-level object",
    )

    if data["schema_version"] != "0.1":
        fail(path, "schema_version must be 0.1")
    artifact_type = data.get("artifact_type", "research-output")
    if artifact_type not in {"research-output", "synthetic-fixture"}:
        fail(path, "artifact_type must be research-output or synthetic-fixture")

    artifact_text = json.dumps(data, ensure_ascii=False).lower()
    forbidden_hits = forbidden_find_stage_hits(artifact_text)
    if forbidden_hits:
        fail(path, f"artifact contains ranking/adoption/audit language {forbidden_hits}")

    boundary = data["find_stage_boundary"]
    if not isinstance(boundary, dict):
        fail(path, "find_stage_boundary must be an object")
    require_keys(path, boundary, ["does", "does_not"], "find_stage_boundary")
    boundary_text = json.dumps(boundary["does_not"], ensure_ascii=False).lower()
    missing_boundary_terms = [
        label
        for label, terms in FIND_STAGE_BOUNDARY_REQUIRED_TERMS.items()
        if not any(term in boundary_text for term in terms)
    ]
    if missing_boundary_terms:
        fail(
            path,
            "find_stage_boundary.does_not must explicitly exclude "
            + ", ".join(missing_boundary_terms),
        )

    candidates = data["candidates"]
    if not isinstance(candidates, list) or not candidates:
        fail(path, "candidates must be a non-empty array")

    seen_ids: set[str] = set()
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            fail(path, f"candidate[{index}] must be an object")
        require_keys(
            path,
            candidate,
            [
                "candidate_id",
                "name",
                "source",
                "entrypoint_url",
                "candidate_type",
                "target_outcome",
                "outcome_mode",
                "query_branch",
                "metrics",
                "find_signals",
                "signal_completeness",
                "false_positive_note",
                "deferred_boundary_tags",
                "notes",
            ],
            f"candidate[{index}]",
        )

        candidate_id = candidate["candidate_id"]
        if candidate_id in seen_ids:
            fail(path, f"duplicate candidate_id: {candidate_id}")
        seen_ids.add(candidate_id)

        candidate_type = candidate["candidate_type"]
        if candidate_type not in ALLOWED_CANDIDATE_TYPES:
            fail(path, f"{candidate_id}: invalid candidate_type {candidate_type!r}")

        candidate_role = candidate.get("candidate_role")
        if candidate_role is not None and candidate_role not in ALLOWED_CANDIDATE_ROLES:
            fail(path, f"{candidate_id}: invalid candidate_role {candidate_role!r}")

        query_branch = candidate["query_branch"]
        if query_branch not in ALLOWED_QUERY_BRANCHES:
            fail(path, f"{candidate_id}: invalid query_branch {query_branch!r}")

        if candidate["signal_completeness"] not in ALLOWED_SIGNAL_COMPLETENESS:
            fail(path, f"{candidate_id}: invalid signal_completeness")

        source = candidate["source"]
        if not isinstance(source, dict):
            fail(path, f"{candidate_id}: source must be an object")
        require_keys(path, source, ["source_family", "source_url", "repo_url"], f"{candidate_id}.source")

        tags = candidate["deferred_boundary_tags"]
        if not isinstance(tags, list):
            fail(path, f"{candidate_id}: deferred_boundary_tags must be an array")

        signal_text = json.dumps(
            [
                candidate.get("notes", []),
                candidate.get("find_signals", []),
                candidate.get("deferred_boundary_tags", []),
            ],
            ensure_ascii=False,
        ).lower()
        if "registry_stats" in candidate and not any(
            term in signal_text for term in REGISTRY_STATS_BOUNDARY_TERMS
        ):
            fail(path, f"{candidate_id}: registry_stats requires explicit safety-proof boundary language")

        if "package_registry_stats" in candidate and not any(
            term in signal_text for term in PACKAGE_STATS_BOUNDARY_TERMS
        ):
            fail(path, f"{candidate_id}: package_registry_stats requires explicit raw-signal boundary language")

        candidate_surfaces = candidate.get("candidate_surfaces", [])
        if not isinstance(candidate_surfaces, list):
            fail(path, f"{candidate_id}: candidate_surfaces must be an array when present")
        surfaces = set(candidate_surfaces)
        is_source_like = (
            candidate_type in SOURCE_LIKE_CANDIDATE_TYPES
            or candidate_role in SOURCE_LIKE_CANDIDATE_ROLES
            or bool(surfaces & SOURCE_LIKE_CANDIDATE_SURFACES)
        )
        if is_source_like and not any(term in signal_text for term in SOURCE_ROLE_BOUNDARY_TERMS):
            fail(path, f"{candidate_id}: source-like candidate requires explicit source-only/not-adoption boundary language")

        if surfaces & {"skill-installer", "skill-manager"} and not any(
            term in signal_text for term in INSTALL_BOUNDARY_TERMS
        ):
            fail(path, f"{candidate_id}: skill-installer/skill-manager surfaces require explicit no-install/install-boundary language")

        if "skill-marketplace" in surfaces and not any(
            term in signal_text for term in PUBLISH_BOUNDARY_TERMS
        ):
            fail(path, f"{candidate_id}: skill-marketplace surface requires explicit no-publish/publish-boundary language")

        adjacent_candidates = candidate.get("adjacent_candidates", [])
        if adjacent_candidates:
            if not isinstance(adjacent_candidates, list):
                fail(path, f"{candidate_id}: adjacent_candidates must be an array")
            for adj_index, adj in enumerate(adjacent_candidates):
                if not isinstance(adj, dict):
                    fail(path, f"{candidate_id}: adjacent_candidates[{adj_index}] must be an object")
                if "candidate_id" not in adj:
                    fail(path, f"{candidate_id}: adjacent_candidates[{adj_index}] missing candidate_id")
                if "relationship" not in adj:
                    fail(path, f"{candidate_id}: adjacent_candidates[{adj_index}] missing relationship")
                rel = adj.get("relationship")
                if rel not in ALLOWED_ADJACENT_RELATIONSHIPS:
                    fail(path, f"{candidate_id}: adjacent_candidates[{adj_index}] invalid relationship {rel!r}")
                ref_id = adj.get("candidate_id")
                if ref_id and ref_id not in seen_ids:
                    print(f"warning: {candidate_id} adjacent_candidates[{adj_index}] references unknown candidate_id {ref_id!r}", file=sys.stderr)

        has_claims = "claims" in candidate
        has_verified = "verified" in candidate
        if has_claims and not has_verified:
            print(f"warning: {candidate_id} has claims but no verified field", file=sys.stderr)
        if has_verified and not has_claims:
            print(f"warning: {candidate_id} has verified but no claims field", file=sys.stderr)
        verified_method = candidate.get("verified_method")
        if verified_method is not None and verified_method not in ALLOWED_VERIFIED_METHODS:
            fail(path, f"{candidate_id}: invalid verified_method {verified_method!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Candidate pool JSON files to validate")
    args = parser.parse_args()

    errors: list[str] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        try:
            validate_candidate_pool(path)
        except Exception as exc:
            errors.append(str(exc))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(args.paths)} candidate pool file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
