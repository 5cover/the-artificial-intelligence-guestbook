# Recurring duties

Status: Draft (2026-11-15). Becomes binding at launch. Items depending on undecided infrastructure are marked "(after #9)".

Issue: #33

Basis: [continuity](../constitution/continuity.md); [deletion lifecycle](../specs/deletion-lifecycle.md); [retention schedule](../specs/retention.md); [archive format](../specs/archive-format.md); [threat model](../specs/threat-model.md); [illegal-content protocol](illegal-content.md); [domain procedure](../procedures/register-and-configure-domain.md); [infrastructure proposal](../proposals/infrastructure.md).

The custodial obligation as a calendar. Each duty names its trigger, what "done" means and where the result is recorded. Duties that a script can check are automated, and their failure alerts the custodian, but automation does not remove the duty (continuity, "Design for one person" 2).

## Continuous or event-driven

| Duty | Trigger | Done when | Recorded in |
| --- | --- | --- | --- |
| Moderate the queue | New submission | Decision taken, with a statement of reasons where needed | Moderation records |
| Answer a withdrawal or other data-subject request | Request received | Answered within one month, deletion procedure complete | Withdrawal request record (deletion lifecycle, section 1) |
| Handle a notice or suspected illegal content | Notice or flag | Protocol followed | Moderation records ([illegal-content protocol](illegal-content.md)) |
| Answer the registrar's or host's abuse reports | Report received | Answered the same day, or within 24 hours at most | Mailbox; domain record |
| Apply security updates | Advisory for the OS, PostgreSQL, Django or a dependency | Patched, or a documented mitigation | Commit or operations log |
| Respond to an operational alert | Backup age, failed job, certificate or domain expiry, error rate | Cause fixed | Operations log |
| Personal data breach | Suspected breach | CNIL notified within 72 hours where required, and contributors informed where required | Breach record (#19) |

## Daily

| Duty | Automated | Done when |
| --- | --- | --- |
| Retention job (retention schedule, section 3) | Yes | Report of counts received; a failure alerts |
| Backup upload and age check (after #9) | Yes | Last successful upload under 26 hours old |
| Read the registrar notification mailbox | No | Read |

## Weekly

| Duty | Done when |
| --- | --- |
| Check that the moderation backlog is under the published target (proposal: no submission older than 14 days) | Backlog checked; if it is over the target, the intake throttle is lowered or submissions are paused, openly (continuity, "Design for one person" 3) |
| Check dependency update proposals | Merged or deferred with a reason |

## Monthly

| Duty | Done when |
| --- | --- |
| Privacy revision of hosted editions, if any withdrawal is pending | Revision published within 30 days of the oldest request (deletion lifecycle, section 4) |
| Read DMARC aggregate reports | Anomalies investigated |
| Refresh the disposable-domain blocklist (ADR 0003) | Updated from the maintained list, committed |

## Yearly

| Duty | Suggested month | Done when |
| --- | --- | --- |
| Produce the annual edition (time capsule) | January to February, after the queue for the period is cleared | Edition published, deposited, registered (archive format) |
| Fixity check of every copy of every edition | With the edition | All digests match, or repaired from a matching copy; logged (archive format, section 6.1) |
| Restore drill: database from backup into an empty server, with erase-on-restore | Before the edition | Restored, with elapsed time recorded (deletion lifecycle, section 7) |
| Deletion drill on production with a test testimony | With the restore drill | Every place in the inventory verified |
| Edition drill: restore an edition from one copy and read it with the independent reader | With the edition | Read successfully, with time recorded |
| Retention audit: compare the schedule with live systems and the privacy notice | Any | Mismatches fixed |
| Verify the reference shelf: dead links, changed operators or licences | Any | Records updated, snapshots taken where lawful |
| Review context pages | Any | Dated updates published |
| Domain: expiry, auto-renew, card, DNSSEC, registrar 2FA | Before the anniversary (2027-11-15) | Checked ([domain procedure](../procedures/register-and-configure-domain.md), section 9) |
| Support windows: Django, Python, PostgreSQL, OS | Any | Next upgrade scheduled before end of support (Django 5.2: April 2028, ADR 0010) |
| Succession envelope and escrow: still current | Any | Codes, keys and instructions checked (#33) |
| Re-read this calendar and AGENTS.md | Any | Both still true |

## Before public launch

These one-time duties are tracked as issues:

- the privacy and security review gate (#34);
- extending the domain registration to at least 5 years (ADR 0008);
- a succession arrangement (#33);
- the outside contact for moderation wellbeing and qualification ([illegal-content protocol](illegal-content.md), section 8);
- a rehearsal edition (#38).
