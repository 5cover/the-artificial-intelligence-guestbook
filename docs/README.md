# Documentation

Index of the project's documentation. Conventions for maintaining it are in [AGENTS.md](../AGENTS.md). Precedence when documents conflict: constitution, accepted decisions, specifications, code.

## Plan

- [Founding plan](plans/main.md): what the MVP must accomplish and under which constraints.

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

## Proposals

- [Stack RFP](proposals/stack-rfp.md): pass/fail gates, then a weighted comparison of twelve candidates (frameworks, WordPress, Next.js, bare Node.js) against a reference anti-stack, with a sensitivity analysis on churn (#6, #7).

## Research

- [Custodial indie projects](research/custodial-indie-projects.md): how projects run by individuals handle continuity, abuse and GDPR, and what failed.
- [Legal landscape](research/legal-landscape.md): GDPR, LCEN, DSA and copyright as they apply to the Guestbook. Research, not legal advice.
- [Domain and persistence](research/domain-and-persistence.md): domain choice, registrars, succession, persistent identifiers and edition packaging.

## Specifications

- [Identifiers and permanent URLs](specs/identifiers.md) (#15)
- [Threat model](specs/threat-model.md) (#20)

## Procedures

Step-by-step guides. See [procedures/README.md](procedures/README.md).

- [Register and configure the domain](procedures/register-and-configure-domain.md) (#8)

## Planned

- `specs/`: archive format (#13), data model (#14), deletion lifecycle (#16), retention schedule (#18).
- `legal/`: register, DPIA, privacy notice, mentions légales, publishing rules, consent texts (#19).
- `operations/`: runbook, recurring duties, recovery, succession (#33).
