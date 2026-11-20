# Withdrawal and deletion lifecycle

Status: Accepted (2026-11-20)

Issue: #16

Basis: [deletion philosophy](../constitution/deletion-philosophy.md); [archival model](../constitution/archival-model.md); plan sections 20 to 22; [data model](data-model.md); [identifiers](identifiers.md), section 3; [threat model](threat-model.md); [legal research](../research/legal-landscape.md), sections 4, 6, 10 and 12.

The goal is that deletion is a procedure, not an investigation (deletion philosophy, principle 3). This document lists every place personal data can live, what removes it from each, and how long that takes.

## 1. Requests

| Request | Who | Scope |
| --- | --- | --- |
| Withdraw a testimony | The contributor | The testimony, its versions, identity, disclosure, structured fields, translations and consent record |
| Withdraw one identity field | The contributor | One public-identity field (for example the display name). Produces a new public version and a privacy revision of editions containing the old value. |
| Remove superseded text from editions | The contributor | Text that an edit removed but that hosted editions still contain (data model, section 2.5, rule 8). Produces a privacy revision of those editions with the current text. |
| Close the account | The contributor | The account's testimony (withdrawn as above), then the account |
| Removal after a notice or a later finding | The moderator | As a testimony withdrawal; the cause is recorded privately (data model, section 2.13) |
| Erasure of data collected from a minor | The contributor, as a minor or later as an adult | As a testimony withdrawal, handled "dans les meilleurs délais" (Loi I&L art. 51 II, legal research section 4). No adult's approval is needed. |
| Other data-subject rights | Anyone | Access, rectification and objection follow the request procedure in `docs/legal/` (#19) |

Verification of authorship, in this order (owner decision, 2026-11-19):

1. With an account: a magic link sent to the account email.
2. Without an account, after closure (retention schedule, section 5):
   1. the withdrawal code: at closure, the contributor receives a random code, shown once and sent by email. Only a keyed hash of it is stored with the testimony. Presenting the code proves authorship, whoever holds it, so the contributor is told to keep it like a password;
   2. control of the original mailbox: the requester gives the address they used, and the service sends a magic link to it only if its keyed HMAC matches the one stored with the testimony at closure. Knowing the address is not enough; clicking the link proves control of it.
3. Neither is available: the request cannot be verified, because the testimony holds no other information that only its author could know. The contributor is told so in writing within one month, with the reason, the kind of information that would allow verification, and their right to complain to the CNIL and to seek a judicial remedy (GDPR art. 12(4)). GDPR allows the refusal when the controller demonstrates that it cannot identify the data subject, and does not require it to collect more data for that purpose (art. 11(2) and 12(2); EDPB Guidelines 01/2022 on the right of access, checked through search summaries on 2026-11-19). The custodian does not judge whether a request "sounds genuine", and never asks for identity documents (legal research, section 4, on CNIL Recommendation 7). The warning at closure says this plainly.

Facts that are public, or that an impostor could reconstruct, such as the text, the display name or the publication date, never count as proof. The exact submission time is not used either: contributors do not remember it, and it would only reward whoever guesses.

Deadline: without undue delay and within one month of receipt (GDPR art. 12(3), to be confirmed in the request procedure). Target for the automated steps of section 3: immediate.

1. A request record is opened on receipt, with its deadline. The contributor receives a written answer within the deadline even when the deletion is automatic, and any extension is recorded with its reason. Automatic deletion does not replace the answer: the CNIL's 2026 sanction against Extia concerned late replies and undocumented retention ([privacy research](../research/privacy-failures.md), R16.1).
2. A person who contributed as a minor can withdraw alone. Their withdrawal prevails over a parent's earlier consent, and no adult's approval is asked ([privacy research](../research/privacy-failures.md), R17.5).
3. Identity documents are never requested by default. Any that arrive anyway, in the mailbox or elsewhere, are deleted under the same request record (R16.7).

## 2. Inventory of places

| # | Place | What it may hold | Under project control | Removed by | Delay |
| --- | --- | --- | --- | --- | --- |
| 1 | PostgreSQL rows | Everything in the data model | Yes | Deletion job (section 3, step 2) | Immediate |
| 2 | PostgreSQL storage remnants | Dead row versions and WAL segments still on disk | Yes | Autovacuum and WAL recycling; the deletion job runs `VACUUM` on affected tables | Hours to days. Requirement for #26: the database volume is encrypted at rest, so that remnants are not readable from a detached disk. |
| 3 | Search vectors | Derived text | Yes | Derived in the database, so deleted with the row | Immediate |
| 4 | Reverse-proxy page cache | Rendered HTML of the testimony page and listings | Yes | Purge by URL in the deletion job; short cache lifetimes as a backstop | Immediate, at most the cache lifetime |
| 5 | Static renderings | Pre-rendered testimony pages and listings (ADR 0006), and the static data files and Markdown views ([identifiers](identifiers.md), section 2.1) | Yes | Regenerated without the testimony; the testimony page becomes the tombstone | Immediate |
| 6 | Hosted editions | Edition packages served for download | Yes | Privacy revision (section 4) | Within 30 days of verification |
| 7 | Withdrawal list | Public IDs of withdrawn testimonies | Yes | Not removed: it is the mechanism (section 5) | Updated immediately |
| 8 | Backups | Database dumps and file backups, encrypted | Yes | Expiry by rotation, plus erase-on-restore (section 6) | At most 30 days (ADR 0015) |
| 9 | Application and proxy logs | URLs with the public ID, timestamps, hashed or no IP addresses; never text or emails | Yes | Log rotation | Retention schedule (#18) |
| 10 | Email provider | The account email and message metadata for sign-in and notification emails | Under contract (processor) | The provider's retention, set in the DPA | Per provider (#10) |
| 11 | Project mailbox | Correspondence with the contributor about the request | Yes | Deleted when the request is complete, except the minimal evidence record | Upon completion |
| 12 | Custodian's own devices | The mail client's synced copy of the project mailbox (IMAP); otherwise nothing by policy, with no local exports or copies of unpublished content | Yes | Deletion on the server over IMAP, which the client mirrors; the disk is encrypted ([mailbox procedure](../procedures/project-mailbox-and-dmarc.md), section 1.2) | At the next sync |
| 13 | Search engines | Cached copies and snippets | No | The 410 response, plus removal requests through the engines' own tools | Days to weeks, not guaranteed |
| 14 | Web archives (Internet Archive, BnF dépôt légal) | Captures of published pages | No | Exclusion request where the archive offers one. The BnF's handling of erasure is unverified (domain research, section 3.7). | Not guaranteed |
| 15 | Third-party mirrors and downloads of editions | Full editions | No | The withdrawal list, and notification of known mirrors (section 5) | Not guaranteed |

Places 13 to 15 are outside the project's control. Contributors are told so before they submit (deletion philosophy, principle 6), using the wording drafted in the legal research (section 10).

## 3. Testimony withdrawal procedure

The deletion job runs these steps in order, in one transaction where the steps touch the database, and records each step in the withdrawal request (data model, section 2.12).

1. Set the testimony to `withdrawn` and create the tombstone. From this moment the URL answers 410 with the tombstone, and no listing, search or feed includes the testimony.
2. Delete the text versions, public identity, authorship disclosure, structured fields, translations and consent record. Then delete moderation records and notices about the testimony, unless a legal claim or an authority's request requires keeping them (#41). Delete the account link.
3. Run `VACUUM` on the affected tables.
4. Purge the reverse-proxy cache for the testimony URL in every locale, and for the listing and search pages.
5. Regenerate the static renderings affected.
6. Add the public ID to the withdrawal list, with the editions that contain it.
7. Schedule the privacy revision of every hosted edition containing the testimony (section 4).
8. Add the internal ID to the erase-on-restore list (section 6).
9. File removal requests with major search engines for the URL if it was indexed, and with the Internet Archive if it holds captures. These are manual steps for the custodian, listed in the job's output.
10. Notify known mirror operators (section 5).
11. Confirm completion to the contributor, including what could not be guaranteed (places 13 to 15). Then delete the correspondence (place 11).
12. Keep the evidence record: `public_id`, `completed_at` and `minor_at_collection`, with no account link (data model, section 2.12).

Field-level withdrawal follows steps 4 to 7, 10 and 11, with a new public version in place of steps 1 and 2.

Account closure withdraws the account's testimony, then deletes the account. If decree 2021-1362 applies, the account email is retained for one year in a restricted store and used for nothing else (legal research, section 6). This is an open legal question in #12.

## 4. Privacy revisions of editions

1. A privacy revision of edition `Y.n` is edition `Y.(n+1)`: the same content minus the withdrawn testimonies, with tombstones in their place and a changelog entry stating the number of withdrawals, not their identities ([archival model](../constitution/archival-model.md), principle 7).
2. Privacy revisions are batched, at most one a month, and within 30 days of the oldest verified request they include. Batching keeps the custodial burden bounded and avoids publishing a revision that pinpoints a single withdrawal date.
3. The superseded package is deleted from project hosting when the revision is published. Its checksums stay listed, so mirrors can recognize which version they hold.
4. Packaging details (BagIt, OCFL purge procedure) belong to the archive format (#13).

## 5. Withdrawal list and mirrors

1. The project publishes a machine-readable withdrawal list at a permanent URL, with one entry per withdrawn testimony: `public_id` and the edition IDs that contained it. It contains nothing else (data model, section 2.13).
2. The format is defined in the archive format (#13). It is also included in every edition, so that a mirror can apply it offline.
3. Mirror operators may register a contact address with the project to be notified. The registry of mirrors is private operational data.
4. The archive documentation and each edition's README ask mirror operators to apply the withdrawal list. The project does not claim it can enforce this (archival model, principle 9).

## 6. Backups

1. Backups rotate (ADR 0015) so that no backup older than 30 days is kept. A withdrawn testimony disappears from all backups at most 30 days after withdrawal. The window equals the 30-day compliance-mode object lock proposed in the [infrastructure proposal](../proposals/infrastructure.md), section 4.4. Each daily backup is immutable for 30 days, even against a compromised server, and expires when its lock ends. The window is published in the privacy notice. The tradeoff is recovery depth (60 or 90 days would allow later detection of corruption) against how long withdrawn data persists.
2. Erase-on-restore: the erase-on-restore list holds internal IDs only, never content. It is kept outside the database backups. After any restore, the deletion job is re-run for every ID on the list before the service is reopened. The list is pruned when an ID is older than the backup window.
3. Backups are encrypted client-side (threat model, section 3.7). Their keys are part of the succession arrangements (#33).

## 7. Testing and drills

1. Automated tests withdraw a fixture testimony and assert, for each place under project control (places 1 to 9):
   - every row is gone;
   - the URL answers 410;
   - the search no longer finds it;
   - the cache and static files no longer contain it;
   - the withdrawal list contains it;
   - the next edition build excludes it.
2. A deletion drill is run before launch and then yearly, on the production system with a test testimony. It includes a restore from backup followed by erase-on-restore (deletion philosophy, principle 9). The result is recorded in `docs/operations/`.

## 8. Open questions

- The privacy-revision cadence (monthly, within 30 days, proposed). The backup window is 30 days (ADR 0015).
- Whether decree 2021-1362 retention applies to the account email after closure (#12).
- How long moderation records and notices are kept after a removal that involved illegal content (#41, #18).
- The BnF's position on erasure requests for collected material (domain research, section 3.7).
