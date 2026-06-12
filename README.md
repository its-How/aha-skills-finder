# Aha Skills Finder

Runtime-agnostic agent skill for finding skill and capability candidates that first-pass registry, package, or search queries would likely miss.

This repository is written for agents and automated consumers, not for tutorials, marketing, manual operation, or one specific AI runtime.

## Package

| Path | Purpose |
|---|---|
| `aha-skills-finder/SKILL.md` | Agent-readable discovery workflow contract |
| `aha-skills-finder/sources.yaml` | Source-family catalog |
| `aha-skills-finder/source-registries/` | Seed registries for discovery sources |
| `aha-skills-finder/schemas/` | Research brief and candidate pool schemas |
| `aha-skills-finder/scripts/` | Local validators and light metric collectors |
| `aha-skills-finder/examples/` | Canonical find-stage artifacts |
| `aha-skills-finder/adapters/` | Optional runtime metadata policy |

## What It Does

`aha-skills-finder` helps an agent produce an aha-shaped discovery artifact:

- multiple traceable skill/capability candidates;
- source-surface coverage across registries, repos, packages, MCP/tool catalogs, native runtimes, and curated lists;
- query expansion and false-positive correction;
- raw signals such as stars, downloads, installs, registry stats, README claims, package metadata, and source gaps;
- handoff artifacts for later audit or adoption gates.

It does not recommend adoption, rank winners, audit safety/source quality, install, enable, configure, publish, deploy, mutate runtime config, log in, or perform browser/provider/credential/live/external-write actions.

## Validation

Run from the repository root:

```bash
python3 aha-skills-finder/scripts/validate-candidate-pool.py aha-skills-finder/examples/find-skill-finder/candidate-pool.json
python3 aha-skills-finder/scripts/validate-candidate-pool.py aha-skills-finder/examples/find-skill-audit/candidate-pool.json
quick_validate.py aha-skills-finder
```

`quick_validate.py` means any equivalent SKILL.md frontmatter validator available in the consuming runtime.

## Repository Boundary

This is the standalone repository shape for `aha-skills-finder`.

Do not add unrelated skills to this repo. `bigdeal-supplier-finder` belongs in its own independent repository because it has different users, package terms, validation risk, and live/provider boundaries.

License: MIT.
