# The Artificial Intelligence Guestbook

A human time capsule of the AI era. The archive is the primary deliverable; the web application is a replaceable front end ([ADR 0006](docs/decisions/0006-archive-first-replaceable-application.md)). Start with the [documentation index](docs/README.md).

## Running it locally

You need Python 3.12 or later, [uv](https://docs.astral.sh/uv/) and PostgreSQL 18. How this was installed without administrator rights is recorded in [local development](docs/operations/local-development.md).

Set the database password and a secret key in the environment. Variables may also be kept in a `.env` file, which is ignored by Git, and loaded with `uv run --env-file .env`.

```text
GUESTBOOK_DB_PASSWORD      password of the PostgreSQL user (required)
GUESTBOOK_DB_USER          default guestbook_admin
GUESTBOOK_DB_NAME          default guestbook
GUESTBOOK_DB_HOST          default 127.0.0.1
GUESTBOOK_DB_PORT          default 5432
GUESTBOOK_SECRET_KEY       required unless GUESTBOOK_DEBUG=1
GUESTBOOK_DEBUG            1 for local development only
GUESTBOOK_MODERATOR_EMAILS comma-separated addresses that see the moderation queue
GUESTBOOK_PUBLIC_BASE_URL  base of the links in emails and citations, default https://theaiguestbook.org; use http://127.0.0.1:8000 locally
GUESTBOOK_ALLOWED_HOSTS    default localhost,127.0.0.1
GUESTBOOK_FROM_EMAIL       default contact@theaiguestbook.org
GUESTBOOK_EMAIL_BACKEND    default console
GUESTBOOK_ERASE_ON_RESTORE_FILE  file listing withdrawn testimony IDs, kept outside database backups (empty by default)
```

Then, from the repository root:

```text
uv run python app/manage.py migrate
uv run python app/manage.py runserver
```

Outgoing email is printed to the console unless `GUESTBOOK_EMAIL_BACKEND` names another backend.

## Operations commands

These run by hand for now. Scheduling them belongs to the deployment work.

```text
uv run python app/manage.py purge_expired
uv run python app/manage.py erase_on_restore
uv run python app/manage.py export_edition 2027.0 <directory>
```

- `purge_expired` deletes sign-in links and rate-limit counters older than 24 hours (retention schedule, rows 1 and 19).
- `erase_on_restore` runs the deletion again for every testimony on the erase-on-restore list (deletion lifecycle, section 6).
- `export_edition` writes an unsigned edition bag inside `<directory>`. It refuses to run before the cutoff of its period, and while a testimony of the period has a pending revision. Signing and compression happen on the custodian's machine (archive format, section 9).

## Tests and linting

```text
pnpm test          # uv run pytest, against PostgreSQL
pnpm lint:py       # ruff check and ruff format --check
pnpm fix:py        # ruff fixes and formatting
pnpm lint:md       # markdownlint
pnpm lint:json     # prettier --check on JSON
```

## Licences

- Application code, templates and CSS: MIT ([LICENSE](LICENSE)).
- Documentation in `docs/`, including the plan, the constitution, context documents and reference records: CC BY 4.0 ([LICENSE-docs](LICENSE-docs)).
- Testimonies, project translations of testimonies, and each edition as a compilation (including the database right): CC BY 4.0 ([ADR 0009](docs/decisions/0009-testimony-licensing.md), [ADR 0016](docs/decisions/0016-project-licensing.md)).
- The name "The Artificial Intelligence Guestbook" and any logo or illustration are not licensed for use as identifiers of another project.
