# Runtime Adapters

This directory is for optional runtime metadata only.

The core contract is runtime-agnostic and lives in:

- `../SKILL.md`
- `../schemas/`
- `../sources.yaml`
- `../examples/find-skill-finder/`
- `../examples/find-skill-audit/`

Do not add adapter files as placeholders.

Add a runtime adapter only when all of these are true:

- the runtime has a concrete metadata schema or documented convention;
- the adapter can be validated in that runtime or in a clean-room fixture;
- the adapter does not change the find-stage-only boundary;
- the adapter does not imply install, enable, ranking, audit, or adopt/use success;
- the adapter states what it cannot prove.

Adapters are never authority. They only map the core contract into a runtime.
