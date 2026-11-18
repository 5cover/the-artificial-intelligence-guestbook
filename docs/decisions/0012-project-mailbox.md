# 0012. Project mailbox: `contact@theaiguestbook.org` on OVHcloud's free hosting

Status: Accepted (2026-11-18)

Issue: #45

## Context

ADR 0004 requires a project contact address for contributors, privacy requests and legal notices, separate from any personal mailbox. The domain procedure recommended the mailbox included with OVHcloud's free hosting plan, which comes with the domain: EU provider, DKIM configured automatically, no extra cost ([procedure](../procedures/register-and-configure-domain.md), section 6.1). The owner created the mailbox on 2026-11-18.

## Decision

1. The project mailbox is `contact@theaiguestbook.org`, hosted by OVHcloud under the free hosting plan attached to the domain.
2. It receives contributor messages, data-subject requests, notices about content, DMARC aggregate reports and, once the site runs, operational alerts that do not depend on the same mail path. Alerts about the mail path itself go to a different channel ([infrastructure proposal](../proposals/infrastructure.md), section 4.7).
3. It is not the login of the registrar account, which uses a mailbox outside the domain (ADR 0008).
4. Its contents follow the [retention schedule](../specs/retention.md), rows 25 and 26: correspondence about a request is deleted when the request is complete, and other correspondence is reviewed yearly.

## Consequences

- The domain, its DNS and the mailbox sit with one provider. This concentration was accepted in ADR 0008.
- The free plan holds one address. Role addresses such as `privacy@` or `security@` come later, as redirections or a paid mail plan ([procedure](../procedures/register-and-configure-domain.md), section 8.1).
- OVHcloud is a processor for the mailbox's contents. Its DPA must be recorded in the register of processing (#19).
- The mailbox password and its recovery material belong in the password manager and the succession envelope (#33).
