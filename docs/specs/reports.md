# Reports

Status: Draft (2026-11-20; proposals accepted by the owner the same day).

Issue: #41

Basis: [publishing rules](../legal/publishing-rules.md); [illegal-content protocol](../operations/illegal-content.md); [data model](data-model.md), sections 2.5 and 2.11; [threat model](threat-model.md), section 3.4; DSA arts. 16 and 17 as summarized in the [legal research](../research/legal-landscape.md), section 5; [moderation-failures research](../research/moderation-failures.md).

Anyone can report a published testimony. A report is a request for the custodian's attention, never an action in itself: no number of reports hides, edits or removes a testimony on its own. This is what prevents a person, or a script, from emptying the guestbook by reporting everything while the custodian is asleep.

## 1. Reasons

The report form asks for one reason. Each maps to a publishing rule, so that the decision cites the same code.

| Reason shown to the reporter | Rule | Priority |
| --- | --- | --- |
| Child sexual abuse material | `illegal` | Urgent |
| A threat to someone's life or safety | `threat` | Urgent |
| It exposes someone's address, contact details or other identifying information | `third-party-privacy` (doxxing) | Urgent |
| It is about me, or names me, and exposes my private life | `third-party-privacy` | High |
| Someone is publishing under my name, or under the name of a person I represent | `impersonation` | High |
| It contains a password, key or other secret | `secrets` | High |
| It makes false or damaging accusations against an identifiable person | `defamation` | Normal |
| Other illegal content: hatred, terrorism | `illegal` | Normal |
| Harassment | `harassment` | Normal |
| Spam, advertising, or not a testimony | `spam`, `advertising`, `not-testimony` | Low |
| Something else | none | Low |

A contributor who wants to change or remove their own testimony is sent to editing or withdrawal instead, which need no report.

The form asks for the reasons, the exact passage where relevant, and a statement of good faith (DSA art. 16(2)). It warns that a knowingly false report is an offence (LCEN art. 6 VII).

## 2. Who can report, and limits

1. A reporter gives an email address and confirms it through a link before the report enters the queue. This makes reports accountable and lets the custodian reply. Exception: reports of child sexual abuse material may be anonymous (DSA art. 16(2)(c)); they enter the queue at once.
2. Rate limits, like submissions (threat model, section 3.4): at most 3 confirmed reports per email address per day, and 10 per keyed IP hash per day. Proof-of-work applies as on the contribution form (ADR 0003).
3. One report per reporter per testimony. Repeats are merged into the first.
4. A reporter whose reports have repeatedly been found unfounded has later reports placed at the bottom of the queue, with the reason recorded. They are still read.
5. Counts never decide anything. Ten reports of one testimony are read as one item with ten notices, not as a vote, because counts are cheap to fake.

## 3. What a report triggers

1. A notice record is created (data model, section 2.11) and the reporter receives an automatic acknowledgement (DSA art. 16(4)).
2. The testimony enters the moderation queue at the report's priority, ahead of ordinary reviews of the same priority. Its current public revision, and any pending revisions, are reviewed against the reason given.
3. **The testimony stays up** while it is reviewed. A report does not hide it.
4. One exception, for the urgent reasons only. A confirmed report for child sexual abuse material, a threat or doxxing hides the testimony at once, as a temporary quarantine with reason `legal-hold`, until the custodian reviews it. To bound abuse:
   - at most one automatic hiding per reporter per 30 days;
   - at most 3 automatic hidings across the whole site per day; beyond that, urgent reports are queued without hiding and the custodian is alerted;
   - an automatic hiding is reversed as soon as the custodian finds the report unfounded, and the testimony returns with nothing lost.
   The worst case of mass reporting is therefore three testimonies hidden for one night, not the guestbook.
5. The custodian is alerted at once for urgent reports, and by a daily summary otherwise. A sudden rise in reports also triggers an alert, since it usually means a campaign.

## 4. Decisions and deadlines

1. Possible outcomes:
   - no action;
   - return the revision: keep the previous version, or quarantine the testimony until an edit is approved (data model, section 2.5, rule 6);
   - removal (moderator withdrawal), for content that editing cannot fix;
   - quarantine with `legal-hold` and a report to the authorities, per the [illegal-content protocol](../operations/illegal-content.md).
2. Target deadlines, published with the publishing rules: urgent reports within 24 hours, high within 3 days, normal within 7 days, low within 30 days. Statutory deadlines, such as 24 hours for a removal order from the OCLCTIC, override these targets.
3. The reporter is told the outcome and how to seek redress (DSA art. 16(5)). The contributor receives a statement of reasons when their testimony is restricted (DSA art. 17). Neither learns the other's identity.
4. Either side can ask for a review of the decision within 30 days ([publishing rules](../legal/publishing-rules.md), "Asking for a review").

## 5. Impersonation

1. A display name is given by the contributor and never verified. The methodology page, a discreet note on named testimonies ("name given by the contributor") and each edition's README say so, so that a citation cannot claim more.
2. During review, a display name that obviously belongs to a public figure or another recognizable real person is returned, asking the contributor to choose a pseudonym or anonymous mode. If the contributor says they are that person, the moderator may ask for a confirmation through a channel publicly tied to that person, such as an official site or a verified account. Ordinary names are not questioned.
3. A report from someone saying a testimony impersonates them is high priority. If the report is plausible, the testimony is quarantined with reason `awaiting-edit` while the custodian checks, rather than staying up during the dispute.
4. An impersonation found after an edition was built is removed from hosted editions by a privacy revision, as for a withdrawal.
5. Using another person's identity to harm their honour or reputation may be an offence under French law (Code pénal art. 226-4-1, recollection, to verify), and attributing invented statements to a real person may be defamatory.

## 6. Open questions

1. [x] The automatic hiding of section 3, item 4, and its caps: accepted (2026-11-20).
2. [x] The rate limits of section 2, item 2: accepted (2026-11-20).
3. [x] The target deadlines of section 4, item 2: accepted (2026-11-20).
