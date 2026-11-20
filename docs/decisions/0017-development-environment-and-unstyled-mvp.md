# 0017. Development environment, and an unstyled MVP with minimal JavaScript

Status: Accepted (2026-11-20)

Issue: #21

## Context

The specifications are accepted, and a first local MVP can be built (ADR 0010: Django 5.2 LTS on PostgreSQL 18). The scaffold needs fixed tool choices so that implementation does not reopen them. No visual design has been chosen. The owner proposed starting with no CSS at all, which forces an interface that works without it, and allowing JavaScript only where necessary, since the application is server-rendered.

Versions below were read from PyPI on 2026-11-20. The custodian's machine has Python 3.12.4, and neither PostgreSQL nor Docker installed.

## Decision

1. **Python and dependencies:** Python 3.12 or later. Dependencies and the virtual environment are managed with uv (0.13.9), with `pyproject.toml` and a committed `uv.lock`.
2. **Libraries:** Django `~=5.2` (5.2.19 at the time of writing), psycopg 3 (3.3.9), markdown-it-py (4.3.0), nh3 (0.3.8), jsonschema (4.26.0), bagit (1.9.0). Others only when a specification requires them.
3. **Quality tools:** pytest (9.2.0) with pytest-django (4.14.0), and Ruff (0.17.6) for linting and formatting. Every constraint in the data model has a test (data model, section 1.4).
4. **Database:** PostgreSQL 18 installed natively on the development machine. Tests run against PostgreSQL, never SQLite, because the constraints, search and time semantics depend on it.
5. **Configuration:** settings read from environment variables, with a `.env` file for local development that stays ignored. Email uses Django's console backend locally.
6. **Layout:** the Django project lives in `app/`, with `manage.py` and a `guestbook` package containing the settings and one Django app per domain area (accounts, testimonies, moderation, reports, publication, exports). The archive schemas stay in `archive/schema/` and are read from there.
7. **No CSS in the MVP.** Pages send no stylesheet and no `style` attribute, and the Content-Security-Policy forbids them (`style-src 'none'`). The baseline mechanisms are HTML:
   - folded timelines and citation tabs use `<details>`;
   - the editor's "Write" and "Preview" are a form submission that renders the preview server-side;
   - review diffs mark changed words with `<ins>` and `<del>`, which browsers distinguish by default.
8. **JavaScript only where a feature needs it** (owner decision, 2026-11-20). The architecture is server-rendered, so JavaScript is an enhancement, never a requirement:
   - every page and form works with JavaScript disabled, and tests cover that path;
   - scripts are first-party static files served by the site: no third-party scripts, no inline scripts or event handlers (`script-src 'self'`);
   - no framework and no build step for the MVP: plain ES modules;
   - no tracking or analytics, and no personal data stored in the browser.

   Uses allowed in the MVP: the proof-of-work of ADR 0003 on sign-in, submission and reports, with a stricter rate limit as the fallback when JavaScript is off; converting displayed instants to the browser's time zone, with UTC in a tooltip (data model, section 1.3, rule 6), with UTC shown as is when JavaScript is off; copy-to-clipboard in the citation component; and a live preview in the editor, with the server-side preview as the fallback. Any other use, a framework or a build step needs a new decision.

## Consequences

- Every page must make sense in the browser's default rendering, which is also the baseline for accessibility (#35) and for the static HTML of editions.
- A visual design later adds a stylesheet without changing the HTML structure, if the HTML is semantic.
- The custodian installs PostgreSQL 18 and uv before running the project.
- Revisit item 7 when a visual design is chosen, and item 8 if a feature needs more JavaScript than it allows.
