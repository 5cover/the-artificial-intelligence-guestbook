# 0008. Canonical domain: theaiguestbook.org, no defensive registrations

Status: Accepted (2026-11-15). In effect: registered at OVHcloud on 2026-11-15 ([operations record](../operations/domain.md)).

Issue: #8

## Context

Every permanent testimony URL depends on the domain never lapsing ([identifiers](../specs/identifiers.md)). The [domain research](../research/domain-and-persistence.md) recommended `theaiguestbook.org` as canonical, plus `theaiguestbook.fr`, `aiguestbook.org` and `theaiguestbook.com` as defensive redirects. All four were unregistered on 2026-11-15 (RDAP 404). `aiguestbook.com` is registered by a third party.

`.org` is open to anyone, not tied to a country, and is not read by search engines as a country signal, which suits a bilingual, international archive. Vanity ccTLDs (`.io`, `.ai`) and small new gTLDs carry policy, pricing or registry-failure risks that are unacceptable for decades-long identifiers.

The owner judged defensive registrations unnecessary for a project of this scale. Their benefit is protection against impersonation, phishing, spoofed email and squatters; each one also adds renewals, DNS and email-policy upkeep to the custodial burden.

## Decision

1. The canonical domain is `theaiguestbook.org`.
2. No defensive domains are registered for now.
3. The registrar is an EU registrar different from the VPS provider: OVHcloud (owner's choice, 2026-11-15). It is French, the cheapest of the shortlist to start with, offers DNSSEC at no cost, and includes a free hosting plan with one mailbox. The VPS must therefore come from another provider (#9).
4. Term: 1 year with auto-renew until public launch, then at least 5 years from launch onwards. The permanence obligation starts when the first testimony URL is published. Before that, a lapse would cost the name but break no citation, and prepaying a decade for a project without users is not proportionate (owner decision, 2026-11-15).
5. Registrar lock, DNSSEC and expiry monitoring from day one. The registrar login uses a mailbox outside the domain, so that renewal and recovery mail still arrives if the domain fails. The account has hardware-key or TOTP two-factor authentication, and its recovery material is part of the succession arrangements (#33).
6. The procedure is [register-and-configure-domain](../procedures/register-and-configure-domain.md).

## Consequences

- The specifications use `theaiguestbook.org` in place of the earlier `<domain>` placeholder.
- Domain, DNS and the project mailbox sit with one provider. A lockout of the OVHcloud account would affect all three, but not the site or the data on the VPS. Accepted for one custodian, with the account secured by two-factor authentication and backup codes kept in the succession envelope.
- The public-launch gate (#34) must include extending the registration term.
- Someone else may register `theaiguestbook.fr`, `.com` or `aiguestbook.org` and impersonate the project. Accepted. Revisit if impersonation or phishing appears, or if the project grows enough to be a target.
