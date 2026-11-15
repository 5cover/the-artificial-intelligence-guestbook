# 0002. Host on a single self-managed EU VPS

Status: Accepted (2026-11-15)

Issue: #9

## Context

Personal data must stay in the EU, and preferably with a provider not subject to non-EU extraterritorial access (plan section 21). The custodian is one person (plan section 28). Options considered: a French PaaS with managed PostgreSQL (lower patching burden, higher cost, platform coupling), a single EU VPS, or deferring the choice.

## Decision

Production runs on one self-managed VPS from an EU provider (Hetzner, OVHcloud, Scaleway or equivalent). The provider, region and size remain open (#9). Backups go to storage operated by a different provider (plan section 30).

## Consequences

- Cheap, transparent and easy for a successor to understand: everything is on one machine and described in `docs/operations/`.
- The custodian owns OS patching, firewalling, TLS, monitoring and restore drills. These become recurring duties in the runbook (#33).
- The machine is a single point of failure. Availability is traded for simplicity, and recovery time depends on tested backups (#31).
- The stack must run comfortably on a small VPS with modest memory (input to the stack RFP, #6).
