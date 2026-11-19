# Illegal content, threats and third-party notices: custodian protocol

Status: Draft (2026-11-15), to be validated before launch

This protocol is the custodian's procedure for content that may be illegal, threatening or harmful to a third party. It applies the [moderation principles](../constitution/moderation-principles.md) and the [threat model](../specs/threat-model.md), and it answers issue #41. It is not legal advice. Each legal assertion carries its source and its verification status. The tag `[fetched]` marks a text read in this session, `[fetched, summarised]` marks a text read through a summarising tool that must be re-read verbatim before publication, `[search]` marks a secondary source or search snippet, and `[inference]` marks reasoning. Uncertain points are written as "Uncertain:".

The Digital Services Act duties in arts. 16 to 18 are assumed to apply to the archive, because the micro and small enterprise exemption in art. 19(1) reaches only Section 3 of the Regulation [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065). Whether the archive is an information society service at all is uncertain; see the [legal landscape research](../research/legal-landscape.md), section 5.

## 1. Principles

1. Report, do not investigate. The custodian stops publication, keeps what the authorities need without copying it, and reports [inference](../research/moderation-failures.md).
2. Use the least intrusive action first: return the testimony to its contributor to remove a third party's identifier rather than remove the testimony, unless the whole testimony is unlawful ([moderation principles](../constitution/moderation-principles.md), practice 2). Returning either restores the previous version or, when the approved text itself is at fault, quarantines the testimony until an edit is approved ([data model](../specs/data-model.md), section 2.5, rules 5 and 6).
3. View the minimum. Decide suspected child sexual abuse material from text and metadata; never open a file that may be such material ([inference](../research/moderation-failures.md), section 2.4).
4. Do not delete suspected illegal material as a first step; quarantine it. The hotline's guide for hosts says the same ([fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le traitement"). Deletion may also fall under Code pénal art. 434-4 ([search](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006418608/2021-08-26)).
5. Never let one person carry a suspected child abuse case alone (section 8).

## 2. Triage for every flagged item

