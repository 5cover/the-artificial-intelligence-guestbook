# Proposals and decision queue

Status: Living index (2026-11-15)

Proposals present options for an owner decision. Once decided, a proposal stays here as the record of the reasoning, and an ADR in [docs/decisions/](../decisions/) records the outcome ([AGENTS.md](../../AGENTS.md)).

## Proposals

| Proposal | Issues | State |
| --- | --- | --- |
| [Stack RFP](stack-rfp.md) | #6, #7 | Concluded: [ADR 0010](../decisions/0010-stack-django-postgresql.md) |
| [Legal bases, retention duty and minors](legal-bases-and-minors.md) | #12, #17, #18 | Concluded: [ADR 0013](../decisions/0013-legal-bases-and-minors.md) |
| [Licences for the project's own material and for editions](project-licensing.md) | #43 | Awaiting decision: L1 to L5 |
| [Infrastructure](infrastructure.md) | #9, #10, #31 | Awaiting decision: VPS, backups, email |
| [Context pages](context-pages.md) | #36 | Awaiting review: editorial rules and first set |
| [Reference shelf](reference-shelf.md) | #37 | Awaiting review: record format, selection criteria, 22 verified records |

## Decision queue

Decisions waiting for the owner, grouped by the work they unblock. The recommendation, where there is one, is in the linked section.

### Unblocks hosting, deployment and backups (#9, #10, #26, #31)

1. VPS provider and size ([infrastructure](infrastructure.md), section 3).
2. Backup target, encryption and key custody ([infrastructure](infrastructure.md), sections 4.3 and 4.6).
3. Backup window: 30 days proposed and aligned in the [deletion lifecycle](../specs/deletion-lifecycle.md) and [retention schedule](../specs/retention.md).
4. Transactional email provider ([infrastructure](infrastructure.md), section 5).
5. Whether test buckets and mail accounts may be created to verify object lock and tracking behaviour ([infrastructure](infrastructure.md), section 8).

### Unblocks the archive format and the first edition (#13, #38)

1. Licences for the documentation, context material, project translations and editions ([project licensing](project-licensing.md)).
2. Package serialization and signature scheme ([archive format](../specs/archive-format.md), section 12).
3. PDF/A or XML renditions, embargo option, DOI, number of copies and deposit institution ([archive format](../specs/archive-format.md), section 12; #42).

### Unblocks the data model and the interface (#14, #23, #27)

1. Proposed field set, text length limits and edition-period rule ([data model](../specs/data-model.md), sections 2.3, 2.7 and 5).
2. Visible redaction notes on the site and in editions ([data model](../specs/data-model.md), section 8).
3. Filter threshold N, whether region is ever shown, and date precision on listings ([browsing and filters](../specs/browsing-and-filters.md), section 6).
4. Whether a contributor may delete their account while keeping a testimony published, which would make later withdrawal impossible ([retention schedule](../specs/retention.md), section 4).

### Moderation (#41)

1. The review window, and who reviews while the custodian moderates alone ([publishing rules](../legal/publishing-rules.md)).
2. A separate code for defamation ([publishing rules](../legal/publishing-rules.md)).
3. The outside contact for wellbeing and qualification ([illegal-content protocol](../operations/illegal-content.md), section 8).

### Context (#36)

1. Editorial rules, first set of pages and who writes them ([context pages](context-pages.md)).

### Reference shelf (#37)

1. The record format, including the five added fields and naming against plan section 18 ([reference shelf](reference-shelf.md), section 7).
2. Whether all-rights-reserved resources are listed as metadata only, and whether sources run by individuals are allowed ([reference shelf](reference-shelf.md), section 7).

### Constitution (#2)

1. Ratify the ten constitution documents, or ask for changes ([constitution](../constitution/README.md)).
