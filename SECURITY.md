# Security

Report security issues through GitHub Security Advisories when available, or by
opening a minimal public issue that avoids secrets and private account details.

Do not include credentials, tokens, cookies, browser profiles, session material,
private supplier/customer data, or provider account data in reports.

## Security Scope

`aha-skills-finder` is a find-stage skill package. It should not:

- install, enable, configure, publish, deploy, or mutate runtime config;
- log in, handle credentials, read sessions, solve captcha, or access paid APIs;
- perform browser/provider/live/external-write actions;
- claim that candidate discovery proves safety, quality, maintenance, or
  adoption readiness.

Validators in this repository check local structure and scope hygiene only.
They do not prove that any discovered candidate is safe to install or adopt.
