# 0008. Canonical domain: theaiguestbook.org, no defensive registrations

Status: Accepted (2026-11-15). Takes effect when the domain is registered.

Issue: #8

## Context

Every permanent testimony URL depends on the domain never lapsing ([identifiers](../specs/identifiers.md)). The [domain research](../research/domain-and-persistence.md) recommended `theaiguestbook.org` as canonical, plus `theaiguestbook.fr`, `aiguestbook.org` and `theaiguestbook.com` as defensive redirects. All four were unregistered on 2026-11-15 (RDAP 404). `aiguestbook.com` is registered by a third party.

`.org` is open to anyone, not tied to a country, and is not read by search engines as a country signal, which suits a bilingual, international archive. Vanity ccTLDs (`.io`, `.ai`) and small new gTLDs carry policy, pricing or registry-failure risks that are unacceptable for decades-long identifiers.

The owner judged defensive registrations unnecessary for a project of this scale. Their benefit is protection against impersonation, phishing, spoofed email and squatters; each one also adds renewals, DNS and email-policy upkeep to the custodial burden.

## Decision

1. The canonical domain is `theaiguestbook.org`.
2. No defensive domains are registered for now.
3. The registrar is an EU registrar different from the VPS provider. Gandi, OVHcloud and Infomaniak are shortlisted; live prices and registry-lock availability must be checked before choosing.
4. Registration for the longest available term, with auto-renew, a registrar lock, DNSSEC, and expiry monitoring. The registrar account uses a project mailbox with hardware-key two-factor authentication, and its recovery material is part of the succession arrangements (#33).

## Consequences

- The `<domain>` placeholder in the specifications becomes `theaiguestbook.org` once registered.
- Registration is first come, first served. Until the owner registers it, the decision is at risk.
- Someone else may register `theaiguestbook.fr`, `.com` or `aiguestbook.org` and impersonate the project. Accepted. Revisit if impersonation or phishing appears, or if the project grows enough to be a target.
