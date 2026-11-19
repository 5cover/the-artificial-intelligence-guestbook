# Retention schedule

Status: Draft (2026-11-15). Follows [ADR 0013](../decisions/0013-legal-bases-and-minors.md), in particular option C of D2. Periods marked "Proposal" need owner review.

Issue: #18

Basis: [data model](data-model.md) (objects and the moment each clock starts, section 6); [deletion lifecycle](deletion-lifecycle.md); [threat model](threat-model.md); [legal research](../research/legal-landscape.md), sections 6, 10 and 12.

Rule: every category of personal data has a period and a mechanism that ends it. A category without both is a defect, like an unclassified field (data model, section 1). Every period here appears in the privacy notice (#19).

## 1. Minimum data collected

The service collects:

- the account email address;
- the content and optional metadata the contributor chooses to give;
- the consent evidence;
- short-lived operational data.

It does not collect, and does not log:

- names beyond an optional display name;
- phone numbers or postal addresses;
- identity documents;
- device fingerprints;
- analytics or tracking identifiers;
- raw IP addresses in any persistent store.

The reverse proxy and the application are configured to log no raw IP address. Anti-abuse uses keyed hashes with a salt rotated at least daily (data model, section 2.16; legal bases proposal, D2).

## 2. Schedule

| # | Data | Kept for | Starts at | Ended by | Basis |
| --- | --- | --- | --- | --- | --- |
| 1 | Sign-in tokens (hashed) | 15 minutes valid; deleted within 24 hours | Creation | Scheduled job | Security (6(1)(f)) |
| 2 | Contributor sessions | Proposal: 30 days of inactivity | Last use | Session expiry | Service (6(1)(b)) |
| 3 | Admin sessions | Proposal: 12 hours | Sign-in | Session expiry | Security |
| 4 | Account email of an active account | While the account exists | | Account closure | Service, and the withdrawal channel |
| 5 | Account email after closure | 1 year in a restricted store, then deleted | Closure | Scheduled job | Decree 2021-1362 art. 3, if applicable (D2, option C) |
| 6 | Accounts with nothing submitted | Proposal: deleted after 12 months without sign-in, after a notice email 30 days before | Last sign-in | Scheduled job | Storage limitation |
| 7 | Drafts never submitted | Proposal: 90 days | Last edit | Scheduled job, after a reminder email at 60 days | Storage limitation |
| 8 | Submitted, unmoderated testimonies | Until a decision | Submission | Moderation | Consent |
| 9 | Rejected testimonies and their versions | Proposal: 6 months | Rejection | Scheduled job | Handling disputes about the decision |
| 10 | Published testimony, identity, disclosure, structured fields, translations | Until withdrawal or removal | Publication | Deletion lifecycle | Consent (6(1)(a), 9(2)(a)) |
| 11 | Private text versions (originals under redaction) | While the testimony is published | | Deletion lifecycle | Integrity of the record (moderation principles) |
| 12 | Consent and age evidence | While the testimony is published, then a minimal record (public ID, dates, text versions accepted, consent path) for 5 years | Withdrawal | Scheduled job | Showing lawful processing; 5 years matches the general limitation period of French civil law (Code civil art. 2224, to confirm) |
| 13 | Parental verification data (parent email, confirmation link) | Until the consent is recorded | Request | Deleted at once | CNIL Recommendation 7 |
| 14 | Moderation records (ordinary) | Proposal: 12 months | Decision | Scheduled job | Accountability |
| 15 | Moderation records and notices about illegal content | As required by the illegal-content protocol (#41) | Decision | Manual, per the protocol | Legal obligation where it applies |
| 16 | Third-party notices (other) | Proposal: 12 months | Outcome | Scheduled job | Accountability |
| 17 | Withdrawal requests in progress | Until completion | Request | Deletion lifecycle | |
| 18 | Withdrawal evidence (public ID, completion date, minor flag) | 5 years, then deleted. The public tombstone stays: it holds no personal data. | Completion | Scheduled job | Showing compliance |
| 19 | Rate-limit counters | The counting window, at most 24 hours | Window start | Expiry | Security |
| 20 | Application logs (no text, emails or raw IP addresses) | Proposal: 14 days | Writing | Log rotation | Security, operations |
| 21 | Reverse-proxy access logs (no raw IP addresses) | Proposal: 14 days | Writing | Log rotation | Security, operations |
| 22 | Error reports | Proposal: 30 days | Writing | Rotation | Operations |
| 23 | Admin audit log (no text or emails) | Proposal: 2 years | Writing | Scheduled job | Accountability of the custodian |
| 24 | Email provider logs | As short as the provider allows; target 30 days or less | Sending | Provider, per the DPA | Processor (#10) |
| 25 | Project mailbox: correspondence about a request | Until the request is complete | | Manual, part of the deletion procedure | |
| 26 | Project mailbox: other correspondence | Proposal: 12 months | Receipt | Manual, yearly review | |
| 27 | Backups | 30 days, equal to the object-lock period ([ADR 0015](../decisions/0015-backups-and-transactional-email.md)) | Backup | Lock expiry and rotation, plus erase-on-restore | Recovery (deletion lifecycle, section 6) |
| 28 | Erase-on-restore list (internal IDs only) | The backup window plus 7 days | Withdrawal | Scheduled job | Deletion lifecycle |
| 29 | Hosted editions | As published; superseded revisions deleted when a privacy revision is published | | Privacy revision | Consent; archival model |
| 30 | Mirror-operator contacts | While they ask to be notified | Registration | On request | Legitimate interest |

## 3. Scheduled jobs

One daily job applies rows 1, 5, 6, 7, 9, 12, 14, 16, 18, 19, 23 and 28. It reports to the custodian what it deleted, as counts, never as content. A job failure is an operational alert (#32). Log rotation (rows 20 to 22) and backup rotation (row 27) are configured in the server and the backup tool, and checked in the yearly drill (deletion lifecycle, section 7).

## 4. Open questions

- D2 of the legal-bases proposal: if the decree is judged not to apply, row 5 becomes "deleted at closure".
- Whether a published testimony keeps the account email indefinitely (row 4) as its withdrawal channel, or whether contributors may choose to delete their account and keep the testimony published. That would make withdrawal impossible later; the interface would have to say so plainly.
- The 5-year periods in rows 12 and 18 rely on Code civil art. 2224, to be confirmed against its text before the privacy notice is published.
- All "Proposal" periods.
