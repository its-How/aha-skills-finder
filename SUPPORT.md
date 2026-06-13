# Support

`aha-skills-finder` is maintained as a portable, runtime-agnostic skill
directory for find-stage discovery artifacts.

## Supported Scope

Maintained:

- `aha-skills-finder/SKILL.md` trigger and workflow contract;
- source-family registry hygiene;
- research brief and candidate pool schema compatibility;
- canonical examples;
- deterministic validators;
- documentation that preserves the find-stage boundary.

Not supported by this package:

- adoption recommendations or final ranking;
- source, safety, permission, maintenance, provider, browser, credential, login,
  live, or external-write audit;
- install managers, plugin packaging, MCP servers, marketplace submission,
  runtime config mutation, or provider configuration;
- npm package usage as a CLI or JavaScript import API;
- guarantees that a discovered candidate is safe, current, high quality, or fit
  for adoption.

## Version Policy

- Patch releases may fix validators, examples, docs, source registries, or
  boundary wording without changing the find-stage contract.
- Minor releases may add schema fields, source families, examples, or adapter
  metadata after validation.
- Major releases are reserved for incompatible artifact contract changes.

## Issue Policy

Use GitHub issues for deterministic package defects, unclear documentation, or
candidate-source improvements.

Do not include credentials, tokens, cookies, browser profiles, session material,
private account data, private customer/supplier data, or live/provider
materials in issues.

Requests for runtime adapters, registry submission, marketplace listing,
plugin/MCP packaging, new npm publication, or live/provider behavior need a
separate design and approval gate before implementation.
