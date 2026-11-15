# 0010. Application stack: Django 5.2 LTS on PostgreSQL 18

Status: Accepted (2026-11-15)

Issue: #7

## Context

The [stack RFP](../proposals/stack-rfp.md) applied pass/fail gates, then 15 weighted criteria derived from the plan and the ADRs, to thirteen candidates and a reference anti-stack. Its criteria were revised after owner review: churn was redefined as the cost of staying supported, a type-system criterion was added, and security was raised.

Django scored highest under both the original and the revised criteria (88.6 and 86.4), well ahead of Symfony (77.4). Its lead comes from the first-party admin for one-person moderation, gettext-based i18n, PostgreSQL full-text search with French and English configurations, foundation governance and a published security policy.

The owner values TypeScript for modelling complex data. Minimal TypeScript (68.8) and the other TypeScript options were considered as a possible axis and not adopted.

Owner answers to the RFP's closing questions (2026-11-15):

- no non-compensatory security floor (question 13);
- the revised criteria and weights are accepted (question 14);
- minimal TypeScript was a possible axis only (question 15).

## Decision

1. The application framework is **Django**, on its **5.2 LTS** series, tracking the latest 5.2 patch release. Per the RFP sources, 5.2 is supported until April 2028, and the next LTS, 6.2, is planned for April 2027.
2. The database is **PostgreSQL 18**.
3. The architecture follows section 8 of the RFP: reverse proxy, the Django application, PostgreSQL, systemd timers for jobs, encrypted off-site backups, and an archive exporter that reads through the domain layer and writes the canonical format, which is specified independently of the application ([ADR 0006](0006-archive-first-replaceable-application.md)).
4. The archive specification (#13) is written before the application is scaffolded (#21).
5. The RFP is concluded and kept in `docs/proposals/` as the record of how this decision was reached.

## Consequences

- The application language is Python. The supported Python version for Django 5.2 is chosen and verified at scaffold time, not assumed here.
- The typing gap measured by criterion 15 is narrowed deliberately: strict static type checking with Django type stubs, and types generated from the archive JSON Schema where the domain model meets the export.
- Upgrade calendar: Django 5.2 support ends in April 2028. The move to the next LTS must be planned well before then, and goes on the operations calendar (#33).
- Implementation choices left open by the RFP (its questions 4 to 11), to be decided during scaffolding and authentication work (#21, #22):
  - job runner: systemd timers and management commands only, or a database-backed task package;
  - magic-link library, with a maintenance threshold, or a thin in-project flow on Django's signing tools;
  - admin: Django's admin on a restricted path, with a phishing-resistant second factor;
  - context pages: Markdown in the repository (the default) or a CMS such as Wagtail;
  - reverse proxy: Caddy or nginx;
  - proof-of-work verifier: ALTCHA's server component or a custom verifier, with its licence checked;
  - search for languages without a PostgreSQL stemmer: the "simple" configuration.
- Revisit if Django's governance or security policy changes materially, or if the archive specification reveals a requirement the stack serves poorly.
