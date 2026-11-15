# AGENTS.md

Conventions for anyone, human or AI agent, working on The Artificial Intelligence Guestbook.

**Keep this file current.** When a convention changes, a new one emerges, or a section below becomes inaccurate, update this file in the same commit as the change that caused it. A stale AGENTS.md is a bug.

## What this project is

A public archive of first-person testimonies about living through the AI era: "A human time capsule of the AI era." The founding requirements are in [docs/plans/main.md](docs/plans/main.md). The authoritative principles derived from it are in [docs/constitution/](docs/constitution/).

The archive is the primary deliverable, not the website. The web application is an operational front end that must remain replaceable ([ADR 0006](docs/decisions/0006-archive-first-replaceable-application.md)).

Operator and publisher: Raphaël Bardini, a private individual in France. GDPR applies to everything.

## Current state

Pre-implementation. Phase A (constitution) and Phase B (data and privacy design) are in progress.

- Stack: Django 5.2 LTS on PostgreSQL 18 ([ADR 0010](docs/decisions/0010-stack-django-postgresql.md)). The archive specification (#13) comes before the application scaffold (#21), as the RFP recommends.
- Domain: `theaiguestbook.org`, registered at OVHcloud on 2026-11-15 ([ADR 0008](docs/decisions/0008-canonical-domain.md), [docs/operations/domain.md](docs/operations/domain.md)).

## Knowledge lives in the repository

Session transcripts, chat logs and agent memories are dispensable. Anything worth keeping must be written into `docs/`:

- findings from research go to `docs/research/`;
- options for an owner decision go to `docs/proposals/`, and stay there once decided;
- decisions go to `docs/decisions/` as ADRs;
- issue threads may hold discussion, but the conclusion must be copied into a document.

The agent working on the project is the primary custodian of the organization of `docs/`: keep the hierarchy coherent, keep [docs/README.md](docs/README.md) indexed, merge or split documents when that helps a future reader, and fix broken internal links. Moving a document requires updating every link to it.

## Documentation hierarchy

| Path | Contents | Authority |
| --- | --- | --- |
| `docs/plans/main.md` | Founding plan. Requirements source. | Owner |
| `docs/constitution/` | Short authoritative principles (Phase A). | Highest. Changes need explicit owner approval. |
| `docs/decisions/` | Architecture and policy decision records (ADRs). | Binding once Accepted. |
| `docs/proposals/` | RFPs and options, awaiting or reached. Decided proposals stay as the record of the reasoning. | None; the concluding ADR is binding. |
| `docs/research/` | Findings with sources. Dated. | Informative only. |
| `docs/specs/` | Specifications: archive format, data model, lifecycle, threat model. | Binding for implementation. |
| `docs/legal/` | Drafts of privacy notice, register, DPIA, mentions légales, consent texts. | Binding once published. |
| `docs/operations/` | What exists and when it must be done: inventory of services, recurring duties calendar, incident runbooks, recovery, succession. | Binding for the custodian. |
| `docs/procedures/` | Repeatable step-by-step guides: how to do one-time setups that may need redoing and occasional tasks. Each states when its external facts were last checked. | Binding when run. |

Precedence when documents conflict: constitution, then accepted ADRs, then specs, then code. A conflict is resolved by amending the lower document or, with owner approval, the higher one. Never resolve it silently in code.

Directories that do not exist yet are created when their first document is written.

### Document conventions

- Every document under `docs/` except the plan starts with a title and a status line, for example `Status: Draft`, `Status: Accepted (2026-11-15)`, `Status: Superseded by ADR 0012`.
- Research documents state their date and sources. Claims without a source are marked as inference.
- ADRs are numbered sequentially (`NNNN-short-slug.md`), follow [docs/decisions/template.md](docs/decisions/template.md), and are never deleted; they are superseded.
- English is the working language of documentation. Public interface text is French and English.
- Markdown with no hard line wrapping, one paragraph per line. Plain hyphens and straight quotes. No decorative Unicode.

## Terminology

The individual contribution is a **testimony** (plural "testimonies"; French "témoignage") everywhere: interface, code, URLs, identifiers and documentation ([ADR 0011](docs/decisions/0011-testimony-in-the-interface.md)). "Voices" and "entry" were earlier wordings and must not reappear. Other terms: "contributor", "archival record", "edition" (public: "time capsule"), "context", "reference shelf".

Public interface copy stays plain: "sign the guestbook", "leave a testimony", "read the guestbook", "time capsule". Methodology terms such as "corpus", "archival record" or "Zeitzeugnis" belong in methodology pages and internal documentation.

Decided proposals stay in `docs/proposals/` as the record of how a decision was reached, with a status line pointing to the ADR that concluded them.

Dated research documents in `docs/research/` keep the wording of their date and are not rewritten for terminology. Data model names should be consistent with [docs/specs/](docs/specs/).

## Tracking

- GitHub Project (public): https://github.com/users/5cover/projects/23
- Issues live in this repository. Milestones map to plan phases A to G. Labels: `decision`, `research`, `legal`, `ops`, `area:*`, plus the GitHub defaults.
- Status workflow: `Idea` (captured), `Ready` (specified enough to start), `In Progress`, `Pending` (blocked on a decision, an external party or another item), `Nope` (deliberately not doing, reason on the item), `Done`.
- When starting work on an issue, set it to `In Progress`. When a document or commit completes it, close the issue and set `Done`. New work discovered along the way becomes a new issue rather than an unrecorded intention.
- The `gh` CLI is used for project operations. Project node ID: `PVT_kwHOAmiDks4Brvf4`. Status field ID: `PVTSSF_lAHOAmiDks4Brvf4zhqAwAU`.

## Commits

- Conventional Commits (`docs:`, `feat:`, `fix:`, `chore:`...) with descriptive bodies. Reference issues (`Refs #2`, `Closes #2`).
- Commit on the current branch. No branching workflow has been defined yet; ask the owner before creating one.
- Plan files in the repository are committed alongside the work they describe.
- Never commit secrets. `.env` is ignored and must stay ignored.

## Product guardrails

Before adding a feature, apply the test in plan section 37: does it make it easier to preserve, understand, discover or responsibly maintain human testimony? The scarce resource is custodial attention. No comments, likes, follows, messaging, feeds, rankings or profiles (plan sections 15, 34).
