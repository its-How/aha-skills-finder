# Aha Skills Finder

Runtime-agnostic agent skill for finding skill and capability candidates that first-pass registry, package, or search queries would likely miss.

## What It Does

Aha Skills Finder helps an agent produce a traceable discovery artifact:

- multiple plausible skill or capability candidates
- source-surface coverage across registries, repositories, packages, tool catalogs, native runtimes, and curated lists
- query expansion and false-positive correction
- raw discovery signals such as downloads, installs, stars, metadata, claims, and source gaps
- handoff artifacts for later audit or adoption gates

It does not recommend adoption, rank winners, audit safety or source quality, install, enable, configure, publish, deploy, mutate runtime config, log in, or perform browser, provider, credential, live, or external-write actions.

## Installation

### Option 1: skills.sh

```bash
npx skills add its-how/aha-skills-finder
```

### Option 2: ClawHub

```bash
clawhub install aha-skills-finder
```

### Option 3: Manual copy

Copy the `aha-skills-finder/` directory into your agent runtime's skills path.

## Repo Contents

- `aha-skills-finder/SKILL.md` — agent-readable discovery workflow contract
- `aha-skills-finder/sources.yaml` — source-family prompt and checklist
- `aha-skills-finder/source-registries/` — seed registries for discovery sources
- `aha-skills-finder/references/` — research brief and candidate pool contracts

## License

MIT-0.
