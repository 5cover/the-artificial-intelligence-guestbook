# 0014. Provisional VPS: OVHcloud VPS-1

Status: Accepted (2026-11-19)

Issue: #9

## Context

[ADR 0002](0002-single-eu-vps.md) chose a single self-managed EU VPS and left the provider open. The [infrastructure proposal](../proposals/infrastructure.md) recommended Scaleway DEV1-M in Paris (EUR 14.74 per month excluding VAT, IPv4 and disk extra), partly to keep the server at a different provider from OVHcloud, which already holds the domain, DNS and project mailbox ([ADR 0008](0008-canonical-domain.md), [ADR 0012](0012-project-mailbox.md)).

OVHcloud's VPS-1 (2 vCores, 4 GB RAM, 40 GB NVMe, IPv4 and a 24-hour daily backup included) is listed at EUR 4.49 per month excluding VAT without commitment, or EUR 3.81 with a 12-month prepayment (third-party comparisons of November 2026; to be confirmed on the order page). Its memory matches the proposal's sizing brief: Django, PostgreSQL 18 and the reverse proxy fit in 4 GB for a moderated, text-only site.

The owner accepts the concentration risk provisionally. The OVHcloud account has a long unique password and OTP two-factor authentication, which protects against takeover. It does not protect against the provider locking the account (abuse report, payment or billing error), which would stop the domain, mail and server together.

## Decision

1. Production runs on an OVHcloud VPS-1, provisionally. VPS-2 (4 vCores, 8 GB) is the upgrade path.
2. The datacentre is in the EU and not Strasbourg; the exact location is chosen at order time.
3. Backups stay at a different provider with separate credentials (ADR 0002; proposal section 4), so that an OVHcloud fire, data loss or account lock cannot take the archive with it.
4. The rebuild runbook must work on another provider, so that leaving OVHcloud is a rebuild, not a migration project.

## Consequences

- Monthly cost falls from about EUR 21 to about EUR 11 excluding VAT with the proposed backup and mail (proposal section 7).
- One provider account now holds the domain, DNS, mailbox and server. Its two-factor setup and recovery codes belong in the succession envelope (#33).
- The 40 GB disk is the first limit. Hosted editions move to object storage if downloads grow.
- Revisit when the project goes public at scale, if OVHcloud suspends or threatens the account, or when the rebuild drill shows a move would be cheap.
