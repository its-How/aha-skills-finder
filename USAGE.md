# Usage

Use `aha-skills-finder` when an agent needs a find-stage candidate pool for
skills, MCPs, CLIs, plugins, registries, extensions, SaaS/provider routes, repo
tools, or native runtime capabilities.

The output is a traceable discovery artifact, not an adoption recommendation.

## Offline First Run

From the repository root:

```bash
python3 aha-skills-finder/scripts/validate-candidate-pool.py \
  aha-skills-finder/examples/find-skill-finder/candidate-pool.json \
  aha-skills-finder/examples/find-skill-audit/candidate-pool.json
python3 aha-skills-finder/scripts/validate-skill.py aha-skills-finder
python3 -m json.tool aha-skills-finder/examples/find-skill-finder/research-brief.json >/dev/null
python3 -m json.tool aha-skills-finder/examples/find-skill-audit/research-brief.json >/dev/null
```

Expected result:

- both candidate-pool examples validate;
- `SKILL.md` frontmatter validates;
- bundled research briefs are valid JSON.

This proves local structure only. It does not prove discovery quality, candidate
safety, source quality, adoption fit, registry freshness, or runtime adapter
support.

## Minimal Agent Prompt

After installing the skill directory into a runtime that can load `SKILL.md`
skills, use a prompt like:

```text
Use aha-skills-finder to find skill or capability candidates for:
<target outcome>

Stay in find-stage only. Produce a research brief and candidate pool. Do not
recommend adoption, install anything, audit safety, log in, use credentials,
mutate runtime config, or perform live/external-write actions.
```

## Expected Artifacts

The skill is designed to produce:

- a research brief shaped by `aha-skills-finder/schemas/research-brief.schema.json`;
- a candidate pool shaped by `aha-skills-finder/schemas/candidate-pool.schema.json`;
- explicit source gaps, false-positive corrections, and raw signals.

## Optional GitHub Metrics Script

`aha-skills-finder/scripts/collect-github-metrics.py` can collect raw GitHub repo
signals when network access is available. It is not part of the offline smoke
path and does not prove quality, safety, maintenance, or adoption readiness.
