# Open Source Audit

Status: split-ready local audit.

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
- Find-stage only: discover multiple traceable skill/capability candidates and raw signals.
- No adoption recommendation, ranking, safety/source audit, install/enable/configure, browser/provider/credential/live action, publish, deploy, or external write.

## Required Checks

- No unrelated skill packages in this standalone repo.
- No internal workspace paths in public package files.
- No private credentials, tokens, cookies, sessions, or account identifiers.
- No claims that discovery signals prove quality, safety, maintenance, or adoption readiness.
- Candidate pool validator passes on canonical examples.
- `SKILL.md` frontmatter validates.

## Cannot Prove

- Candidate safety or source quality.
- Adoption fit.
- Registry/package freshness after publication.
- Runtime adapter support.
- GitHub repository creation, transfer, push, package publish, or external release success.
