# Retention schedule

Status: Draft (2026-11-15; periods accepted by the owner 2026-11-19). Follows [ADR 0013](../decisions/0013-legal-bases-and-minors.md), in particular option C of D2.

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
| 2 | Contributor sessions | 30 days of inactivity | Last use | Session expiry | Service (6(1)(b)) |
| 3 | Admin sessions | 12 hours | Sign-in | Session expiry | Security |
| 4 | Account email of an active account | While the account exists | | Account closure | Service, and the withdrawal channel |
| 5 | Account email after closure | 1 year in a restricted store, then deleted | Closure | Scheduled job | Decree 2021-1362 art. 3, if applicable (D2, option C) |
| 6 | Accounts with nothing submitted | Deleted after 12 months without sign-in, after a notice email 30 days before | Last sign-in | Scheduled job | Storage limitation |
| 7 | Drafts never submitted | 90 days | Last edit | Scheduled job, after a reminder email at 60 days | Storage limitation |
| 8 | Submitted, unmoderated testimonies | Until a decision | Submission | Moderation | Consent |
| 9 | Submitted testimonies never published, whose latest revision was returned, and their revisions | 6 months without an edit | Return | Scheduled job | Giving the contributor time to edit, and handling disputes about the decision |
| 10 | Published testimony, identity, disclosure, structured fields, translations | Until withdrawal or removal | Publication | Deletion lifecycle | Consent (6(1)(a), 9(2)(a)) |
| 11 | Revision bodies other than the public, archived, pending and latest returned revisions | Deleted as soon as a revision is none of these | Review or edit | Review and edit handling | Informed review, and genuine removal by the contributor (data model, section 2.5, rule 7) |
| 12 | Consent and age evidence | While the testimony is published, then a minimal record (public ID, dates, text versions accepted, consent path) for 5 years | Withdrawal | Scheduled job | Showing lawful processing; 5 years matches the general limitation period of French civil law (Code civil art. 2224) |
| 13 | Parental verification data (parent email, confirmation link) | Until the consent is recorded | Request | Deleted at once | CNIL Recommendation 7 |
| 14 | Moderation records (ordinary) | 12 months | Decision | Scheduled job | Accountability |
| 15 | Moderation records and notices about illegal content | As required by the illegal-content protocol (#41) | Decision | Manual, per the protocol | Legal obligation where it applies |
| 16 | Third-party notices (other) | 12 months | Outcome | Scheduled job | Accountability |
| 17 | Withdrawal requests in progress | Until completion | Request | Deletion lifecycle | |
| 18 | Withdrawal evidence (public ID, completion date, minor flag) | 5 years, then deleted. The public tombstone stays: it holds no personal data. | Completion | Scheduled job | Showing compliance |
| 19 | Rate-limit counters | The counting window, at most 24 hours | Window start | Expiry | Security |
| 20 | Application logs (no text, emails or raw IP addresses) | 14 days | Writing | Log rotation | Security, operations |
| 21 | Reverse-proxy access logs (no raw IP addresses) | 14 days | Writing | Log rotation | Security, operations |
| 22 | Error reports | 30 days | Writing | Rotation | Operations |
| 23 | Admin audit log (no text or emails) | 2 years | Writing | Scheduled job | Accountability of the custodian |
| 24 | Email provider logs | As short as the provider allows; target 30 days or less | Sending | Provider, per the DPA | Processor (#10) |
| 25 | Project mailbox: correspondence about a request | Until the request is complete | | Manual, part of the deletion procedure | |
| 26 | Project mailbox: other correspondence | 12 months | Receipt | Manual, yearly review | |
| 27 | Backups | 30 days, equal to the object-lock period ([ADR 0015](../decisions/0015-backups-and-transactional-email.md)) | Backup | Lock expiry and rotation, plus erase-on-restore | Recovery (deletion lifecycle, section 6) |
| 28 | Erase-on-restore list (internal IDs only) | The backup window plus 7 days | Withdrawal | Scheduled job | Deletion lifecycle |
| 29 | Hosted editions | As published; superseded revisions deleted when a privacy revision is published | | Privacy revision | Consent; archival model |
| 30 | Mirror-operator contacts | While they ask to be notified | Registration | On request | Legitimate interest |
| 31 | Published testimonies quarantined awaiting an edit | Indefinitely, hidden, until the contributor's edit is approved or the testimony is withdrawn (data model, section 2.5, rule 6) | Quarantine | Deletion lifecycle on withdrawal | Consent (6(1)(a)); the contributor can still edit or withdraw |

## 3. Scheduled jobs

One daily job applies rows 1, 5, 6, 7, 9, 12, 14, 16, 18, 19, 23 and 28. It reports to the custodian what it deleted, as counts, never as content. A job failure is an operational alert (#32). Log rotation (rows 20 to 22) and backup rotation (row 27) are configured in the server and the backup tool, and checked in the yearly drill (deletion lifecycle, section 7).

## 4. Open questions

1. [x] Row 5 is kept as written: the account email is held for one year after closure (owner decision, 2026-11-19, following ADR 0013, D2).
2. [ ] Whether a contributor may close their account and keep their testimony published, detached from any account (section 5).
3. [x] The 5-year periods in rows 12 and 18 rest on Code civil art. 2224, checked on Légifrance on 2026-11-19: "Les actions personnelles ou mobilières se prescrivent par cinq ans à compter du jour où le titulaire d'un droit a connu ou aurait dû connaître les faits lui permettant de l'exercer." Accepted by the owner.
4. [x] All proposed periods are accepted (owner decision, 2026-11-19).

## 5. Closing an account while keeping the testimony (proposal)

Forums often keep posts after account deletion and show them as written by a "deleted user". The same is possible here, but it is detaching, not anonymizing [inference, from GDPR recital 26 and art. 4(1)]:

1. Removing the account link does not make the testimony anonymous data. The text, and any display name, can still identify its author, so it stays personal data. Its publication still rests on the consent given at submission (ADR 0013, D1), which remains valid until withdrawn. Detaching is therefore lawful, but GDPR keeps applying.
2. The author keeps the right to withdraw. Without an account email, the request is verified the other way the deletion lifecycle already allows: describing the testimony from a new address, confirmed by the custodian ([deletion lifecycle](deletion-lifecycle.md), section 1). This is weaker: an impostor could try it, and a genuine author may fail to prove authorship.
3. Detaching never removes the identity the author chose. A contributor who wants their name gone as well asks for the identity fields to be withdrawn, which changes the testimony to anonymous and triggers a privacy revision of the editions that contain the name.
4. The account email still goes to the restricted store for one year (row 5).

Proposal: at account closure, the contributor chooses, with neither option preselected:

- withdraw the testimony and close the account; or
- keep the testimony published without an account, optionally made anonymous at the same time, after a plain warning that later withdrawal will require proving authorship without the account.

The consent record (row 12) and the tombstone rules are unchanged.
