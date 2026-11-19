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

### Moderation (#41)

1. The outside contact for wellbeing and qualification ([illegal-content protocol](../operations/illegal-content.md), section 8).

### Context (#36)

1. Editorial rules, first set of pages and who writes them ([context pages](context-pages.md)).

### Reference shelf (#37)

1. The record format, including the five added fields and naming against plan section 18 ([reference shelf](reference-shelf.md), section 7).
2. Whether all-rights-reserved resources are listed as metadata only, and whether sources run by individuals are allowed ([reference shelf](reference-shelf.md), section 7).

### Constitution (#2)

1. Ratify the ten constitution documents, or ask for changes ([constitution](../constitution/README.md)).

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
