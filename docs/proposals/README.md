# Proposals and decision queue

Status: Living index (2026-11-15)

Proposals present options for an owner decision. Once decided, a proposal stays here as the record of the reasoning, and an ADR in [docs/decisions/](../decisions/) records the outcome ([AGENTS.md](../../AGENTS.md)).

## Proposals

| Proposal | Issues | State |
| --- | --- | --- |
| [Stack RFP](stack-rfp.md) | #6, #7 | Concluded: [ADR 0010](../decisions/0010-stack-django-postgresql.md) |
| [Legal bases, retention duty and minors](legal-bases-and-minors.md) | #12, #17, #18 | Concluded: [ADR 0013](../decisions/0013-legal-bases-and-minors.md) |
| [Licences for the project's own material and for editions](project-licensing.md) | #43 | Concluded: [ADR 0016](../decisions/0016-project-licensing.md) |
| [Infrastructure](infrastructure.md) | #9, #10, #31 | Concluded: [ADR 0014](../decisions/0014-provisional-vps-ovhcloud.md), [ADR 0015](../decisions/0015-backups-and-transactional-email.md) |
| [Context pages](context-pages.md) | #36 | Awaiting review: editorial rules and first set |
| [Reference shelf](reference-shelf.md) | #37 | Awaiting review: record format, selection criteria, 22 verified records |

## Decision queue

Decisions waiting for the owner, grouped by the work they unblock. The recommendation, where there is one, is in the linked section. Decisions that block nothing before launch are listed separately at the end, so that they are neither forgotten nor mistaken for blockers.

### Context (#36)

1. Editorial rules, first set of pages and who writes them ([context pages](context-pages.md)).

### Reference shelf (#37)

1. The record format, including the five added fields and naming against plan section 18 ([reference shelf](reference-shelf.md), section 7).
2. Whether all-rights-reserved resources are listed as metadata only, and whether sources run by individuals are allowed ([reference shelf](reference-shelf.md), section 7).

### Contribution form (#23, #27)

1. The `Field` enumeration has only "other". The data model defers its values to #27, and no document lists them, so the form offers no field choice. Options: the owner supplies the list; or a provisional list is drafted for approval. Blocks the contribution form before launch ([ADR 0018](../decisions/0018-implementation-choices-of-the-mvp.md), "Contribution and consent").
2. Under 16, organization type is refused as well as the four fields the data model lists. Options: keep organization type refused (current, since it also reveals a sector of employment); or follow the data model exactly ([ADR 0018](../decisions/0018-implementation-choices-of-the-mvp.md), "Contribution and consent").

### Withdrawal and closure (#16, #33)

1. The tombstone rule conflicts with constraint 5. Constraint 5 of [data model](../specs/data-model.md), section 2.3, requires language, received date and edition period on every non-draft testimony. Section 2.13 says a tombstone keeps only the public ID and the withdrawal. Options: amend constraint 5 so that withdrawn rows may clear these three columns (recommended: none of them is shown on a tombstone, and the received date is private); or keep them on withdrawn rows, as built, and say so in section 2.13 ([ADR 0018](../decisions/0018-implementation-choices-of-the-mvp.md), "Withdrawal and closure").
2. Where the erase-on-restore list is kept in deployment. It must sit outside the database backups ([deletion lifecycle](../specs/deletion-lifecycle.md), section 6). Options: a file on the server, excluded from the backup set, which is the current design through `GUESTBOOK_ERASE_ON_RESTORE_FILE`; or an encrypted store held with the backup provider. Blocks the deployment and the first restore drill (#33).

### Identifiers and review (#15, #24)

1. The handle for unpublished testimonies in review URLs. The [identifiers](../specs/identifiers.md) specification forbids internal IDs in any URL and names no key for unpublished testimonies. The current handle is a keyed digest of the internal ID, which cannot be reversed without the application secret. Options: accept the digest, and name it in the identifiers specification as the moderation handle (recommended, since it adds no field); or add a random review key as an operational field, which changes the data model. Needed before launch ([ADR 0018](../decisions/0018-implementation-choices-of-the-mvp.md), "Revisions and review").

### Moderation and parental consent (#24, #41)

1. Lifting a legal hold. The data model has no decision that ends a hold, except dismissing an automatic hiding. Options: add a `lift-hold` decision to [data model](../specs/data-model.md), section 2.10, with the rule and a note (recommended); or keep the current behaviour and resolve holds that the custodian sets by hand. Blocks ending any hold the custodian sets.
2. The lifetime of parental confirmation links. They last 15 minutes, the token lifetime of the [threat model](../specs/threat-model.md), section 3.1. Options: keep 15 minutes, and allow a new request (3 per parent address per day; current, recommended); or give parental links a longer lifetime, which amends the threat model ([ADR 0018](../decisions/0018-implementation-choices-of-the-mvp.md), "Contribution and consent").

### Launch controls (#20, #34)

1. Moderator second factor. The [threat model](../specs/threat-model.md), section 3.2, requires a phishing-resistant second factor for administration. Moderators sign in by magic link only. Blocks launch. Options: build a passkey check before the moderation area; or amend section 3.2 with a stated reason for accepting magic links for moderators.
2. Admin audit log. The [threat model](../specs/threat-model.md), section 3.2, asks for an append-only log of destructive actions. Only the moderation records exist. Blocks launch. Options: build a small append-only log of every destructive action; or accept the moderation records as the log, and amend section 3.2.

### Edition (#38)

1. Edition period. Editions are cumulative in the current build: each one holds every published testimony up to its cutoff. Options: keep cumulative editions (current); or let each edition hold only the testimonies of its own period. [Data model](../specs/data-model.md), section 5, does not settle it. Blocks the contents of the rehearsal edition.
2. Rehearsal cutoff. A build must come after its cutoff, which is 31 December of the year in the identifier, so a 2026 rehearsal cannot be built before 1 January 2027. Options: a cutoff date for rehearsals only, given by the owner (recommended); or wait for the calendar. Blocks the rehearsal before launch ([archive format](../specs/archive-format.md), section 9).

### Legal texts (#19)

1. The consent texts and the honest-limit texts are drafts ([ADR 0018](../decisions/0018-implementation-choices-of-the-mvp.md), "Contribution and consent"). The licence grant, the terms and the privacy notice carry the placeholder version "draft-2026-11-20". Decide who approves the final texts, and when, before the first real submission. Blocks launch.

## Deferred until after launch

Open on purpose: nothing before launch depends on them. Each is revisited when its trigger occurs.

| Decision | Trigger | Where |
| --- | --- | --- |
| Institution for deposit of editions, as a fourth copy and second custody | There are testimonies to deposit | [Archive format](../specs/archive-format.md), section 6.1; [institutional custodians](../research/institutional-custodians.md); #42 |
| Whether documentation and schemas are deposited on Zenodo | Same as above | [Institutional custodians](../research/institutional-custodians.md) |
| Who reviews moderation appeals | A second moderator joins | [Publishing rules](../legal/publishing-rules.md), "Asking for a review" |
| A standby transactional mail provider | Sign-in outages become a problem | [ADR 0015](../decisions/0015-backups-and-transactional-email.md), item 6 |
| WAL archiving, for a recovery point finer than a day | Daily loss becomes unacceptable | [ADR 0015](../decisions/0015-backups-and-transactional-email.md), item 5 |
| Moving the server away from OVHcloud | An account problem, or the project goes public at scale | [ADR 0014](../decisions/0014-provisional-vps-ovhcloud.md) |
| A region filter | Enough testimonies give a region | [Browsing and filters](../specs/browsing-and-filters.md), section 3.1 |
| Registry lock for the domain | Optional, at any time | [Domain record](../operations/domain.md), "Pending" |
| Making a testimony anonymous when its account is closed | A contributor asks for it. Until then, the field withdrawal does it in two steps | [ADR 0018](../decisions/0018-implementation-choices-of-the-mvp.md), "Withdrawal and closure"; [retention schedule](../specs/retention.md), section 5 |
| Localised interface URLs (`/en/`, `/fr/`) and `hreflang` | The French interface is written (#27) | [Identifiers](../specs/identifiers.md), section 2 |
| Translations of testimonies | The translation workflow is specified (#29) | [Data model](../specs/data-model.md), section 2.9 |
| Signing, compression and the independent reader of editions | The first real edition is built | [Archive format](../specs/archive-format.md), sections 1.1, 6 and 9 |
