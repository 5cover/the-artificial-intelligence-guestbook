# Infrastructure proposal: VPS, backups and transactional email

Status: Partly decided. VPS: OVHcloud VPS-1, provisionally ([ADR 0014](../decisions/0014-provisional-vps-ovhcloud.md), 2026-11-19). Backup target and email: Hetzner Object Storage and Scaleway TEM ([ADR 0015](../decisions/0015-backups-and-transactional-email.md), 2026-11-19). Retention window, key custody, WAL archiving, mail standby and test accounts: awaiting owner decision.

Issues: #9, #10, #31

Research date: 2026-11-15. Source tags: [fetched] means the page was read in this pass through a summarising fetch tool, with figures cross-checked where two sources agreed; [search] means only a search-result summary or snippet was available; [inference] means reasoning from the cited sources. Each claim names its source as [S#], listed in section 9. Most price pages show no price date, so prices are "as read on 2026-11-15". Every figure must be re-read on the provider's console before any purchase. Nothing was signed up for or bought.

## 1. Summary of recommendations

1. VPS: a Scaleway Instance in Paris, DEV1-M class (3 vCPU, 4 GB), at EUR 14.74 per month excluding VAT [search] [S13]. Hetzner Cloud CPX22 in Helsinki (2 vCPU, 4 GB, 80 GB NVMe, IPv4 included) at EUR 16.99 excluding VAT [fetched] [S2] is the close runner-up, and the better choice if 8 GB of RAM is needed from the start (CPX32, EUR 30.49 in Helsinki) [fetched] [S2]. Both providers have documented account-suspension episodes, so the choice rests on jurisdiction and the DPA, not on a clean record (section 3).

2. Backups: encrypt each daily PostgreSQL dump on the VPS with age, using only a public recipient on the VPS, and keep the private identity offline in escrow [fetched] [S68]. Upload the encrypted dumps to a Hetzner Object Storage bucket in Helsinki or Nuremberg, not Falkenstein, with object lock in compliance mode and a 30-day retention [fetched] [S65] [S66]. The VPS can write backups but cannot read old ones, which matches the threat model's "keys held offline" control [S71].

3. Email: Scaleway Transactional Email (TEM), used over SMTP or its REST API. Its documentation describes no open or click tracking [fetched] [S19]. Its pricing is 300 emails free, then EUR 0.25 per 1,000 [fetched] [S18]. The fallback is Mailjet with tracking set to Disabled at account level, which Mailjet documents [fetched] [S39]. Brevo is rejected: its tracking cannot be switched off outside Enterprise, and two projects documented login and token links being rewritten in October and November 2026 [fetched] [S31] [S33] [S34].

4. Deletion window: propose 30 days, equal to the object-lock retention. The alternatives of 60 and 90 days, and their trade-offs, are in section 4.4.

5. Estimated cost for the recommended set: about EUR 21.41 per month excluding VAT (section 7).

6. Failure lessons that most change the design:
   - a backup in the same building as the server is no backup: in the 2021 Strasbourg fire, a court awarded damages to two OVHcloud customers who lost data, and one of them had its backup in the same building as its production server [fetched] [S44]; two other claims failed because those customers had not set up or bought backups [search] [S46];
   - backups must be run, monitored and restored, not assumed: GitLab's 2017 incident found that several backup methods had silently failed [fetched] [S47];
   - an account can be locked, and the warning may never arrive: Hetzner terminated Kiwix's account in late 2024, which Kiwix says came without notice, and Scaleway locked about 50 build servers in 2017 after an abuse report whose notice ticket apparently never opened [fetched] [S9] [S21];
   - a mail provider that rewrites links breaks login links [fetched] [S33] [S34].

## 2. Requirements derived from the ADRs and the threat model

- The VPS is a single, self-managed EU machine. This proposal also asked that its provider differ from OVHcloud, which holds the domain, DNS and the project mailbox; the owner accepted that concentration provisionally in ADR 0014 ([ADR 0002](../decisions/0002-single-eu-vps.md), [ADR 0008](../decisions/0008-canonical-domain.md)).
- The stack is Django 5.2 LTS on PostgreSQL 18, behind a reverse proxy, with systemd timers and encrypted off-site backups ([ADR 0010](../decisions/0010-stack-django-postgresql.md), section 8 of the [stack RFP](stack-rfp.md)). The sizing brief for this proposal is 2 to 4 vCPU and 4 to 8 GB of RAM, and traffic is modest and text-only.
- Backups are encrypted client-side before they leave the VPS, the keys are held offline and in succession escrow, and the backup target is append-only or object-locked for the retention window, at a different provider with separate credentials ([threat model](../specs/threat-model.md) section 3.7, required).
- Hardening: SSH keys only, no root login, automatic security updates, services as unprivileged users, and secrets readable only by the application user (threat model section 3.5, required).
- Unpublished testimonies never go to external services, and any processor must be an EU processor under a DPA (threat model section 3.6, required). This applies to the mail provider and the backup provider.
- The plan requires a real backup strategy, separate enough that one operational failure cannot destroy the archive, with recovery tested rather than assumed ([plan](../plans/main.md) section 30).
- Deletion propagates to backups within a defined and published expiry window, and the deletion procedure is tested before launch and periodically ([deletion philosophy](../constitution/deletion-philosophy.md), principles 2 and 9).
- Magic links must reach the contributor unmodified. The threat model already expects mail scanners to prefetch links (threat model section 3.1), so the mail path must add no tracking pixels and no link rewriting (task brief; [ADR 0003](../decisions/0003-email-magic-link-auth.md)).

## 3. VPS comparison and recommendation

| Option | Plan for sizing | Price excl. VAT | EU locations seen | Snapshots and backups | IPv6 | DPA | Ownership and jurisdiction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Scaleway Instance DEV1-M | 3 vCPU, 4 GB [S13] | EUR 14.74 per month, Paris; list price includes egress and IPv6, public IPv4 and block storage billed separately [search] [S13] | Paris seen; other EU zones not read | Instance snapshots about EUR 0.02 per GB-month in 2022 material [search] [S24]; current backup price not read | Included in list price [search] [S13] | A DPA exists, from a 2021 PDF; 2026 general terms refer to a processing agreement [search] [S22] [S23] | French provider; contracting entity and parent to confirm in the terms [search] [S23] |
| Hetzner Cloud CPX22 | 2 vCPU, 4 GB, 80 GB NVMe [fetched] [S2] | EUR 16.99 Helsinki, EUR 19.99 Nuremberg; prices include IPv4 [fetched] [S2] | Falkenstein, Nuremberg, Helsinki [fetched] [S1] | Daily automatic backups, 7 kept [fetched] [S3]; backup starting price EUR 1.098 per month [fetched] [S2], which a third-party source describes as 20 percent of the server price [search] [S4]; snapshots EUR 0.0143 per GB-month [fetched] [S2] | Free [search] [S5] | DPA accepted as a checkbox in the customer account [fetched] [S6]; sample text [search] [S7] | Hetzner Online GmbH, Gunzenhausen, Germany; managing directors named in its DPA [search] [S7]; shareholders not verified; US subsidiary exists [fetched] [S6] |
| Hetzner Cloud CPX32 | 4 vCPU, 8 GB, 160 GB NVMe [fetched] [S2] | EUR 30.49 Helsinki, EUR 35.99 Nuremberg [fetched] [S2] | As above | As above | Free [search] [S5] | As above | As above |
| netcup VPS Lite 2 | 4 vCPU, 8 GB, 160 GB SSD [fetched] [S25] | EUR 7.98, computed by dividing the displayed VAT-inclusive price by 1.19 [fetched] [S25] | Nuremberg, Vienna or Amsterdam, depending on availability [fetched] [S25] | "Snapshots listed", no price and no backup option shown [fetched] [S25] | IPv4 and IPv6 option [fetched] [S25] | Not verified | netcup GmbH, Karlsruhe; owned by the Anexia group since 2016 per several secondary sources [search] [S27] |
| OVHcloud VPS-1 (added 2026-11-19) | 2 vCores, 4 GB, 40 GB NVMe [search] [S72] | EUR 4.49 per month without commitment, EUR 3.81 with 12 months prepaid; IPv4 included [search] [S72] | Several; Strasbourg to be avoided | Daily backup of the last 24 hours included [search] [S72] | Not read | Not read | OVHcloud SAS, French; same provider as the domain and mailbox |
| OVHcloud VPS-2 (added 2026-11-19) | 4 vCores, 8 GB, 75 GB NVMe [search] [S72] | EUR 8.49 without commitment, EUR 7.21 with 12 months prepaid [search] [S72] | As above | As above | Not read | Not read | As above |
| Infomaniak VPS Lite | 4 vCPU, 8 GB, 160 GB [search] [S28] | CHF 18.00 per month with a 12-month prepayment [search] [S28] | Switzerland [search] [S28] | Not read | Not read | DPA template reportedly cites GDPR article 28; not verified on Infomaniak's pages [search] | Swiss; a foundation became majority owner in May 2026 [search] [S29]; Switzerland's EU adequacy stands [search] [S30] |

Abuse handling and suspension record:

- Hetzner: its general terms allow it to lock the server and terminate the contract "without prior notice" and "without notice" for listed reasons [fetched] [S8]. Kiwix, a project that distributes offline Wikipedia, reported on 2024-12-01 that its Hetzner servers went dark, that it received no email, and that access was locked; Hetzner replied that a termination notice had been sent by email on 2024-10-30 and that cases are reviewed manually [fetched] [S9]. Reviews describe suspensions with little explanation [search] [S69].
- Scaleway: its abuse documentation says Scaleway may suspend immediately "if it is deemed necessary and proportionate", and repeat reports on the same resource are treated as the customer's failure [search] [S20]. In July 2017, 50 linux-arm builders for the Go project went offline after the Scaleway account was locked for an abuse report; the automatic notification ticket apparently never opened, and Scaleway apologised and offered a EUR 20 credit [fetched] [S21]. Individual reviews describe lockouts within hours of signup [search] [S70], which are anecdotes.
- netcup: many forum and LowEndTalk reports describe servers taken offline after an abuse notice, with no grace period and slow support; one German forum post says a server is deactivated 48 hours after an unanswered abuse warning [search] [S26]. These are unverified anecdotes.
- Infomaniak: no abuse record was read in this pass.

Recommendation: Scaleway in Paris. The reasons are the French operator and Paris location, a DPA on file, and a price close to Hetzner's [search] [S13] [S22]. Its abuse-related lock is documented, and so is Hetzner's, so the record does not separate them. Hetzner is the better choice for RAM per euro and for documented snapshot pricing [fetched] [S2], and it is an acceptable choice if the owner prefers Germany or Finland. Either way, the mitigation is the same: backups at a different provider (section 4), a second contact address on the account, hardware-key two-factor authentication on the provider login (threat model section 3.8), and a rebuild runbook for a new provider. netcup has the lowest price but the weakest abuse record and was not recommended. The Scaleway price is from a search summary that quotes the official page, because the official pricing page returned HTTP 403 [search] [S13] [S14].

## 4. Backup design

### 4.1 What is backed up

- A daily PostgreSQL logical dump in custom format, with `pg_dump -Fc`, which is compressed by default and allows selective restore. It makes consistent exports while the database is in use [fetched] [S49].
- The archive edition export defined by the archive specification, which is independent of the application ([ADR 0006](../decisions/0006-archive-first-replaceable-application.md)) [inference from ADR 0006].
- Configuration and secrets needed to rebuild the VPS. These are encrypted with the rest of the backup, so they can be stored without exposing them [inference].
- Not backed up: application logs and caches, which have short retention by design (threat model section 3.6) [S71].

### 4.2 How often

- Daily, at a fixed hour. The recovery point objective is then up to 24 hours [inference].
- Optional, for an owner who wants a shorter recovery point: WAL archiving to the same object store, so that point-in-time recovery is possible. PostgreSQL supports this with a base backup and a continuous WAL sequence [fetched] [S48]. Archive lag increases the data that would be lost in a disaster, and a failing archive command is retried until it succeeds [fetched] [S48]. WAL retention is a second copy of deleted content, because the WAL "contains effectively everything in your database" [fetched] [S48], so its expiry must follow the same deletion window as the dumps.

### 4.3 Where

- Recommended: Hetzner Object Storage in Helsinki or Nuremberg. Its page describes object lock as available and prices the service from EUR 6.49 per month including 1 TB of storage [fetched] [S11]. Object lock is set at bucket creation and cannot be added later [search] [S67].
- Caveat: Hetzner's status page records that object lock retention and legal hold were unavailable in Falkenstein from 2025-11-10 to 2026-01-17, and recommends Nuremberg or Helsinki for object lock [fetched] [S66]. The bucket must therefore not be created in Falkenstein.
- Test before relying on it: create a throwaway bucket, upload an object with a compliance-mode retention, and confirm that deletion fails until expiry. Hetzner's page says only that compliance mode "cannot be ended in advance" [fetched] [S65]. No test is run in this pass, and no bucket was created.
- Alternative: OVHcloud Object Storage. It is French and documents object lock with versioning, which must be enabled first and can only be set at bucket creation [search] [S62]. Its governance mode lets privileged users bypass the lock [search] [S62]. Its page states no outbound traffic charges [fetched] [S63], but no storage price was readable in this pass [fetched] [S63].
- Rejected: Scaleway Object Storage, because it is the same provider as the recommended VPS, which threat model section 3.7 excludes. Its figures were EUR 0.01606 per GB-month Multi-AZ and 75 GB of free egress per month [search] [S15]. Object lock modes are documented [search] [S16].
- Rejected: Hetzner Storage Box, at EUR 3.20 per month for 1 TB [fetched] [S10]. Its page lists BorgBackup, restic and rsync, but no immutability feature [fetched] [S10]. The append-only Borg setup on a Storage Box comes from forum reports that were not confirmed by Hetzner's documentation [search] [S10].
- Rejected for now: Backblaze B2 in its EU region. It has governance and compliance lock modes [search] [S59] and egress free up to three times stored data [search] [S60], and it reportedly keeps EU capacity in Amsterdam [search] [S61]. Its headquarters and incorporation are in the United States [search] [S61], so US-law reach is a concern for an archive that must stay under EU jurisdiction. Its price is about USD 6.95 per TB-month according to third-party sites [search] [S60] and was not read from Backblaze's own page.
- Credentials: the VPS holds a key that can write objects but not change or delete locked ones. The restore key is held offline and is not on the VPS [inference from the lock semantics].

### 4.4 Retention and deletion window

Proposal: 30 days. Each daily encrypted dump is locked for 30 days in compliance mode, and expires when its lock ends. The window, and the fact that backups hold withdrawn testimonies until then, must be published in the privacy notice, as the deletion philosophy requires (principle 2).

The trade-offs are these:

- 30 days: the smallest exposure of withdrawn testimonies in backups, and the smallest storage cost. The risk is that silent corruption or a ransomware event is found after the last good backup has expired, so the daily backup check must alert within days (section 4.7).
- 60 days: twice the storage and exposure, and more time to detect corruption.
- 90 days: three times the storage and exposure, with the longest recovery window.

Compliance mode is preferred to governance mode. Compliance mode cannot be ended early, by anyone [fetched] [S65] [search] [S16], so a withdrawal cannot purge a locked backup early, and a stolen administrator key cannot purge the backups either. Governance mode would let the owner purge early, but it lets anyone holding the bypass permission do the same [search] [S62]. The cost of compliance mode is that a withdrawal is honoured in the live system at once and in backups only at expiry.

After a restore to an older point, the withdrawal list must be re-applied before the site is reopened, or withdrawn testimonies return [inference from the deletion philosophy, principle 9].

### 4.5 Tooling

| Tool | Encryption | Immutability or append-only | Status | Protects against | Does not protect against |
| --- | --- | --- | --- | --- | --- |
| age | Public-key file encryption with pluggable recipients [fetched] [S68] | Not a storage tool; retention comes from the bucket | Maintenance not checked in this pass | A stolen backup copy, and a compromised VPS reading old backups, because the VPS holds only the public recipient [inference] | Loss of the private identity; it provides no retention |
| restic 0.19.1, released 2026-07-05 [search] [S53] | Always on: AES-256-CTR with Poly1305-AES [fetched] [S54]; any S3 bucket [fetched] [S55] | None in the S3 backend; the password must be on the machine that writes [fetched] [S55] | Active releases in 2026 [search] [S53] | Deduplication, integrity, convenient restore | A compromised VPS can read all backups, because the writing machine needs the repository password [inference] |
| rest-server with `--append-only` | Client-side, as restic [fetched] [S56] | "Prevents deletion and modification of existing backups" [fetched] [S56] | Repository active, with 666 commits and 47 open issues shown [fetched] [S56] | Deletion by a compromised client | Needs its own server; it cannot run on a Storage Box [search] [S56] |
| BorgBackup 1.4.5, released 2026-07-18 [fetched] [S58] | Encrypted repositories [inference; not verified in this pass] | Append-only only restricts low-level segment writes; deletes and prune are still allowed by the client [fetched] [S57] | 2.0 is pre-release and says "do not use this on production backup repositories" [fetched] [S58] | Deduplication | Deletion through the normal client path [fetched] [S57] |
| pgBackRest v2.60.0, latest [fetched] [S51] | Encrypts the repository [fetched] [S50] | S3-compatible repositories and WAL push and get [fetched] [S50] | Release 2.59.3 fixed "possible weak encryption subkeys/salts" [fetched] [S52] | Point-in-time recovery, parallel backup | The cipher passphrase sits in the server configuration, so the VPS can read its backups [inference] |
| pg_dump custom format | Not built in; encrypt with age [inference] | None | Ships with PostgreSQL; a newer server cannot be dumped by an older pg_dump [fetched] [S49] | Logical corruption; a portable, version-tolerant copy | Point-in-time recovery; a dump is a day old at most |

Decision: daily pg_dump, encrypted with age, uploaded with an S3 client (the client to be chosen and tested; not verified in this pass), into a locked bucket. pgBackRest is the optional upgrade for WAL archiving (section 4.2). restic is the alternative if the owner accepts that the VPS can read backups.

### 4.6 Encryption keys and escrow

- The age identity (private key) is generated offline. Only its public recipient is installed on the VPS [fetched] [S68]. Losing the identity makes every backup unreadable [inference].
- Two offline copies: one in the succession envelope and one in a second secure place, for example a password manager with emergency access, held separately from the backup provider account. Threat model section 3.7 requires keys offline and in escrow [S71].
- The identity is never stored on the VPS, in the repository, or in the backup provider account.
- Rotation: add a new recipient on the VPS and keep the old identity in escrow until the backups it encrypted have expired.
- The restic password cannot be recovered if lost [fetched] [S55]; the same escrow rule applies if restic is chosen instead.

### 4.7 Restore drills

- Quarterly: restore the latest backup into a scratch PostgreSQL 18 server on a different machine, using only the escrowed identity and the restore key. Run the application tests, compare row counts, round-trip the archive export ([ADR 0006](../decisions/0006-archive-first-replaceable-application.md)), and record the elapsed time in `docs/operations/`.
- Annually: rebuild the whole service at a new provider from escrow alone. This simulates the loss of the VPS provider or its building.
- Deletion drill: withdraw a test testimony, restore an older backup that contains it, and confirm that the withdrawal list removes it before anything is published.
- Monitoring: a daily check of the age of the last successful upload and of the object count, with alerts sent to a channel that does not depend on the same account or mail path. GitLab's failure emails were rejected by the receiving side and no one noticed [fetched] [S47].
- The restore time must be measured. GitLab's restore took about 18 hours because the staging disks were slow [fetched] [S47].

## 5. Email comparison and recommendation

| Provider | Jurisdiction and ownership | DPA | Free or low tier | Open and click tracking | DKIM on our domain | API or SMTP | Suspension record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Scaleway TEM | French provider (section 3) | Scaleway DPA, not checked for TEM specifically [search] [S22] | 300 emails free, then EUR 0.25 per 1,000 on Essential; 100k included on Scale at EUR 0.20 per 1,000 [fetched] [S18] | No tracking: "Scaleway does not provide open or click tracking" [fetched] [S19]; to confirm in Scaleway's own API reference, which was not readable [search] | Concepts describe DKIM and SPF records [fetched] [S18]; the domain setup page was not read | REST API [fetched] [S19]; an SMTP relay is listed in the docs menu [fetched] [S18] | None found in this pass |
| Mailjet | Headquarters in Paris; parent Sinch AB, Sweden [search] [S41] | Not verified | Free: 6,000 per month and 200 per day; Starter USD 9 per month for 8,000 [fetched] [S38] | Account-level Disabled option: "Mailjet does not rewrite links for click tracking" [fetched] [S39]; anonymous tracking is not on the free plan [fetched] [S39]; per-message fields not found on the Send API v3.1 page read [fetched] [S40] | Not read | API and SMTP [search] [S41] | Anecdotal reviews of sudden suspensions [search] [S42] |
| Brevo | Sendinblue SAS, Paris, per archived terms; the archived terms also list access by group companies in the US, India and Canada [search] [S37] | A DPA appendix to the terms, per one reviewer [search] | Free tier 300 per day and Starter from USD 9, both from third-party summaries; the official pricing page returned only its title [fetched] [S35] | Only anonymisation is self-serve; disabling is on request for Enterprise [fetched] [S31] [search] [S32]; GitHub reports that X-Mailin-Track headers do not stop tracking [fetched] [S34] | Not read | SMTP and API [search] | Anecdotal non-compliance suspensions [search] [S36] |
| OVHcloud MX Plan mailbox | French | OVHcloud | Included with the mailbox; the same provider holds the domain and DNS (ADR 0008) | Not a bulk service | Not read | SMTP, limited to 200 emails per hour per account and 300 per hour per IP [fetched] [S43] | Not checked |
| Self-hosted SMTP on the VPS | Not applicable | Not applicable | Free software, but deliverability work | Not applicable | Configured by us | SMTP | Outbound port 25 is blocked by default on Hetzner cloud servers and unblocked on request [search] [S12]; Spamhaus removes listings only for a static IP that runs an outbound mail server [search] [S64] |

Recommendation: Scaleway TEM as the primary provider, for its documented absence of tracking, its price at modest volume, and its EU operator. Mailjet is the standby and the choice if the owner wants a second provider from the start. The concentration trade-off is real: if the VPS and the mail share one provider account, a lock on that account takes down both (section 8, question 7).

Design requirements that apply to any provider: tracking off, verified by sending a magic link to test mailboxes and checking that the link in the message is the canonical URL on theaiguestbook.org; SPF, DKIM and DMARC on the canonical domain as the research document sets out [S71]; and a send-failure alert that does not depend on the mail path it reports on.

## 6. Failure cases and their lessons

1. OVHcloud SBG2, Strasbourg, March 2021. Both the SBG1 and SBG2 buildings were affected by the fire [fetched] [S44]. A French court awarded Bluepad EUR 153,837 and Bati Courtage EUR 101,102 [fetched] [S44]. Bati Courtage's backup was in the same building as its production server; Bluepad's production server was in SBG1 and its backup was in SBG2 [fetched] [S44]. Two other claims were dismissed because those customers had not set up or bought backups [search] [S46]. OVHcloud's founder then promised free backups as a default [fetched] [S45]. Lesson: a backup at the same provider and site is not an independent copy. Design: different provider and different country (section 4.3).

2. GitLab.com database deletion, 2017-01-31. An engineer ran a deletion on the primary instead of the secondary, removing about 300 GB; GitLab.com was down for about 18 hours, and the restore also took more than 18 hours [fetched] [S47]. At least 5,000 projects, 5,000 comments and roughly 700 user accounts were lost [fetched] [S47]. The backups had failed in several ways: the daily pg_dump to S3 had produced an empty bucket, because it ran a 9.2 client against a 9.6 server; its failure emails were rejected because DMARC was not set up; the 6-hour LVM snapshot was used; Azure disk snapshots were not enabled on the database servers; and replication broke under load without WAL archiving [fetched] [S47]. Lessons: check that every backup job writes a non-empty, current artefact and alert on failure; match the pg_dump version to the server, as PostgreSQL documents [fetched] [S49]; replication is not a backup; and test restores at the planned speed. Design: section 4.7.

3. Kiwix, Hetzner, December 2024. Kiwix reported that its servers became unreachable on 2024-12-01, that it received no notice, and that its account access was locked; Hetzner said a termination notice had been emailed on 2024-10-30 [fetched] [S9]. Hetzner's terms allow locking and termination without notice for listed reasons [fetched] [S8]. Whether Kiwix had off-site backups is not established in the source [fetched] [S9]. Lesson: a provider notice can be the only warning, and it may not reach the operator. Design: a monitored contact path, a second contact on the account, and backups elsewhere.

4. Scaleway, Go builders, 2017. The Go project's 50 linux-arm builders went offline after an account lock for an abuse report; Scaleway said the automatic ticket failed and the servers were suspended after 48 hours; it apologised and offered a EUR 20 credit [fetched] [S21]. Lesson: the same as case 3, for another provider. Design: a rebuild runbook that works on a different provider within days.

5. Link rewriting breaking login links, October and November 2026. A Keycloak deployment sending through Brevo had its verification and password-reset links rewritten to Brevo redirect URLs; the issue, opened on 2026-10-25, is still open and proposes switching providers [fetched] [S33]. Another project found that Brevo rewrote sign-in, address-confirmation and voting links, and that the tokens in them passed through Brevo's click tracker; X-Mailin-Track headers did not stop it, Brevo staff said only Enterprise accounts can turn tracking off, and the maintainer accepted the limitation and documented it [fetched] [S34]. Lesson: a provider that cannot disable link rewriting is unusable for magic links, and tokens in tracked links reach a third party. Design: section 5.

6. Transactional mail providers suspending accounts. Anecdotal reports describe Brevo and Mailjet suspending accounts with little explanation [search] [S36] [S42]. No single incident with verified details was found, so none is relied on here. Lesson: keep a second provider configured and tested, and check the provider's dashboard for holds as a routine duty.

7. Untested restores. Covered by GitLab (case 2). The PostgreSQL manual adds that a failing archive command is retried, and a lagging archive increases loss [fetched] [S48]. Design: section 4.7.

## 7. Estimated monthly cost

| Item | Basis | EUR per month, excluding VAT |
| --- | --- | --- |
| Scaleway DEV1-M, Paris | List price as read on 2026-11-15 [search] [S13] | 14.74 |
| Scaleway public IPv4 and block storage | Billed separately; not priced in this pass [search] [S13] | Not included |
| Hetzner Object Storage | EUR 6.49 per month including 1 TB [fetched] [S11]; the page's overage figure is ambiguous, so the minimum is used | 6.49 |
| Scaleway TEM at 1,000 emails per month | 700 chargeable at EUR 0.25 per 1,000 [fetched] [S18] | 0.18 |
| Domain and DNS | OVHcloud, ADR 0008; price not read | Not included |
| Recommended total | | 21.41 |

Decided set (ADR 0014), with the proposed backup and mail: OVHcloud VPS-1 EUR 4.49 + 6.49 + 0.18 = EUR 11.16 [search] [S72].

Alternatives for comparison:

- Hetzner CPX22 in Helsinki, with the same backup and mail: EUR 16.99 + 6.49 + 0.18 = EUR 23.66, with IPv4 included per the page [fetched] [S2]. The IPv4 price is contradicted in search summaries [search] [S5].
- Hetzner CPX32 in Helsinki, for 8 GB from the start: EUR 30.49 + 6.49 + 0.18 = EUR 37.16 [fetched] [S2].
- netcup VPS Lite 2, the lowest price: EUR 7.98 + 6.49 + 0.18 = EUR 14.65 [fetched] [S25]. Not recommended because of its abuse record (section 3).

The backup figure is a floor. The base price includes 1 TB, and the database is expected to be a few gigabytes at most [inference], so the base price is the expected cost. VAT is not included. The public price pages were not dated, so each figure must be confirmed on the console before purchase.

## 8. Open questions for the owner

1. VPS: Scaleway in Paris (recommended), or Hetzner in Helsinki for more RAM per euro? Both have documented no-notice suspension episodes.
2. Backup target: Hetzner Object Storage in Helsinki or Nuremberg (recommended), or OVHcloud Object Storage, whose price must be read first?
3. Retention window: 30, 60 or 90 days? Is a compliance lock acceptable, knowing that a withdrawal cannot purge a locked backup early?
4. Recovery point: is a daily backup enough, or should WAL archiving be added, with its own retention rules?
5. Key custody: who holds the second offline copy of the age identity, and where?
6. Mail: Scaleway TEM alone, or Scaleway TEM with Mailjet as a tested standby?
7. Concentration: may the VPS and the mail share one provider account, given that a lock on it would stop both?
8. Sizing: is 8 GB of RAM needed from day one, or is 4 GB enough to start?
9. Verification: may test buckets and test mail accounts be created at the providers, so that object lock and tracking behaviour are proven before a commitment? This proposal does not sign up for anything.
10. Wording: the chosen window must be published in the privacy notice; who drafts it, under the legal review in [ADR 0007](../decisions/0007-privacy-review-path.md)?

## 9. Sources

Limits of this research: several official pages could not be read (Scaleway pricing and tutorial pages returned HTTP 403; the Backblaze pricing page redirected to a gateway that could not be followed; Brevo's pricing page returned only its title; OVHcloud's and Infomaniak's pricing content was missing or truncated). Where that happened, the figure comes from a search summary and is tagged [search], or it is marked as not verified.

- [S1] <https://www.hetzner.com/cloud> - fetched. Locations: Falkenstein, Nuremberg, Helsinki; US and Singapore sites exist.
- [S2] <https://www.hetzner.com/cloud/regular-performance> - fetched. CPX plan prices excl. VAT by location; backup starting price EUR 1.0980; snapshot EUR 0.0143 per GB-month. No price date shown.
- [S3] <https://docs.hetzner.com/cloud/servers/backups-snapshots/overview/> - fetched. Daily automatic backups, seven kept; snapshots kept until deleted.
- [S4] <https://dev.to/rozoomnews/hetzner-cloud-review-2026-four-years-three-servers-and-every-bill-explained-26kn> - search. Backup fee stated as 20% of server price; third-party, unconfirmed by Hetzner.
- [S5] <https://docs.hetzner.com/general/infrastructure-and-availability/ipv4-pricing/> - search snippet. Cloud primary IPv6 free; primary IPv4 EUR 0.50 per month; the page is marked as old.
- [S6] <https://docs.hetzner.com/general/company-and-policy/data-protection-at-hetzner/> - fetched. DPA accepted in the customer account; EU storage for non-cloud products; US subsidiary.
- [S7] <https://www.hetzner.com/AV/DPA_en.pdf> - search. Company address and managing directors.
- [S8] <https://www.hetzner.com/legal/terms-and-conditions/> - fetched. Sections 2.7 and 5.2 on locking and termination without notice; section 5.5 on customer backups.
- [S9] <https://news.ycombinator.com/item?id=42365295> - fetched. Kiwix account and server termination, December 2024; Hetzner's reply.
- [S10] <https://www.hetzner.com/storage/storage-box> - fetched. Storage Box plans and prices excl. VAT; supported tools; no immutability mentioned.
- [S11] <https://www.hetzner.com/storage/object-storage/> - fetched. EUR 6.49 per month including 1 TB; object lock described as supported; locations Falkenstein, Helsinki, Nuremberg. Overage figure ambiguous.
- [S12] <https://queensmtp.com/smtp-settings/hetzner> - search. Port 25 blocked by default on new Hetzner cloud accounts. Third-party.
- [S13] <https://www.scaleway.com/en/pricing/virtual-instances/> - search snippet, cross-checked by a third-party API read on 2026-11-06 (see S14). DEV1-M EUR 14.74 per month; list price includes egress and IPv6; storage and public IPv4 excluded.
- [S14] <https://catalogue.cost-pilot.com/scaleway> - search. Third-party cross-check of Scaleway instance prices.
- [S15] <https://www.scaleway.com/en/pricing/storage/> - search snippet. Multi-AZ EUR 0.01606 per GB-month; 75 GB egress free, then EUR 0.01 per GB.
- [S16] <https://www.scaleway.com/en/docs/object-storage/how-to/use-object-lock/> - search snippet. Governance and compliance modes; versioning required; compliance mode cannot be shortened.
- [S18] <https://www.scaleway.com/en/docs/transactional-email/concepts/> - fetched. 300 free emails on Essential, EUR 0.25 per 1,000 beyond; Scale 100k included, EUR 0.20 per 1,000; DKIM and SPF defined; SMTP relay defined.
- [S19] <https://anymail.dev/en/latest/esps/scaleway/> - fetched. Third-party integration documentation: Scaleway TEM is REST API only, with no open or click tracking.
- [S20] <https://www.scaleway.com/en/docs/dedibox-account/how-to/resolve-abuse/> - search snippet. Abuse process; immediate suspension wording (Dedibox documentation).
- [S21] <https://github.com/golang/go/issues/21237> - fetched. Scaleway builder lock, July 2017; Scaleway's statement and credit.
- [S22] <https://images-www.scaleway.com/wp-content/uploads/2021/08/19103126/Data-Processing-Agreement-03092021.pdf> - search. Scaleway DPA dated 2021; the PDF could not be fetched in this pass.
- [S23] <https://www-uploads.scaleway.com/Conditions_Generales_de_Services_v2026_a0028de41c.pdf> - search. 2026 general terms; refer to a personal data processing agreement.
- [S24] <https://www-uploads.scaleway.com/Scaleway_Upcoming_price_changes_Dec_1st_2022_863a99f92f.pdf> - search. Scaleway 2022 price change notice; snapshot prices per GB-hour. Dated.
- [S25] <https://www.netcup.com/en/server/vps-lite> - fetched. VPS Lite prices shown with 19 percent VAT; plans; snapshot listed without price; IPv4 and IPv6 option; locations.
- [S26] <https://lowendtalk.com/discussion/185783/netcup-shut-down-my-server-directly> and <https://forum.netcup.de/thread/19545-clarification-on-abuse-policy-immediate-server-shutdown/> - search. Anecdotal reports and a forum post on abuse deactivation timing.
- [S27] <https://netcup.cheap/kb/about/> - search. Anexia group ownership since 2016 and locations; secondary sources disagree on some details.
- [S28] <https://www.infomaniak.com/en/hosting/vps-lite> - search. VPS Lite plans; CHF 18.00 per month for 4 vCPU and 8 GB with an annual prepayment. The page was truncated when fetched.
- [S29] <https://menafn.com/1111142715/European-Digital-Sovereignty-Infomaniaks-Founder-Transfers-Control-Of-His-Company-To-A-Foundation> - search. Press release on the Infomaniak Foundation becoming majority owner in May 2026.
- [S30] <https://www.edoeb.admin.ch/edoeb/fr/home/datenschutz/international/angemessenheit.html> - search. Swiss data protection authority on the EU adequacy decision for Switzerland.
- [S31] <https://help.brevo.com/hc/en-us/articles/11643306229906-Can-I-anonymize-the-tracking-of-opens-and-clicks-for-my-emails> - fetched. Brevo offers anonymisation for transactional emails, which can be turned on and off; the article does not describe a disable option.
- [S32] <https://community.brevo.com/t/no-way-to-disable-by-option-tracking-in-transactional-e-mail/201> - search. Brevo staff: disabling tracking is available on request for Enterprise. Community thread, dated.
- [S33] <https://github.com/vocabulary-org/vocabulary-api/issues/141> - fetched. Brevo rewrites Keycloak verification and reset links; opened 2026-10-25; still open.
- [S34] <https://github.com/MarimerLLC/scheduler/issues/21> - fetched. Brevo rewrites sign-in, confirmation and voting links; X-Mailin-Track headers do not stop tracking; Enterprise-only per Brevo staff; dated 2026-11-01.
- [S35] <https://www.brevo.com/pricing/> - fetched. Returned only the page title; figures not read.
- [S36] <https://community.brevo.com/t/your-account-has-been-suspended-for-non-compliance-with-our-terms-of-use/6145> - search. Anecdotal suspension report.
- [S37] <https://www.brevo.com/legal/termsofservice-archive/> - search. Archived terms; contracting entity Sendinblue SAS, Paris; group companies. Over a year old.
- [S38] <https://www.mailjet.com/pricing/> - fetched. Free 6,000 per month and 200 per day; Starter USD 9 per month for 8,000 emails; prices excl. VAT in USD.
- [S39] <https://documentation.mailjet.com/hc/en-us/articles/51109335532571-Email-Tracking-Pixels-and-Consent-CNIL-and-Garante-Guidance> - fetched. Account-level open and click tracking can be Disabled; click tracking disabled means no link rewriting; anonymous option not on Free; updated 2026-11-04.
- [S40] <https://dev.mailjet.com/email/guides/send-api-v31/> - fetched. The part read covers message fields only; the tracking fields were not found there.
- [S41] <https://www.mailjet.com/ai-info/> - search. Mailjet by Sinch; headquarters Paris; parent Sinch AB.
- [S42] <https://www.trustpilot.com/review/mailjet.com?page=3> - search. Anecdotal suspension reviews.
- [S43] <https://docs.ovhcloud.com/en/guides/web-cloud/web-hosting/email-sending-best-practices> - fetched. MX Plan limits: about 200 emails per hour per account; 300 per hour per source IP; dedicated transactional services recommended for bulk. Updated 2026-09-03.
- [S44] <https://www.blocksandfiles.com/data-protection/2023/03/23/ovhcloud-must-pay-damages-for-lost-backup-data/1594496> - fetched. SBG2 fire, March 2021; damages to Bluepad and Bati Courtage; backup locations as described in section 6.
- [S45] <https://www.datacenterdynamics.com/en/news/ovh-fire-while-police-investigate-cause-ovhcloud-promises-free-backups-future/> - fetched. Klaba's promise of free backups by default; the article does not state a fire date.
- [S46] <https://www-datacenterdynamics-com.translate.goog/en/news/ovhcloud-ordered-to-pay-250k-to-two-customers-who-lost-data-in-strasbourg-data-center-fire/?_x_tr_sl=en&_x_tr_tl=id&_x_tr_hl=id&_x_tr_pto=tc> - search. Two other claims dismissed because no backup was set up or bought. Also <https://www.theregister.com/2021/03/23/ovh_fire_lab_restoration_update/>, which reports about 30 percent of affected customers had backups in the destroyed facility; not verified.
- [S47] <https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/> - fetched. GitLab 2017 postmortem: timeline, data loss, failed backup methods, restore time.
- [S48] <https://www.postgresql.org/docs/18/continuous-archiving.html> - fetched. Base backup and WAL archiving; archive command semantics; loss grows with archive lag.
- [S49] <https://www.postgresql.org/docs/18/app-pgdump.html> - fetched. Custom format; consistency under concurrent use; version compatibility rule.
- [S50] <https://pgbackrest.org/> - fetched. Full, differential and incremental backups; WAL push and get; repository encryption; S3, Azure, GCS and SFTP repositories; sponsors; MIT licence.
- [S51] <https://github.com/pgbackrest/pgbackrest/releases> - fetched. Latest release v2.60.0 (18 October); v2.59.3 (4 October); v2.59.2 (27 September); maintainer account shown.
- [S52] <https://github.com/pgbackrest/pgbackrest/releases/tag/release%2F2.59.3> - fetched. "Fix possible weak encryption subkeys/salts"; affected versions not named.
- [S53] <https://github.com/restic/restic/releases/tag/v0.19.1> - search. restic 0.19.1 released 2026-07-05; 0.19.0 on 2026-06-09.
- [S54] <https://github.com/restic/restic/blob/master/doc/design.rst> - fetched. Encryption: AES-256-CTR with Poly1305-AES; everything except key-file metadata encrypted; key revocation needs re-encryption.
- [S55] <https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html> - fetched. Backends include Amazon S3 and S3-compatible storage; password required; losing it makes data unrecoverable.
- [S56] <https://github.com/restic/rest-server> - fetched. The --append-only mode, its stated effect, and security notes.
- [S57] <https://borgbackup.readthedocs.io/en/stable/usage/serve.html> - fetched. borg serve --append-only restricts low-level writes; delete and prune remain possible; documentation for 1.4.5.
- [S58] <https://github.com/borgbackup/borg/releases> - fetched. 1.4.5 latest (18 July 2026); 2.0 betas flagged as not for production.
- [S59] <https://www.backblaze.com/docs/cloud-storage-enable-and-manage-lock-features> - search snippet. Governance and compliance modes; compliance cannot be removed.
- [S60] <https://www.backblaze.com/blog/cloud-101-data-egress-fees-explained/> - search. Free egress up to three times average stored data. Third-party price summary at <https://shattered.io/backblaze-pricing-b2-vs-wasabi-r2-s3-gcs-2026/> quoting about USD 6.95 per TB-month; not verified on Backblaze's pricing page, which redirected.
- [S61] <https://www.sec.gov/Archives/edgar/data/1462056/000119312521301141/d62601ds1.htm> - search. Backblaze S-1: principal offices in San Mateo, California; leased facilities in California, Arizona and Amsterdam.
- [S62] <https://docs.ovhcloud.com/en/guides/storage-and-backup/object-storage/s3-managing-object-lock> - search snippet. OVHcloud object lock: versioning first; set at bucket creation; governance bypass flag.
- [S63] <https://www.ovhcloud.com/en/public-cloud/object-storage/> - fetched. States no charges for incoming or outgoing traffic (vendor claim); no storage prices on the page read.
- [S64] <https://www.spamhaus.org/faqs/policy-blocklist-pbl/> - search snippet. PBL criteria: static IP, real outbound mail server, matching DNS.
- [S65] <https://docs.hetzner.com/storage/object-storage/howto-protect-objects/protect-object-lock-retention/> - fetched. Governance or compliance mode; "it is not possible to end compliance mode in advance".
- [S66] <https://status.hetzner.com/incident/5517a22b-2040-4ee3-9929-d2f480e7e163> - fetched. Object lock unavailable in Falkenstein, 2025-11-10 to 2026-01-17; Nuremberg or Helsinki recommended.
- [S67] <https://docs.hetzner.com/storage/object-storage/faq/buckets-objects/> - search snippet. Object lock can only be enabled when the bucket is created.
- [S68] <https://github.com/C2SP/C2SP/blob/main/age.md> - fetched. age is a file encryption format with pluggable recipients and identities.
- [S69] <https://nz.trustpilot.com/review/hetzner.com> - search. Anecdotal Hetzner suspension reviews.
- [S70] <https://www.trustpilot.com/review/scaleway.com> - search. Anecdotal Scaleway reviews of lockouts.
- Repository documents, cited by relative link in the text: [ADR 0002](../decisions/0002-single-eu-vps.md), [ADR 0003](../decisions/0003-email-magic-link-auth.md), [ADR 0006](../decisions/0006-archive-first-replaceable-application.md), [ADR 0007](../decisions/0007-privacy-review-path.md), [ADR 0008](../decisions/0008-canonical-domain.md), [ADR 0010](../decisions/0010-stack-django-postgresql.md), [threat model](../specs/threat-model.md), [plan](../plans/main.md), [deletion philosophy](../constitution/deletion-philosophy.md), [stack RFP](stack-rfp.md).
- [S71] Repository threat model, sections 3.1, 3.5, 3.6, 3.7, 3.8, and the domain research note `docs/research/domain-and-persistence.md`, which covers SPF, DKIM and DMARC (section 1.8).
- [S72] <https://dev.to/neurau_tech/vps-pas-cher-en-novembre-2026-8-hebergeurs-compares-au-prix-officiel-25k6>, <https://quasa.io/fr/media/ovhcloud-ou-scaleway-le-produit-compare-peut-inverser-l-ecart-de-prix>, <https://valebyte.com/en/providers/ovh/> - search summaries, 2026-11-19. OVHcloud VPS range of June 2026; prices raised in March 2026.
