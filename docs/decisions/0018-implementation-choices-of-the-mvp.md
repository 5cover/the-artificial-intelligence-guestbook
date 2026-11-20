# 0018. Implementation choices of the local MVP

Status: Draft (2026-11-20). Not accepted: the owner decides which choices stand. Choices that need an owner decision are listed in the [decision queue](../proposals/README.md) under "MVP implementation" and are marked "queue" below.

Issues: #16, #21, #22, #23, #24, #25, #27, #38, #39, #41

## Context

The [MVP plan](../plans/mvp-implementation.md), section 4, lets the implementing agent decide details that no document settles, provided they do not change what a contributor, reader or moderator experiences. Several choices made during the implementation do change experience, or fill a gap that the specifications leave open. They were made in commits f12bc68 to 31be02c. This record collects them so that they can be checked against the code, and then accepted, changed or rejected by the owner.

No specification or earlier ADR was changed. Where a choice differs from a specification, the difference is named below.

## Decision

Paths are relative to `app/`. Each choice states what the code does.

### Accounts and sign-in

- Magic links last 15 minutes, are single-use, and are stored as SHA-256 digests. They serve sign-in, parental confirmation, withdrawal, closure and report confirmation (`accounts/magic_links.py`).
- Sign-in allows 5 requests per email address per hour. Per network, it allows 20 per hour with a solved proof-of-work challenge and 3 per hour without one (`accounts/views.py`).
- The proof-of-work asks for 16 leading zero bits of SHA-256 over the challenge and a nonce. A challenge is held in the session and is single-use (`accounts/proof_of_work.py`, `POW_DIFFICULTY_BITS`).
- Email and network keys are HMACs under the application secret. The network key also uses a salt that changes each day (`accounts/hashing.py`).
- The `purge_expired` command deletes sign-in links and rate-limit counters older than 24 hours (`accounts/management/commands/purge_expired.py`).
- Sessions expire after 30 days of inactivity.

### Contribution and consent

