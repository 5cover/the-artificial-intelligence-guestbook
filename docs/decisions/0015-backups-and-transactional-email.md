# 0015. Backups at Hetzner Object Storage, transactional email through Scaleway TEM

Status: Accepted (2026-11-19)

Issue: #10, #31

## Context

The server is an OVHcloud VPS-1 ([ADR 0014](0014-provisional-vps-ovhcloud.md)). Backups must be encrypted before they leave it, held at a different provider with separate credentials, and append-only or object-locked for the retention window ([threat model](../specs/threat-model.md), section 3.7; [ADR 0002](0002-single-eu-vps.md)). The site must send magic links (ADR 0003), parental-consent links and notices; the project mailbox is limited to 200 emails per hour and is not meant for this. Options and sources are in the [infrastructure proposal](../proposals/infrastructure.md), sections 4 and 5.

## Decision

1. **Backups:** daily PostgreSQL dumps, encrypted on the VPS with age to a public recipient only, uploaded to a Hetzner Object Storage bucket in Helsinki or Nuremberg (not Falkenstein), with object lock in compliance mode. The private key is held offline.
2. **Transactional email:** Scaleway Transactional Email (TEM), over SMTP or its API, with SPF and DKIM on `theaiguestbook.org`. No open or click tracking and no link rewriting.

3. **Retention window:** 30 days, equal to the object-lock retention. Backups older than 30 days are deleted, and the privacy notice publishes the window. The erase-on-restore list stays required: a restore brings back testimonies withdrawn after the backup was taken ([deletion lifecycle](../specs/deletion-lifecycle.md), section 6).
4. **Key custody:** the age private key is kept offline by the custodian and as a paper copy stored apart from the custodian's computer; the succession envelope (#33) says where. No second person is required.
5. **Recovery point:** daily dumps only, no WAL archiving. Up to a day of submissions can be lost in a disaster.
6. **No standby mail provider for now.** If Scaleway TEM is unavailable, sign-in and notices are delayed until it returns.
7. **Verification first:** test accounts are created at Hetzner and Scaleway to prove object lock and the absence of tracking before production use.

## Consequences

- Three providers, three accounts: OVHcloud (domain, DNS, mailbox, server), Hetzner (backups), Scaleway (mail). A lock at OVHcloud no longer reaches the backups or the mail account.
- Both providers need a DPA on file and an entry in the processing register (#19), and their credentials and two-factor setups go in the succession envelope (#33).
- DMARC can be tightened only once Scaleway TEM passes SPF and DKIM alignment ([mailbox procedure](../procedures/project-mailbox-and-dmarc.md), section 2.4).
- Expected cost: about EUR 11 per month excluding VAT with the VPS (proposal section 7).
