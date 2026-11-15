# 0003. Authenticate contributors with email magic links, defended in depth

Status: Accepted (2026-11-15)

Issue: #22

## Context

Authentication exists for anti-abuse and to validate later withdrawal requests, never to provide public identity (plan sections 4, 22, 25). Options considered: email magic links; magic links plus OAuth providers; OAuth only.

OAuth makes mass account creation somewhat harder but excludes people without those accounts, sends login metadata to non-EU companies, adds one maintained integration per provider, and complicates withdrawal if the contributor loses the account. Magic links work for everyone, including parents in a consent flow, and the private email doubles as the contact and withdrawal channel.

The owner raised the risk of spam via temporary email addresses and asked whether to allowlist domains. An allowlist was rejected because it would exclude legitimate ISP, institutional, small and privacy-focused providers, contradicting "anybody can express themselves" (plan section 3). No authentication method stops a determined spammer, so the goal is to make spam unprofitable and cheap to clear.

## Decision

Contributors sign in with single-use, short-lived email magic links. No passwords, no OAuth for now. Defences, in layers:

1. Reject sign-up from domains on a maintained disposable-email blocklist, and reject domains without valid MX records.
2. Nothing auto-publishes (plan section 9). Spam can only cost moderator attention, so protect that attention: cap pending entries per account, throttle global intake, and give the moderator bulk rejection and account suspension.
3. A self-hosted, privacy-friendly proof-of-work challenge on sign-up and submission. No third-party tracking captcha.
4. Per-account and per-hashed-IP rate limits with short retention.
5. Outbound links in entries are marked `rel="ugc nofollow"`, removing the SEO incentive (plan section 25).

The account email is private, never published and never exported to archives.

## Consequences

- Requires a transactional email provider (#10) and DNS authentication (SPF, DKIM, DMARC) on the project domain (#8).
- The blocklist is a dependency to keep updated, which goes on the recurring duties list.
- A contributor who uses a throwaway address loses the ability to authenticate a later withdrawal request; the sign-up page should say so plainly.
- OAuth can be added later by a new ADR if abuse patterns justify it.
