# Threat model

Status: Draft

Issue: #20

Basis: plan sections 21, 25, 26, 30; [ADR 0002](../decisions/0002-single-eu-vps.md), [ADR 0003](../decisions/0003-email-magic-link-auth.md), [ADR 0006](../decisions/0006-archive-first-replaceable-application.md); [privacy assumptions](../constitution/privacy-assumptions.md).

Stack-independent. Controls marked **(required)** are launch requirements; the rest are recommended.

## 1. Assets

| Asset | Why it matters | Where it lives |
| --- | --- | --- |
| Unpublished testimonies | Potentially sensitive self-disclosure not yet consented to publication; may contain third-party data or secrets awaiting moderation | Database, backups |
| Account emails | The only link between a person and their testimonies; enables withdrawal and could de-anonymize anonymous testimonies | Database, backups, email provider logs |
| Moderation records, redacted originals | Contain exactly what was judged unfit to publish | Database, backups |
| Privacy and withdrawal requests | Reveal who asked for what | Database, mailbox, backups |
| Admin access | Full control over all of the above | App, VPS |
| Custodian accounts | Email, registrar, VPS provider, backup provider, GitHub, DNS. Each one can take over the project | External providers |
| Backup encryption keys and edition signing keys | Confidentiality of backups; authenticity of editions | Offline, escrow |
| Published archive and editions | Integrity and availability; the project's purpose | Database, static files, mirrors |
| The domain | Every permanent URL depends on it | Registrar, DNS |

## 2. Adversaries

1. Spammers and SEO abusers: automated, high volume, low sophistication.
2. Harassers and doxxers: use testimonies to target third parties, or try to unmask anonymous contributors.
3. Opportunistic attackers: credential stuffing, scanning for known vulnerabilities, compromised dependencies.
4. Targeted attackers: someone seeking the identity behind a specific anonymous testimony, or wanting to deface or delete the archive.
5. Ideological flooders: try to overwhelm moderation or skew the archive.
6. Insider error: the custodian making a destructive mistake, or an export leaking private fields.
7. Providers and legal process: hosting, email or backup providers, and legal requests for data.

## 3. Threats and controls

### 3.1 Authentication and accounts

- **Magic-link token theft or replay.** Tokens are single-use, expire within 15 minutes, are stored only as hashes, and are invalidated on use **(required)**.
- **Email security scanners consuming links.** Corporate mail filters often prefetch links, which would burn single-use tokens or log in the scanner. Opening the link shows a confirmation page, and login happens only on an explicit POST from that page **(required)**. Offering a short one-time code as an alternative to the link is recommended.
- **Account enumeration.** The sign-in form responds identically whether or not an account exists **(required)**.
- **Session hijacking.** Secure, HttpOnly, SameSite cookies; session rotation at login; CSRF protection on every state-changing request; HTTPS only with HSTS **(required)**.
- **Disposable and mass accounts.** See ADR 0003: disposable-domain blocklist, MX check, proof-of-work, rate limits, pending caps.

### 3.2 Administration

- **Admin takeover through the custodian's mailbox.** A magic link alone is not enough for admin. Admin requires a phishing-resistant second factor (WebAuthn/passkey, hardware key preferred) **(required)**.
- **Exposed admin surface.** The admin interface is not reachable from the public internet: it is bound to localhost or a private interface and reached through an SSH tunnel or WireGuard **(recommended; strongly)**.
- **Destructive mistakes.** Destructive actions (delete, bulk reject, purge) require confirmation, are logged in an append-only audit log, and deletion is recoverable from backups until the backup expiry window passes, which is consistent with the deletion lifecycle.

### 3.3 Content

- **Stored XSS through testimonies.** Testimonies are stored and rendered as plain text, escaped on output. Only URLs are auto-linked. No user-supplied HTML or Markdown at MVP **(required)**. A strict Content-Security-Policy with no inline scripts **(required)**.
- **Link abuse and SEO spam.** Outbound links carry `rel="ugc nofollow noopener"` **(required)**. A per-testimony link count limit is enforced or flagged for moderation.
- **Unicode abuse.** Text is normalized to NFC. Bidirectional override characters and excessive combining marks are flagged for moderation, not silently stripped, because legitimate right-to-left text must survive.
- **Secrets and credentials in testimonies.** Submissions are scanned against known credential patterns before review, and hits are flagged to the moderator (plan section 25).
- **Third-party personal data and doxxing.** Handled by moderation (constitution), helped by flags for emails, phone numbers and street addresses detected in text.
- **Re-identification of anonymous contributors.** No public account linkage; filters suppressed below a population threshold ([browsing and filters](browsing-and-filters.md)); no timestamps finer than the date on public pages, and only the month on tombstones; no public age at all for minors ([data model](data-model.md), section 2.4.1). Exports apply the same rules.
- **Identification by writing style.** Stylometry, increasingly assisted by language models, can attribute anonymous text to known authors ([privacy research](../research/privacy-failures.md), lesson 3). No technical control prevents it. The mitigation is honesty: the consent text and a warning to anonymous contributors say so before submission (legal-bases proposal, D6). The archive offers no "similar testimonies" or style statistics that would make it easier.

