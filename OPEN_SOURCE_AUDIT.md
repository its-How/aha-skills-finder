# Open Source Audit

Status: npm-ready local audit.

## Scope

Audited package path:

```text
aha-skills-finder/
```

Target repository shape:

```text
aha-skills-finder/
  README.md
  LICENSE
  OPEN_SOURCE_AUDIT.md
  package.json
  aha-skills-finder/
    SKILL.md
    adapters/
    examples/
    schemas/
    scripts/
    source-registries/
    sources.yaml
```

## Intended Public Contract

- Runtime-agnostic agent skill package.
- Thin npm package shape for skill-file distribution and deterministic
  validation assets only.
- Find-stage only: discover multiple traceable skill/capability candidates and raw signals.
- No adoption recommendation, ranking, safety/source audit, install/enable/configure, browser/provider/credential/live action, deploy, or external write.
- No CLI, JavaScript import API, runtime adapter claim, marketplace acceptance
  claim, or candidate adoption claim.

## Required Checks

- No unrelated skill packages in this standalone repo.
- No internal workspace paths in public package files.
- No private credentials, tokens, cookies, sessions, or account identifiers.
- No claims that discovery signals prove quality, safety, maintenance, or adoption readiness.
- Candidate pool validator passes on canonical examples.
- `SKILL.md` frontmatter validates.
- npm package dry-run contains only intended public files.

## Cannot Prove

- Candidate safety or source quality.
- Adoption fit.
- Registry/package freshness after publication.
- Runtime adapter support.
- npm registry publication, GitHub release publication, marketplace acceptance,
  or external distribution success.
