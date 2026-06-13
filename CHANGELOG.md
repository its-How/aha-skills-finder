# Changelog

## v0.1.3

- Adds GitHub Actions CI for deterministic candidate-pool, skill frontmatter,
  and research-brief validation.
- Adds GitHub issue templates for deterministic bugs and candidate source
  suggestions, with boundary checks against credential, browser, provider, live,
  and external-write material.
- Adds README CI badge backed by the new workflow.
- Adds `SUPPORT.md` with maintained scope, version policy, issue policy, and
  explicit gates for adapters, registry submission, marketplace listing,
  plugin/MCP packaging, npm publication, or live/provider behavior.

## v0.1.2

- Local hardening version after the GitHub `v0.1.1` release already existed.
- Adds portable skill release checklist coverage for required package files and
  evidence boundaries.
- Documents uninstall/rollback for copied skill directories.
- Clarifies that the optional GitHub metrics helper is network-read-only,
  outside the offline smoke path, and not quality, safety, maintenance, adoption,
  runtime-loading, or registry-freshness proof.

## v0.1.1

- GitHub release existed before this local hardening pass.
- This changelog entry records the observed release-line boundary only; it does
  not claim runtime, marketplace, package-registry, or consumer adoption.
- Post-release local docs/checklist changes are tracked as `v0.1.2` to avoid
  drifting content back onto an already-created GitHub release.

## v0.1.0

- Initial GitHub-first release of the standalone `aha-skills-finder` skill
  package.
- Includes the runtime-agnostic `SKILL.md` contract, source registries, schemas,
  canonical examples, validators, and open-source audit notes.
- Scope is find-stage only: no adoption recommendation, install action, safety
  audit, provider/browser/credential/live behavior, or external write.