### 3.4 Availability and abuse at scale

- **Flooding the moderation queue.** Pending caps per account, global intake throttle with an automatic "submissions paused" mode, and bulk moderation tools (ADR 0003).
- **Denial of service.** Public pages are cacheable and served by the reverse proxy; dynamic endpoints are rate-limited per hashed IP. A CDN would add a processor and usually a non-EU one, so none by default. If attacks justify one, prefer an EU provider and record it as an ADR.

### 3.5 Server and supply chain

- **Server compromise.** SSH keys only, no root login, minimal open ports, automatic security updates, services running as unprivileged users, secrets outside the repository and readable only by the app user **(required)**.
- **Compromised dependency.** Minimal dependency count is a stack selection criterion. Lockfiles committed, automated update PRs, updates applied on a fixed cadence and immediately for security advisories.
- **Known vulnerabilities in the stack.** A supported framework version at all times; end-of-support dates go on the operations calendar.

### 3.6 Data leaving the system

- **Export leakage of private fields.** Exports are built from an explicit allow-list of public fields. Every field in the data model is classified (public, private, operational), and a test fails if an unclassified field exists or a private field appears in an export **(required)**.
- **Logs.** Application logs do not contain testimony text, emails or full IP addresses. Reverse-proxy logs have short retention. Retention may be constrained by law (legal research, section 6); the final values go in the retention schedule (#18).
- **Unpublished content sent to third parties.** Unpublished testimonies are never sent to external services, including machine translation or AI tools. Only published testimonies may be machine-translated, and only through an EU processor under a DPA or a self-hosted system **(required)**.
- **Provider access and legal requests.** EU-controlled processors with DPAs. A documented procedure for answering legal requests, including the right to challenge them and to inform the contributor where lawful. Contributors are told before submitting that confidentiality holds only to the extent French and EU law allow: lawful requests can reach the account email the project holds. In the Belfast Project, oral-history confidentiality promises were overridden by subpoenas ([archive-failures research](../research/archive-failures.md)).
- **Identity documents arriving by email.** People sometimes send identity documents unasked, for example with a withdrawal request. They are never requested by default, and are deleted on receipt under the request record ([deletion lifecycle](deletion-lifecycle.md), section 1).
- **Suspected illegal content held by the project.** The `quarantined` state ([data model](data-model.md), section 3) hides the content without deleting it, keeps its text out of the moderation interface by default, and follows the [illegal-content protocol](../operations/illegal-content.md).

### 3.7 Backups and editions

- **Backup theft.** Backups are encrypted client-side before leaving the VPS **(required)**. Keys are held offline and in succession escrow.
- **Ransomware or account compromise deleting backups.** The backup target is append-only or object-locked for the retention window, and held at a different provider with separate credentials **(required)**.
- **Forged or tampered editions.** Editions ship with checksums (BagIt manifests) and a detached signature. The public key is published on the site, in the repository and in each edition. Key rotation and succession are documented.

### 3.8 Custodian accounts and domain

- **Takeover of email, registrar, VPS, DNS, GitHub or backup accounts.** Hardware-key two-factor authentication on each, unique passwords in a password manager, recovery codes in escrow **(required)**.
- **Domain hijack or lapse.** Registrar lock, DNSSEC, auto-renew, a registration extended to at least 5 years at launch, expiry monitoring, and a registrar separate from the VPS host ([ADR 0008](../decisions/0008-canonical-domain.md)).
- **Domain or account suspension after unanswered abuse reports.** A registrar or host may suspend a service whose abuse reports go unanswered; this happened to a Mastodon instance ([moderation research](../research/moderation-failures.md)). The registrar and host notification mailboxes are read daily, and abuse reports are answered within 24 hours ([recurring duties](../operations/recurring-duties.md)).
- **Lockout of a provider account.** Providers have locked accounts after abuse reports, with disputed warnings ([infrastructure proposal](../proposals/infrastructure.md), section 6). Domain, VPS and backups sit with three different providers, so that no single lockout removes the archive. The recovery path never depends on one account.
- **Email spoofing of the project.** SPF, DKIM and DMARC on the canonical domain; defensive domains parked with `p=reject`.

### 3.9 Structural controls

The absence of comments, messaging, profiles and follower graphs (plan section 15) is itself a security control. It removes the main channels for harassment, grooming and social engineering between users, including towards minors. New social features must be threat-modelled before they are proposed.

## 4. Vulnerability disclosure

Before launch, the repository has a `SECURITY.md` with a private reporting channel (GitHub private vulnerability reporting plus an email address). Security issues are not discussed in public issues until they are fixed ([ADR 0005](../decisions/0005-public-tracking.md)).

## 5. Residual risks accepted for the MVP

- A single VPS is a single point of failure. Recovery relies on tested backups.
- A determined, well-resourced spammer can still create accounts. Moderation is the final barrier, and its capacity is the binding constraint.
- Copies of editions downloaded by third parties cannot be recalled (deletion philosophy).
- The custodian is a single person. Their account security is the project's security.
