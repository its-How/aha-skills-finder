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
- root docs: `README.md`, `INSTALL.md`, `USAGE.md`, `SECURITY.md`,
  `CONTRIBUTING.md`, `CHANGELOG.md`, `OPEN_SOURCE_AUDIT.md`,
  `RELEASE_CHECKLIST.md`, `SUPPORT.md`
- root license: `LICENSE`
- `package.json`

## Boundary Checks

- Runtime adapter files are not included. Add them only after a named runtime
  schema and validator exist.
- `aha-skills-finder/scripts/collect-github-metrics.py` is an optional
  network-read-only helper. It is outside the offline smoke path and does not
  prove quality, safety, maintenance, adoption, runtime loading, or registry
  freshness.
- Local validators prove structure only, not runtime loading, source quality,
  candidate safety, registry freshness, or adoption fit.
- Schema compatibility validation proves bundled examples match the shipped
  JSON schemas. It does not prove real discovery quality or candidate fit.
- `npm pack --dry-run` proves package contents only. It does not prove npm
  registry publication, marketplace acceptance, runtime loading, source quality,
  candidate safety, or adoption fit.
- The npm shape has no `bin`, `main`, or `exports`; do not describe it as a CLI
  or JavaScript import API.

## Channel Gates

- Package inventory assertion: verify `npm pack --dry-run` includes the skill
  directory, root governance docs, `LICENSE`, and `package.json`, and no `bin`,
  `main`, or `exports` claim.
- Local release check: run `npm run release:check`. The `prepublishOnly` guard
  also runs `npm test` before `npm publish`, but it is not a substitute for
  exact publish approval and registry receipt capture.
- Fresh npm install smoke: from a temporary directory, install the published
  package from the intended registry and verify
  `node_modules/aha-skills-finder/aha-skills-finder/SKILL.md` exists. Record a
  receipt before claiming npm distribution works.
- GitHub release: tag, push, and release creation are external writes and require
  exact approval plus a release URL receipt.
- npm publish: requires exact approval, account/2FA handling only by the user or
  explicitly authorized token flow, and an npm registry receipt. It does not
  prove runtime loading, registry acceptance, or adoption.
- Marketplace or skill-registry submission: before submitting, record the target
  schema, account/auth requirement, write action, safety boundary, and overclaim
  boundary. Submission does not prove acceptance.
- Public announcement: requires exact channel/content approval and a URL or
  screenshot receipt. Announcement does not prove adoption.