1. Record the item identifier and the time of receipt in UTC in the private moderation record.
2. Assign one scenario: suspected child sexual abuse material (section 3.1), threat to life or safety (section 3.2), other manifestly illegal content (section 3.3), doxxing (section 3.4), or notice from a third party (section 3.5). If in doubt, use the more serious scenario first.
3. Set the item to quarantine: not published, not visible to anyone else, not previewed, and not deleted ([fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le traitement").
4. Do not screenshot, copy, print, forward or paste any part of the item into any other tool, including AI services. Unpublished testimonies are never sent to external services ([threat model](../specs/threat-model.md), section 3.6).
5. If the scenario is still unclear after triage, consult the hotline (section 5) before deciding. If a life may be at risk, call 17 or 112 first.
6. Edits to published testimonies go live before review ([data model](../specs/data-model.md), section 2.5). A flagged testimony with unreviewed edits is reviewed first, from the word diff against its last reviewed revision. Quarantine freezes the testimony with that revision and the current one, so that neither is deleted while the item is handled. Whether review after publication fits the director-of-publication regime of loi 82-652 art. 93-3, which this protocol cites from recollection only, is an open item (section 10).

## 3. Procedures

### 3.1 Suspected child sexual abuse material

1. Do not open any attached or linked image, video or file. Decide from the text and metadata. Treat the item as suspected child sexual abuse material if the text describes sexual conduct involving a minor, or an image or representation of a person who appears to be a minor. Uncertain: the reach of the offence to text is the hotline guide's reading of the law, not a court decision ([fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le traitement"; [inference](../research/moderation-failures.md), section 4.5).
2. Do not download, copy, screenshot, print, forward or send the item, even to a second person. Code pénal art. 227-23 punishes fixing, recording, transmitting, offering, distributing, acquiring and possessing such images ([fetched, summarised](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043409170)). The current penalty is five years and EUR 75,000 for the transmission and possession offences. The article has no exemption for people who handle such images for reporting ([fetched, summarised](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043409170)).
3. Quarantine the item and suspend the associated account. Do not delete the item or the account data. The hotline guide treats suspension as a technical operation and advises against deletion ([fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le traitement").
4. Record the metadata listed in section 4 and nothing else.
5. Report without delay to Point de Contact, which accepts child sexual exploitation reports ([fetched](https://www.pointdecontact.net/)), using the form at <https://www.pointdecontact.net/signaler/> ([fetched](https://www.pointdecontact.net/)). Give the item identifier, the time, and the public address if there is one, and say that the content was not viewed. Uncertain: whether a report made without viewing is accepted. Ask at first contact.
6. Ask the hotline or PHAROS how to preserve the stored item without keeping a copy beyond the quarantine. Until they answer, keep it quarantined and reachable only by the custodian. Uncertain: the sources read do not say how a host must hold an item it may neither view nor copy nor delete. This is the most urgent open point ([inference](../research/moderation-failures.md), section 4.7).
7. If the content suggests a child is at risk now, also follow section 3.2 at once.
8. Record the reference number given by the authority, the date, and the decision. Do not inform the contributor before section 7 has been applied.
9. Keep the identification data that the law requires separately from the content, for the period the decree sets, if the decree applies. Uncertain: the decree's applicability to the operator is open ([legal landscape research](../research/legal-landscape.md), section 6; the legal basis is LCEN art. 6 V A, [fetched, summarised](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000801164)).
10. Arrange the wellbeing step in section 8 the same day.

### 3.2 Threat to life or safety

1. If the danger appears immediate, for example an attack announced now, a suicide in progress, or a child at risk now, call 17 (police) or 112 first. Do not wait for an online report to be processed. The police page says to call 17 for emergencies ([fetched](https://www.police-nationale.interieur.gouv.fr/actualite/contenus-illicites-sur-internet-comment-fonctionne-portail-officiel-pharos)). The European number 112 is free and available around the clock from a landline or mobile ([fetched](https://lannuaire.service-public.gouv.fr/centres-contact/R12069)).
2. Quarantine the item. Give the authority the item identifier, the time, the public address if any, and the account identifier held for the contributor. Nothing else.
3. Inform the law enforcement authority promptly, as art. 18(1) of the Digital Services Act requires where a hosting provider becomes aware of information suggesting a criminal offence involving a threat to life or safety ([fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065)). PHAROS lists "endangering people", including imminent threats to life and suicide announcements, among its categories ([fetched](https://www.police-nationale.interieur.gouv.fr/actualite/contenus-illicites-sur-internet-comment-fonctionne-portail-officiel-pharos)). Record the reference.
4. If the Member State cannot be identified, art. 18(2) allows notice to law enforcement in the Member State of the provider's legal representative, or to Europol ([fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065)). For a French operator the French police or gendarmerie are the relevant authority [inference].
5. Failure to report a crime that can still be limited may be an offence under Code pénal art. 434-1, which exempts family members (unless the crime is against a minor) and people bound by professional secrecy ([search](https://www.autonome-solidarite.fr/articles/la-non-denonciation-de-crimes-et-delits/)). Uncertain: read the Legifrance text before relying on this. Failure to help a person in peril is an offence under Code pénal art. 223-6 ([search](https://kohenavocats.com/non-assistance-personne-en-danger-elements-constitutifs-peines-defense/)); the text is not read on Legifrance.
6. Do not contact the person at risk, or the contributor, about the report unless the authority agrees [inference].
7. Keep the item quarantined. Do not delete it.
8. Apply section 7 on the contributor; the authority may ask for a delay.

### 3.3 Other manifestly illegal content (incitement, hate speech under French law)

1. Decide whether the content is manifestly illegal or merely offensive, disagreeable or mistaken. Offensive or mistaken views are not moderated ([moderation principles](../constitution/moderation-principles.md), "Limits").
2. Hate speech: provoking discrimination, hatred or violence against a person or group because of origin, ethnicity, nation, race or religion carries one year's imprisonment and/or EUR 45,000 under the seventh alinea of article 24 of the Loi du 29 juillet 1881 ([fetched, summarised](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000043982456)). Other grounds sit in other alineas, which were not read.
3. Apology of terrorism is listed in LCEN art. 6 IV A, which cites Code pénal art. 421-2-5 ([fetched, summarised](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049577522)). The text of art. 421-2-5 was not read.
4. If the case is not clear, consult a lawyer or Point de Contact, which offers orientation in doubt ([fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le signalement"). Keep the item in quarantine meanwhile.
5. If the content is manifestly illegal, remove it. If only one passage is unlawful, return the testimony with the rule and guidance, restoring the previous version if that one is lawful, or quarantining the testimony until an edit is approved, and record the decision and its reason ([moderation principles](../constitution/moderation-principles.md), practice 2).
6. Report to PHAROS, whose categories include incitement to hatred and terrorism ([fetched](https://www.police-nationale.interieur.gouv.fr/actualite/contenus-illicites-sur-internet-comment-fonctionne-portail-officiel-pharos)), or to Point de Contact, which accepts hate speech and terrorist content ([fetched](https://www.pointdecontact.net/)). Give the item identifier and the passage concerned, not the whole text.
7. Send the contributor the statement of reasons described in section 7.
8. For a repeated violation, suspend the account under the published rules ([moderation principles](../constitution/moderation-principles.md), practice 1).
9. Record the decision, the rule relied on, the decider and the date.

### 3.4 Doxxing of a third party

1. Identify the third-party data: a name with an address, workplace, telephone number, email address, photograph, account or other detail that identifies or locates a person ([threat model](../specs/threat-model.md), section 3.3).
2. If the disclosure is meant to expose the person, or their family, to a direct risk of harm, it may be an offence under Code pénal art. 223-1-1 ([fetched, summarised](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043974282)). If there is an immediate threat, follow section 3.2. If not, report to PHAROS, which lists "endangering people" and threats among its categories ([fetched](https://www.police-nationale.interieur.gouv.fr/actualite/contenus-illicites-sur-internet-comment-fonctionne-portail-officiel-pharos)).
3. Where there is no direct risk, return the testimony with guidance to remove the identifiers, as the least intrusive action. If the identifiers are in the approved text, the testimony is quarantined until an edit is approved. Record the decision and its reason, without copying the identifiers ([moderation principles](../constitution/moderation-principles.md), practice 2).
4. A private dispute between individuals, such as insults or harassment, goes to the local police station or gendarmerie rather than to PHAROS ([search](https://www.police-nationale.interieur.gouv.fr/actualite/contenus-illicites-sur-internet-comment-fonctionne-portail-officiel-pharos)).
5. Do not inform the third party by default. If they contact the custodian, handle the message as a notice under section 3.5.
6. Do not disclose the contributor's identity or the removed text to anyone.

### 3.5 Notice received from a third party

1. Acknowledge receipt promptly if the notifier gave an email address ([fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065), DSA art. 16(4)).
2. Check the notice against DSA art. 16(2): the reasons why the content is illegal, its exact location (a URL or testimony identifier), the notifier's name and email, and a statement of bona fide belief. The name requirement does not apply to certain child-abuse offences listed in Directive 2011/93/EU ([fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065)). If an element is missing, ask for it [inference].
3. If the notice describes child sexual abuse material, a threat or doxxing, follow section 3.1, 3.2 or 3.4 before looking at the item. Forward the text of the notice, not the content, to PHAROS or Point de Contact [inference].
4. Do not quarantine an item merely because a notice arrived: a notice alone never hides a testimony ([reports](../specs/reports.md), section 3). Quarantine it once triage under section 2 finds the scenario plausible, or when the capped automatic hiding for urgent reasons has already done so. Do not delete it.
5. Decide promptly, in a timely, diligent, non-arbitrary and objective manner, and record the rule relied on ([fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065), DSA art. 16(6)).
6. Tell the notifier the decision and the redress options promptly ([fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065), DSA art. 16(5)). Share only what the notifier needs; the contributor's identity stays private [inference].
7. Apply section 7 to the contributor.
8. A knowingly false notice, made to obtain removal, is punishable under LCEN art. 6 VII ([fetched, summarised](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000801164)). Record it; do not act on it without a check.
9. A removal request from the OCLCTIC for child sexual abuse images must be complied with within 24 hours under LCEN art. 6-1 I ([fetched, summarised](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000801164)). Uncertain: the criminal penalty for missing that deadline is reported in secondary sources that disagree ([search](https://cms.law/fr/fra/news-information/censure-partielle-de-la-proposition-de-loi-sur-les-contenus-haineux-sur-internet)). Treat the deadline as binding.

## 4. What to record, and what never to keep

What to record, in the private moderation record ([moderation principles](../constitution/moderation-principles.md), practice 4):

- the item identifier, the time of receipt in UTC, and the scenario;
- the rule number or legal basis relied on, the decider, the decision time, and the action taken (quarantine, return, return with quarantine, removal, account suspension);
- for a notice: the notifier type (anonymous or named), the notice identifier, the acknowledgement date and the decision date;
- for a report: the recipient, the date, the reference number and the name of any contact;
- for the contributor: whether they were informed, when, with which template, or why the message was withheld (section 7);
- the identification data that LCEN art. 6 V A may require, kept apart from the content (section 3.1, step 9).

What never to keep:

- any image, video or file suspected to be child sexual abuse material, or any copy, screenshot, print, download or extract of it;
- any copy of suspected illegal content sent outside the custodian;
- notes that reproduce suspected child abuse material or describe it beyond what the report needs;
- hashes or fingerprints of suspected child abuse material, unless the authority asks for them [inference];
- identity documents of the contributor or the notifier;
- third-party identifiers beyond what the report needs, once the case is closed (the period belongs in the retention schedule, issue #18);
- testimony text, emails or full IP addresses in application logs ([threat model](../specs/threat-model.md), section 3.6).

## 5. Whom to report to

| Recipient | Use it for | Address | Verification |
| --- | --- | --- | --- |
| Police or gendarmerie, emergency | Immediate danger to life or safety | Call 17 (police) or 112 (European emergency number) | 17 [fetched](https://www.police-nationale.interieur.gouv.fr/actualite/contenus-illicites-sur-internet-comment-fonctionne-portail-officiel-pharos); 112 [fetched](https://lannuaire.service-public.gouv.fr/centres-contact/R12069) |
| PHAROS, run by the OCLCTIC | Child sexual abuse, threats, endangering people, incitement, hate, terrorism, doxxing with a direct risk | Current address to be verified. The 2014 hotline guide gives internet-signalement.gouv.fr. The police page says the platform is reached through the Ma Sécurité site | Address not confirmed on 2026-11-15: the portal returned an empty response. Platform described [fetched](https://www.police-nationale.interieur.gouv.fr/actualite/contenus-illicites-sur-internet-comment-fonctionne-portail-officiel-pharos) |
| Point de Contact, run by the AFA | Child sexual exploitation, hate speech, terrorist content, orientation in doubt | <https://www.pointdecontact.net/signaler/> | [fetched](https://www.pointdecontact.net/); member of INHOPE [fetched](https://www.pointdecontact.net/) |
| INHOPE | Information on the hotline network; not a reporting route for the custodian | <https://www.inhope.org/EN> | [fetched](https://www.inhope.org/EN) |
| CNIL, personal data breach notification | Breach of personal data within 72 hours | <https://notifications.cnil.fr/notifications/> | [fetched](https://www.cnil.fr/fr/services-en-ligne/notifier-une-violation-de-donnees-personnelles) |
| Local police or gendarmerie station | Private disputes between individuals | Local station | [search](https://www.police-nationale.interieur.gouv.fr/actualite/contenus-illicites-sur-internet-comment-fonctionne-portail-officiel-pharos) |
| Hosting provider abuse contact | Hosting-level abuse and outages | To be entered from the hosting provider's contract | [inference](../research/moderation-failures.md), section 2.1 |
| Registrar abuse desk (OVHcloud) | Reports the registrar forwards about the domain. They must be answered quickly: an unanswered report can lead to the suspension of the domain, as happened to a Mastodon instance | Reports arrive at the registrar account's notification address ([domain record](domain.md)). That address must be read at least daily. | [inference](../research/moderation-failures.md) |

## 6. Deadlines

| Obligation | Deadline | Source |
| --- | --- | --- |
| Acknowledge a notice that gives contact details | Promptly | [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065), DSA art. 16(4) |
| Tell the notifier the decision and the redress options | Promptly | [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065), DSA art. 16(5) |
| Give the contributor a statement of reasons | No later than when the restriction takes effect | [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065), DSA art. 17(2) |
| Inform law enforcement of a suspected threat to life or safety | Promptly | [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065), DSA art. 18(1) |
| Inform the competent authorities of reported listed offences | Promptly | [fetched, summarised](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049577522), LCEN art. 6 IV A |
| Remove child sexual abuse images on an OCLCTIC request | 24 hours | [fetched, summarised](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000801164), LCEN art. 6-1 I |
| Answer a data subject request, such as withdrawal or erasure | One month, extendable by two months with reasons | [fetched](https://gdpr-info.eu/art-12-gdpr/), GDPR art. 12(3) |
| Notify a personal data breach to the supervisory authority | 72 hours where feasible | [fetched](https://gdpr-info.eu/art-33-gdpr/), GDPR art. 33(1) |
| Appeal window offered to contributors | 30 days, proposed | Mastodon practice, [fetched](https://help.joinmastodon.org/article/20-moderation-decisions-and-appeals); the choice is a design decision [inference] |
| Report to the hotline | Immediately after qualification | [fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le traitement" |

## 7. Informing the contributor, and when not to

By default, tell the contributor the outcome and the rule applied, with a statement of reasons ([moderation principles](../constitution/moderation-principles.md), practice 5; [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065), DSA art. 17(1) and (3)). The statement must give the facts relied on, the scope and duration, the legal or contractual basis, and the redress available.

Hold the message, and consult the authority, in these cases:

- suspected child sexual abuse material: do not describe the content, and do not say more than the neutral wording [inference];
- a threat or danger where the authority asks for discretion [inference];
- where the message would reveal a third party's personal data, such as the identity of the person doxxed [inference];
- where an anonymous notifier's identity could be exposed through the reply [inference].

Uncertain: DSA art. 17 contains no exception for these cases, except for orders under its art. 9, which art. 17(5) excludes ([fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065)). The custodian cannot settle this alone. The neutral wording below is a stopgap until the lawyer and the authority have answered (section 10, item 5).

Draft neutral wording, to be reviewed: "Your testimony has not been published because it contains content that may be unlawful under French law. You may ask for a review within 30 days by replying to this message."

## 8. The custodian's wellbeing

1. View the minimum. Decide from text and metadata, and never open suspected child abuse media. Where media exists, use blurring or grayscale by default, as the Stanford report recommends ([fetched](https://stacks.stanford.edu/file/druid:vb515nd6874/20230724-fediverse-csam-report.pdf), section 5.3).
2. Work the queue in fixed sessions with breaks. Do not review flagged material late at night or just before sleep [inference].
3. Do not carry a suspected child abuse case alone. The hotline guide says such work should not fall to one person and that employees should be able to consult a psychologist free of charge ([fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Vos contacts"). For a sole custodian, arrange before launch a confidential outside contact and a professional who can be consulted. Done (2026-11-20): the custodian has arranged one; its details are personal and kept outside the repository.
4. Qualification help: where in doubt, use the Point de Contact orientation ([fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le signalement").
5. After a severe exposure, stop the session, write a short note, and do not return to the queue that day [inference].
6. Decline a case that cannot be assessed without viewing the material. Reporting it is the answer, not viewing it ([inference](../research/moderation-failures.md), section 2.4).

The harm is documented. Gonzalez and Matias list anxiety, nightmares, fatigue and intrusive images among the reported symptoms ([fetched](https://arxiv.org/html/2502.00244)). A claim by more than 140 Kenyan content moderators reports PTSD diagnoses ([search](https://www.business-humanrights.org/en/latest-news/kenya-content-moderators-filed-a-lawsuit-against-meta-alleging-poor-working-conditions-including-insufficient-mental-health-support-and-low-pay/)).

## 9. Related documents

- [Moderation principles](../constitution/moderation-principles.md)
- [Threat model](../specs/threat-model.md), sections 3.3 and 3.6
- [ADR 0003, email magic-link authentication](../decisions/0003-email-magic-link-auth.md), for pending caps and bulk tools
- [Legal landscape research](../research/legal-landscape.md), sections 5 and 6
- [Moderation failures research](../research/moderation-failures.md)

## 10. Open items to validate before launch

1. Lawyer: the legal basis for holding a stored suspected child abuse item under the authority's instruction, and whether a report can be made without viewing (sections 3.1, steps 5 and 6). This is the most urgent item.
2. Point de Contact and PHAROS: the accepted report route, the current PHAROS address, and whether a report without viewing is accepted (section 5).
3. Legifrance: confirm the verbatim text of LCEN art. 6 IV A and art. 6-1, including the penalty status of art. 6-1 (sections 3.5 and 6).
4. Legifrance: confirm the scope of Code pénal arts. 223-6, 434-1, 434-3 and 434-4 (sections 3.1 and 3.2).
5. Lawyer: the tipping-off question under DSA art. 17 (section 7).
6. Lawyer: whether decree 2021-1362 applies to the operator, and so whether identification data must be kept (section 3.1, step 9).
7. Resolved (2026-11-20): the confidential outside contact for wellbeing is arranged, with its details kept outside the repository; qualification help comes from Point de Contact (section 8, items 3 and 4).
8. Read the current Point de Contact terms before adding any link to its form ([fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le signalement").
9. Re-read every [fetched, summarised] text verbatim on Legifrance or EUR-Lex before publication.
10. Lawyer: whether publishing edits to approved testimonies before review is compatible with the operator's position as director of publication (loi no. 82-652, art. 93-3, on contributions not reviewed before publication; cited from recollection, to verify), and with the hosting regime of DSA art. 6 (section 2, step 6).
