# Plan: local MVP implementation

Status: Ready (2026-11-20). Instructions for the implementing agent.

You are implementing the first local MVP of The Artificial Intelligence Guestbook. The design work is done: the specifications are accepted and binding. Your job is to implement them faithfully, not to redesign them. Do not search the web. Every version and tool you need is given below or in the documents.

## 1. Read first

Read these in order, completely:

1. [AGENTS.md](../../AGENTS.md): conventions, commits, Markdown and JSON rules, product guardrails.
2. [ADR 0017](../decisions/0017-development-environment-and-unstyled-mvp.md): tools, layout, no CSS, and JavaScript only where necessary.
3. [Data model](../specs/data-model.md): objects, types, constraints, revisions and review, states. This is the core of the work.
4. [Identifiers](../specs/identifiers.md): URLs, HTTP semantics, data URLs, citation.
5. [Deletion lifecycle](../specs/deletion-lifecycle.md) and [retention schedule](../specs/retention.md).
6. [Reports](../specs/reports.md) and [browsing and filters](../specs/browsing-and-filters.md).
7. [Archive format](../specs/archive-format.md) and the schemas in `archive/schema/`.
8. [Threat model](../specs/threat-model.md), and ADRs [0003](../decisions/0003-email-magic-link-auth.md), [0006](../decisions/0006-archive-first-replaceable-application.md), [0010](../decisions/0010-stack-django-postgresql.md), [0011](../decisions/0011-testimony-in-the-interface.md), [0013](../decisions/0013-legal-bases-and-minors.md).

Then read the rest of `docs/` broadly (constitution, legal drafts, operations) for context. Precedence when documents conflict is in AGENTS.md: constitution, accepted ADRs, specs, code.

## 2. Scope

Build the following, in this order. Each step ends with passing tests and one or more commits.

1. **Scaffold** (#21): `pyproject.toml`, `uv.lock`, the `app/` layout of ADR 0017, settings from environment variables, PostgreSQL connection, Ruff and pytest configured, a `README` section on running it locally. Add a test that fails if any model field lacks a classification or a conceptual type (data model, section 1.1, rule 2), and keep it passing for every later step.
2. **Accounts and sign-in** (#22): accounts, magic-link tokens (hashed, 15 minutes, single use), sessions, the disposable-domain blocklist loaded from a committed file (start with a small file and a loader; do not download a list), MX check, rate limits with keyed, rotating IP hashes. Proof-of-work as a JavaScript enhancement, with its no-JavaScript fallback (ADR 0017, item 8).
3. **Contribution** (#23): one testimony per account, drafts, submission with the consent record and the single publication statement (ADR 0013, D6), the age gate with one threshold of 16 and the parental path by email (D5), public identity, authorship disclosure, structured fields, named enumerations with their `_note` fields, CommonMark rendering with every rule of data model section 2.3.1.
4. **Revisions and review** (#24): revisions with `pending`, `approved` and `returned`; `public_revision` and `archived_revision`; live edits on published testimonies; the under-16 hold; returning with both options and quarantine reasons; the review screen with the pending timeline and word-level diffs using `<ins>` and `<del>`; the prioritized queue for testimonies of a closing edition period; moderation records and statement-of-reasons emails; body deletion per section 2.5, rule 7.
5. **Public reading** (#25, #27): the testimony page and its HTTP semantics (200, 404, 410 tombstone); the folded public timeline; the citation component with plain text, BibTeX and Hayagriva; the chronological listing by day; full-text search; filters per browsing section 3; the "name given by the contributor" note.
6. **Withdrawal and closure** (#16 spec): withdrawal requests of every scope, verification, the deletion job steps that exist locally, the withdrawal list, account closure with the neutral choice and the withdrawal code, and the erase-on-restore list.
7. **Reports** (#41): the report form and reasons, email confirmation, rate limits, merging, priorities, the capped automatic hiding, decisions and notifications.
8. **Data URLs** (#39): every endpoint of identifiers section 2.1, validated in tests against the JSON Schemas, the Markdown views, `/llms.txt` and `/robots.txt`.
9. **Export** (#38, partial): a management command that writes an unsigned edition bag per archive format sections 1 to 5 and 7 to 9 (records, plain text, `all-testimonies.txt`, indexes, withdrawal list, static HTML, manifests, `provenance.json`), refusing to run while a testimony of the period has a pending revision.

Out of scope: deployment and the VPS, a real email provider, any CSS, JavaScript beyond the uses listed in ADR 0017 item 8, French translation of the interface (wrap strings for translation, write English only), translations of testimonies (#29), context pages and reference shelf content (an empty placeholder page each is enough), final legal texts (placeholder pages marked as drafts), signing, compression, PDF/A and the independent reader of editions, monitoring, backups.

## 3. Rules while working

1. Follow AGENTS.md. Conventional Commits with descriptive bodies, referencing issues. Commit on the current branch. Never push. Amend unpushed commits for small fixes.
2. Implement constraints at the level the data model assigns them (section 1.4), each with a test that attempts the invalid state.
3. Only `public` fields reach pages, exports and data URLs, through one allow-list.
4. Do not change any document under `docs/constitution/`, `docs/decisions/` or `docs/specs/`. If code cannot follow a document, stop (section 4). You may update the README, add `docs/operations/` notes on running the project, and keep AGENTS.md current for new conventions such as test commands.
5. Before each commit: `uv run ruff check`, `uv run ruff format --check`, `uv run pytest`, and `pnpm lint:md` and `pnpm lint:json` when Markdown or JSON changed.
6. Prefer the simplest code that satisfies the spec. No features beyond the scope above.
7. Every feature works with JavaScript disabled, and the tests cover that path.

## 4. When to stop

Stop and report, without guessing, if:

1. you are stuck: the same failure persists after a reasonable attempt, or a tool or dependency is missing from the machine (PostgreSQL 18 and uv must be installed by the owner);
2. a document is ambiguous, or two documents contradict each other, and resolving it would be a product, privacy, legal or moderation decision rather than an implementation detail;
3. following the documents is impossible, or would require you to change a constitution, ADR or spec document, or to act beyond the scope of section 2.

An implementation detail that no document addresses, and that does not affect what a contributor, reader or moderator experiences, is yours to decide: note it in the report.

## 5. Report when done or stopped

Reply with:

1. the steps of section 2 completed, partly completed or not started;
2. the commits made, by hash and subject;
3. how to run the project and the tests locally, as exact commands;
4. the test and lint results;
5. every implementation detail you decided yourself;
6. if you stopped: the reason, with the exact documents and sections involved, and the decision needed from the owner, stated as a question with the options you see.
