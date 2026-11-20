# Documentation

Index of the project's documentation. Conventions for maintaining it are in [AGENTS.md](../AGENTS.md). Precedence when documents conflict: constitution, accepted decisions, specifications, code.

## Plan

- [Founding plan](plans/main.md): what the MVP must accomplish and under which constraints.
- [Local MVP implementation plan](plans/mvp-implementation.md): scoped instructions for the agent implementing the first local MVP.

## Constitution

Authoritative principles. See [constitution/README.md](constitution/README.md).

- [Mission](constitution/mission.md)
- [Editorial principles](constitution/editorial-principles.md)
- [Moderation principles](constitution/moderation-principles.md)
- [Privacy assumptions](constitution/privacy-assumptions.md)
- [Authorship disclosure](constitution/authorship-disclosure.md)
- [Archival model](constitution/archival-model.md)
- [Deletion philosophy](constitution/deletion-philosophy.md)
- [Multilingual principles](constitution/multilingual-principles.md)
- [Relationship to external archives](constitution/external-archives.md)
- [Continuity](constitution/continuity.md)

## Decisions

- [Template](decisions/template.md)
- [0001. Record decisions in the repository](decisions/0001-record-decisions.md)
- [0002. Host on a single self-managed EU VPS](decisions/0002-single-eu-vps.md)
- [0003. Authenticate contributors with email magic links, defended in depth](decisions/0003-email-magic-link-auth.md)
- [0004. The operator is publicly named](decisions/0004-operator-identity.md)
- [0005. Track work publicly](decisions/0005-public-tracking.md)
- [0006. The archive is the primary deliverable; the application is replaceable](decisions/0006-archive-first-replaceable-application.md)
- [0007. Privacy review path for the MVP](decisions/0007-privacy-review-path.md)
- [0008. Canonical domain: theaiguestbook.org, no defensive registrations](decisions/0008-canonical-domain.md)
- [0009. Testimonies are licensed CC BY 4.0, separately from the project's own intellectual property](decisions/0009-testimony-licensing.md)
- [0010. Application stack: Django 5.2 LTS on PostgreSQL 18](decisions/0010-stack-django-postgresql.md)
- [0011. The interface calls a contribution a "testimony" ("témoignage")](decisions/0011-testimony-in-the-interface.md)
- [0012. Project mailbox: `contact@theaiguestbook.org` on OVHcloud's free hosting](decisions/0012-project-mailbox.md)
- [0013. Legal bases, identification-data retention and minors](decisions/0013-legal-bases-and-minors.md)
- [0014. Provisional VPS: OVHcloud VPS-1](decisions/0014-provisional-vps-ovhcloud.md)
- [0015. Backups at Hetzner Object Storage, transactional email through Scaleway TEM](decisions/0015-backups-and-transactional-email.md)
- [0016. Licences for the project's own material and for editions](decisions/0016-project-licensing.md)
- [0017. Development environment, and an unstyled MVP with minimal JavaScript](decisions/0017-development-environment-and-unstyled-mvp.md)
- [0018. Implementation choices of the local MVP (draft, awaiting acceptance)](decisions/0018-implementation-choices-of-the-mvp.md)

## Proposals

Open decisions are gathered in the [decision queue](proposals/README.md).

- [Stack RFP](proposals/stack-rfp.md), concluded by ADR 0010: pass/fail gates, then a weighted comparison of thirteen candidates (frameworks, WordPress, Next.js, bare Node.js, minimal TypeScript) against a reference anti-stack, with a sensitivity analysis on churn (#6, #7).
- [Legal bases, retention duty and minors](proposals/legal-bases-and-minors.md): seven owner decisions on GDPR bases, decree 2021-1362, the DSA, age thresholds, parental consent, explicit consent and the DPIA (#12, #17, #18).
- [Licences for the project's own material and for editions](proposals/project-licensing.md) (#43).
- [Infrastructure](proposals/infrastructure.md): VPS, encrypted immutable backups at a second provider, transactional email without tracking, cost, and lessons from real incidents (#9, #10, #31).
- [Context pages](proposals/context-pages.md): editorial rules and a first set of nine pages (#36).
- [Reference shelf](proposals/reference-shelf.md): record format, selection criteria and 22 verified external resources (#37).

## Research

- [Custodial indie projects](research/custodial-indie-projects.md): how projects run by individuals handle continuity, abuse and GDPR, and what failed.
- [Legal landscape](research/legal-landscape.md): GDPR, LCEN, DSA and copyright as they apply to the Guestbook. Research, not legal advice.
- [Domain and persistence](research/domain-and-persistence.md): domain choice, registrars, succession, persistent identifiers and edition packaging.
- [Archive failures](research/archive-failures.md): how archives and testimony collections failed (MySpace, Belfast Project, Domesday, Yahoo Groups and others), and requirements for editions.
- [Privacy failures](research/privacy-failures.md): re-identification, stylometry, timing leaks, erasure and minors' data cases, and requirements for the data model, deletion, retention, minors and filters.
- [Moderation failures](research/moderation-failures.md): how moderation breaks on small platforms, and the French and EU duties for illegal content.
- [Institutional custodians](research/institutional-custodians.md): who could receive deposits of the editions or succeed as custodian, and how GDPR withdrawal interacts with each (#42).
- [Interpretability dependencies](research/interpretability-dependencies.md): living diagnostic of the standards and conventions a future reader needs to interpret an edition, with cheap mitigations.

## Specifications

- [Identifiers and permanent URLs](specs/identifiers.md) (#15)
- [Threat model](specs/threat-model.md) (#20)
- [Data model and testimony lifecycle](specs/data-model.md) (#14)
- [Withdrawal and deletion lifecycle](specs/deletion-lifecycle.md) (#16)
- [Archive format and edition packaging](specs/archive-format.md) (#13), with its JSON Schemas in [archive/schema/](../archive/schema/)
- [Retention schedule](specs/retention.md) (#18)
- [Browsing, search and filters](specs/browsing-and-filters.md) (#27)
- [Reports](specs/reports.md): how reports of published testimonies are received, prioritized, limited and decided, and how impersonation is handled.

## Operations

- [Domain](operations/domain.md): non-secret record of the domain's registration and configuration.
- [Local development environment](operations/local-development.md): how the development machine runs PostgreSQL 18 and uv without administrator rights.
- [Illegal content, threats and third-party notices](operations/illegal-content.md): draft custodian protocol (#41).
- [Recurring duties](operations/recurring-duties.md): the custodial obligation as a calendar, from daily checks to yearly drills (#33).

## Legal drafts

- [Publishing rules](legal/publishing-rules.md): the closed list of moderation grounds with stable codes, review and reporting (#19).

## Procedures

Step-by-step guides. See [procedures/README.md](procedures/README.md).

- [Register and configure the domain](procedures/register-and-configure-domain.md) (#8)
- [Use the project mailbox and read DMARC reports](procedures/project-mailbox-and-dmarc.md) (#46)

## Planned

- `legal/`: register, DPIA, privacy notice, mentions légales, consent texts (#19), once the legal-bases proposal is decided.
- `operations/`: recovery runbook and succession arrangements (#33), once the infrastructure is chosen.
