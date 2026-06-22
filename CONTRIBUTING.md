# Contributing

Keep this repository agent-first, runtime-agnostic, and find-stage only.

Before opening a change, run:

```bash
python3 aha-skills-finder/scripts/validate-candidate-pool.py \
  aha-skills-finder/examples/find-skill-finder/candidate-pool.json \
  aha-skills-finder/examples/find-skill-audit/candidate-pool.json
python3 aha-skills-finder/scripts/validate-skill.py aha-skills-finder
python3 -m json.tool aha-skills-finder/examples/find-skill-finder/research-brief.json >/dev/null
python3 -m json.tool aha-skills-finder/examples/find-skill-audit/research-brief.json >/dev/null
```

Do not add:

- adoption recommendations, final rankings, safety verdicts, source-quality
  verdicts, or install decisions;
- credential, cookie, token, browser profile, provider, paid API, or session
  handling;
- login, captcha, live action, runtime mutation, publish, deploy, or external
  write behavior;
- placeholder runtime adapters or marketplace/plugin metadata that has not been
  validated in that runtime;
- claims that raw metrics, stars, downloads, or validators prove quality,
  safety, maintenance, or adoption readiness.

Changes to schemas or examples should preserve the evidence distinction between
raw discovery signals and later audit/adoption gates.