- A draft is one revision row, overwritten on each save. Its `submitted_at` is the time of the last save, and drafts keep no history (`testimonies/services.py`).
- Editing a submitted testimony adds a pending revision. Editing a published testimony adds a revision that goes live at once, unless the contributor is under 16, in which case the revision stays private until a moderator approves it (`testimonies/revisions.py`).
- Every correction repeats the publication statement and writes a consent record. The parental fields of the original record are copied to it.
- Under 16, the fields age range, region, link, organization and organization type are refused. The data model lists the first four. Organization type is added because it also reveals a sector of employment. (queue)
- Text fields refuse tabs and other control characters. Line feeds are allowed only in multi-line fields (`testimonies/forms.py`).
- Language tags are canonicalised: lowercase language, uppercase two-letter region, title-case four-letter script.
- The consent versions are the placeholder `draft-2026-11-20` for the licence grant, the terms and the privacy notice. The publication statement is the sentence of [ADR 0013](0013-legal-bases-and-minors.md), D6. The honest-limit texts on the submission page are drafts. All of them await legal review (#19). (queue)
- Parental requests are limited to 3 per parent address per day. The parent's address is deleted when consent is recorded (`testimonies/views.py`).

### Revisions and review

- Approval assigns the public ID and the publication date on first publication, numbers the revision, and makes it both public and archived (`moderation/services.py`).
- A revision that is none of public, archived, pending or the latest returned loses its content, and its identity becomes anonymous (`testimonies/revisions.py`, `release_superseded_text`).
- Returning a live edit restores the archived revision. Returned revisions keep their numbers and leave the timeline.
- Returning with quarantine hides the testimony, keeps the archived text, and clears the public revision.
- A legal hold is lifted only by approving the testimony or by dismissing the reports that caused an automatic hiding. The data model has no decision that ends a hold. (queue)
- The review token is a keyed digest of the internal ID, truncated to 32 hexadecimal characters. Lookup compares digests across the testimonies (`moderation/keys.py`). (queue)
- The queue lists testimonies with pending revisions or open reports. Urgent reports come first, then the earliest edition period, then the date of receipt (`moderation/views.py`).
- Removal is a moderation decision. Its withdrawal keeps the moderation record, so that the cause stays on file (`moderation/services.py`, `remove_testimony`).
- Moderators are the accounts listed in `GUESTBOOK_MODERATOR_EMAILS`. There is no second factor and no audit log yet. (queue)

### Reports

- Each reason maps to a publishing rule and a priority, as in [reports, section 1](../specs/reports.md). A reporter with three reports closed as no action gets later reports at low priority (`reports/services.py`).
- A report enters the queue after the reporter confirms it through a 15-minute link. Reports of child sexual abuse material enter the queue at once, and their email address is optional.
- Limits per day: 3 reports per email address. Per network, 10 with a solved proof-of-work challenge and 3 without one.
- Automatic hiding applies only to urgent reasons on confirmed reports, and only to testimonies that are published or submitted. It is capped at 1 per reporter per 30 days and 3 per site per day. Above the caps, the report is queued without hiding. A hiding is a legal-hold quarantine (`reports/services.py`).
- Confirmed urgent reports email the moderators.
- A repeated report from the same address on the same testimony is merged into the first.

### Publication and browsing

- Testimony pages, listings, data URLs and exports read only the public record built by `publication/records.py`.
- Search uses the French, English or simple PostgreSQL configuration, by the language of each testimony. It covers the public text and the display name. It allows 60 searches per network per hour.
- Listings show 50 testimonies per page, with excerpts of 280 characters. Filter and search pages are marked noindex. A filter offers only the values that published testimonies have.
- Citations: Hayagriva values are written as JSON strings, which are valid YAML double-quoted scalars. BibTeX removes braces from names.
- The context, references, methodology, publishing rules, privacy and terms pages are placeholders.

### Withdrawal and closure

- A withdrawal waits for a link to the account email. The link confirms only when the page is submitted, never on GET (`testimonies/withdrawal_views.py`).
- An anonymous contributor can withdraw with the withdrawal code, or with the former account email. The former address receives a link only if its keyed digest matches the one stored at closure.
- The withdrawal code has 16 Crockford symbols in four groups. It is stored as a keyed digest. It is shown once when the account is closed and sent to the account email at the same time.
- The tombstone keeps the language, the received date and the edition period, because constraint 5 of section 2.3 requires them on every non-draft testimony. The tombstone rule asks that they be deleted. (queue)
- Withdrawing a display name makes the testimony anonymous in every revision. Withdrawing any other field clears it in every revision.
- A legal hold postpones a withdrawal. The request is kept, with the single step `held-by-legal-hold`.
- Keeping a testimony without an account requires a published testimony. Making it anonymous at the same time is not built. (queue)
- The erase-on-restore list is a file named by `GUESTBOOK_ERASE_ON_RESTORE_FILE`. It holds testimony IDs, and is not written unless the variable is set. (queue)

### Export

- Editions are cumulative: an edition includes every published testimony whose edition period is at or before its year. (queue)
- An edition holds each testimony's archived revision, never unreviewed text. Each record carries `edition_id`, and its citation ends with the edition.
- A build refuses an identifier outside the archive format, a build dated on or before the cutoff of its year, an existing bag, and any testimony of its period with a pending revision. The cutoff rule also applies to rehearsals. (queue)
- Manifests are SHA-512 and SHA-256, written by the BagIt library. Files are written as UTF-8 with LF line endings and no byte-order mark.

### Storage and identifiers

- The uniqueness check on `relationship_to_ai` uses the SQL function `guestbook_is_distinct`, which the first testimony migration creates.
- Public IDs are 8 Crockford symbols drawn with `secrets.choice`, and drawn again if already used.

## Consequences

- Accepting this record makes its choices binding for the code. A choice that the owner changes needs a code change, and this record must be updated to match.
- The items marked "queue" are decided in the [decision queue](../proposals/README.md). Their outcome is written into this record when it is accepted.
- Not built, recorded so that the gaps are not forgotten: proof-of-work on testimony submission ([ADR 0017](0017-development-environment-and-unstyled-mvp.md), item 8); retention rows 5, 6, 7 and 9 of the [retention schedule](../specs/retention.md), since the purge command covers only rows 1 and 19; restoring a restricted account; a decision that ends a legal hold; the admin audit log and the admin second factor; signing and compression of editions; the round-trip test of the archive format; localised URLs and the French interface; live preview in the editor.
