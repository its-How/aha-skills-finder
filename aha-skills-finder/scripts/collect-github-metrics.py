#!/usr/bin/env python3
"""Collect lightweight raw GitHub repo metrics.

This script exposes find-stage signals only. It does not score quality, safety,
maintenance, or adoption readiness.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request


def fetch_repo(slug: str) -> dict:
    url = f"https://api.github.com/repos/{slug}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "aha-skills-finder-metrics-v0",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize(repo: dict) -> dict:
    return {
        "repo": repo.get("full_name"),
        "html_url": repo.get("html_url"),
        "stars": repo.get("stargazers_count"),
        "forks": repo.get("forks_count"),
        "open_issues": repo.get("open_issues_count"),
        "created_at": repo.get("created_at"),
        "updated_at": repo.get("updated_at"),
        "pushed_at": repo.get("pushed_at"),
        "archived": repo.get("archived"),
        "disabled": repo.get("disabled"),
        "license": (repo.get("license") or {}).get("spdx_id"),
        "cannot_prove": [
            "These metrics do not prove skill quality.",
            "These metrics do not prove safety or adoption readiness.",
            "These metrics do not prove consumer outcome improvement."
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repos", nargs="+", help="GitHub repo slugs, for example owner/repo")
    args = parser.parse_args()

    output = []
    errors = []
    for slug in args.repos:
        try:
            output.append(normalize(fetch_repo(slug)))
        except urllib.error.HTTPError as exc:
            errors.append({"repo": slug, "error": f"HTTP {exc.code}"})
        except Exception as exc:
            errors.append({"repo": slug, "error": str(exc)})

    print(json.dumps({"metrics": output, "errors": errors}, indent=2, ensure_ascii=False))
    return 1 if errors and not output else 0


if __name__ == "__main__":
    raise SystemExit(main())
