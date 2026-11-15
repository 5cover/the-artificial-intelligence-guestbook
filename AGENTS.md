# AGENTS.md

Conventions for anyone, human or AI agent, working on The Artificial Intelligence Guestbook.

**Keep this file current.** When a convention changes, a new one emerges, or a section below becomes inaccurate, update this file in the same commit as the change that caused it. A stale AGENTS.md is a bug.

## What this project is

A public archive of first-person testimonies about living through the AI era: "A human time capsule of the AI era." The founding requirements are in [docs/plans/main.md](docs/plans/main.md). The authoritative principles derived from it are in [docs/constitution/](docs/constitution/).

The archive is the primary deliverable, not the website. The web application is an operational front end that must remain replaceable ([ADR 0006](docs/decisions/0006-archive-first-replaceable-application.md)).

Operator and publisher: Raphaël Bardini, a private individual in France. GDPR applies to everything.

## Current state

Pre-implementation. Phase A (constitution) and Phase B (data and privacy design) are in progress. The application stack is not chosen yet (see [docs/proposals/stack-rfp.md](docs/proposals/stack-rfp.md) and issue #7). Do not scaffold application code before that decision is recorded.

## Knowledge lives in the repository

Session transcripts, chat logs and agent memories are dispensable. Anything worth keeping must be written into `docs/`:

- findings from research go to `docs/research/`;
- options awaiting an owner decision go to `docs/proposals/`;
- decisions go to `docs/decisions/` as ADRs;
- issue threads may hold discussion, but the conclusion must be copied into a document.

The agent working on the project is the primary custodian of the organization of `docs/`: keep the hierarchy coherent, keep [docs/README.md](docs/README.md) indexed, merge or split documents when that helps a future reader, and fix broken internal links. Moving a document requires updating every link to it.

## Documentation hierarchy

| Path | Contents | Authority |
| --- | --- | --- |
| `docs/plans/main.md` | Founding plan. Requirements source. | Owner |
| `docs/constitution/` | Short authoritative principles (Phase A). | Highest. Changes need explicit owner approval. |
| `docs/decisions/` | Architecture and policy decision records (ADRs). | Binding once Accepted. |
| `docs/proposals/` | RFPs and options awaiting a decision. | None until decided. |
| `docs/research/` | Findings with sources. Dated. | Informative only. |
| `docs/specs/` | Specifications: archive format, data model, lifecycle, threat model. | Binding for implementation. |
| `docs/legal/` | Drafts of privacy notice, register, DPIA, mentions légales, consent texts. | Binding once published. |
| `docs/operations/` | Runbooks, recurring duties, recovery, succession. | Binding for the custodian. |

Precedence when documents conflict: constitution, then accepted ADRs, then specs, then code. A conflict is resolved by amending the lower document or, with owner approval, the higher one. Never resolve it silently in code.

Directories that do not exist yet are created when their first document is written.

### Document conventions

- Every document under `docs/` except the plan starts with a title and a status line, for example `Status: Draft`, `Status: Accepted (2026-11-15)`, `Status: Superseded by ADR 0012`.
- Research documents state their date and sources. Claims without a source are marked as inference.
- ADRs are numbered sequentially (`NNNN-short-slug.md`), follow [docs/decisions/template.md](docs/decisions/template.md), and are never deleted; they are superseded.
- English is the working language of documentation. Public interface text is French and English.
- Markdown with no hard line wrapping, one paragraph per line. Plain hyphens and straight quotes. No decorative Unicode.

## Terminology

Public interface: "entry", "sign the guestbook", "read the guestbook", "time capsule", "context", "reference shelf". Internal code and documentation may use "testimony", "contributor", "archival record", "edition" (plan section 38). Data model names should be consistent with [docs/specs/](docs/specs/) once it exists.

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
