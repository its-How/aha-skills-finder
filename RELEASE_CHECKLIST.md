# Release Checklist

Use this checklist before distributing a portable `aha-skills-finder` skill
package.

## Portable Skill Inventory

The package must include:

- `aha-skills-finder/SKILL.md`
- `aha-skills-finder/sources.yaml`
- `aha-skills-finder/source-registries/`
- `aha-skills-finder/schemas/`
- `aha-skills-finder/scripts/`
- `aha-skills-finder/examples/`
- `aha-skills-finder/adapters/README.md` as adapter policy only
- root docs: `README.md`, `INSTALL.md`, `USAGE.md`, `SECURITY.md`,
  `CONTRIBUTING.md`, `CHANGELOG.md`, `OPEN_SOURCE_AUDIT.md`,
  `RELEASE_CHECKLIST.md`
- root license: `LICENSE`

## Boundary Checks

- Adapter files are policy or metadata only unless a named runtime validator is
  added.
- `aha-skills-finder/scripts/collect-github-metrics.py` is an optional
  network-read-only helper. It is outside the offline smoke path and does not
  prove quality, safety, maintenance, adoption, runtime loading, or registry
  freshness.
- Local validators prove structure only, not runtime loading, source quality,
  candidate safety, registry freshness, or adoption fit.
