# Install

`aha-skills-finder` is distributed as a portable skill directory:

```text
aha-skills-finder/
```

The core contract is `aha-skills-finder/SKILL.md`. Runtime-specific adapters are
not required for local use and are not currently claimed as validated.

## From GitHub

```bash
git clone https://github.com/its-How/aha-skills-finder.git
cd aha-skills-finder
```

## Generic Agent Runtime

If your agent runtime supports `SKILL.md` directories, copy the skill directory
into that runtime's configured skill directory:

```bash
cp -R aha-skills-finder /path/to/your/skills/
```

Then restart or reload the runtime according to that runtime's own rules.

## Uninstall / Rollback

Remove the copied `aha-skills-finder/` directory from the runtime's skill
directory, then reload or restart that runtime. This only rolls back the local
portable skill copy; it does not change provider config, credentials, browser
state, plugins, marketplaces, or external systems.

## Codex-Style Local Skill Directory

If your Codex environment uses `CODEX_HOME`, a local install shape is:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R aha-skills-finder "${CODEX_HOME:-$HOME/.codex}/skills/"
```

This copies the portable skill contract only. It does not install a plugin, add
an MCP server, mutate provider config, or prove that any candidate should be
adopted.

## Use Without Installing

You can evaluate the package without copying it into a runtime:

```bash
python3 aha-skills-finder/scripts/validate-candidate-pool.py \
  aha-skills-finder/examples/find-skill-finder/candidate-pool.json \
  aha-skills-finder/examples/find-skill-audit/candidate-pool.json
python3 aha-skills-finder/scripts/validate-skill.py aha-skills-finder
```

Then point an agent at `aha-skills-finder/SKILL.md` and the examples in
`aha-skills-finder/examples/`.

## Not Included

This package does not include npm publication, a marketplace listing, a Codex
plugin manifest, a validated runtime adapter, or any live/provider/browser/
credential action.
