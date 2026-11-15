# The Artificial Intelligence Guestbook - Legal landscape research

Date: 2026-11-15
Scope: GDPR, French data protection law, LCEN, DSA, copyright, minors, retention, transfers, self-review checklist for a pre-launch review.

## Disclaimer

This document is research to support a self-review. It is not legal advice. It does not replace review by a qualified French lawyer, and several points below are explicitly marked as uncertain. Article numbers were checked against primary text where the status legend says so. Summaries of legal texts obtained through a summarising fetch tool were re-read at the level of article number and key wording only; verbatim quotations should be re-checked on Legifrance or EUR-Lex before they are reproduced in public documents.

## Verification status legend

Each source is tagged with one of these markers:

- [F] Fetched in this session from the primary source (Legifrance, EUR-Lex, CNIL, Creative Commons, Cornell LII). Wording was read through a summarising fetch, so re-check verbatim text before publishing it.
- [S] Secondary source only (law firm commentary, blog, search snippet). Use as a lead, not as authority.
- [N] Not read in this session. Cited from knowledge of the instrument; the article number should be verified before reliance.

## Executive summary: decisions this research implies

1. The operator is the controller for all contributor data and, at the same time, a "publisher" (editeur) under LCEN art. 1-1 I and very probably a "hosting provider" for entries stored on its own VPS. The public mentions legales must carry the operator's identity (for a natural person: name, first names, domicile and phone number under art. 1-1 I 1, unless the art. 1-1 II route for non-professional publishers is used), the director of publication (art. 1-1 I 3) and the hosting provider's name, address and phone (art. 1-1 I 4). The domicile point is a real design decision: publishing a home address is in tension with the privacy goals of the project. [F, see section 1]

2. The LCEN was rewritten by the SREN law. Publisher identification now sits in art. 1-1, the penalties in art. 1-2, and the duty to keep identification data for contributors in art. 6 V A (formerly art. 6 II). The decree 2021-1362 still cites "II de l'article 6" and has not been updated in its own text as far as was read. [F]

3. Retention is not only a design choice. If the operator is covered by the decree 2021-1362 (uncertain, see section 6), it must keep account identifiers for one year after the account ends (art. 3), civil identity data for five years where collected (art. 2), and connection data including IP addresses at content creation for one year (art. 5). Erasure requests can then be refused for those data during those periods (GDPR art. 17(3)(b), [N]). The privacy notice must say so, and the architecture should collect only what is needed (decree art. 8 limits the duty to data actually collected). [F/S]

4. The lawful basis set should be: contract or consent for the account, explicit consent (GDPR art. 9(2)(a)) for the testimony and for any voluntarily disclosed special-category content, consent for optional metadata, legitimate interest or legal obligation for moderation and security records, and minimal legal-obligation or legitimate-interest records for withdrawal. Article 6(1)(e) and Article 89 are not available as a basis for a private individual without a legal mandate. [F for art. 6(3) structure, art. 89 text; reasoning in section 2]

5. Because the lawful basis for publication is consent, GDPR art. 8 is engaged where a child is "offered directly" the service (art. 8(1) applies "where point (a) of Article 6(1) applies"). Plan for the French threshold of 15 with joint parental consent below 15 (Loi Informatique et Libertes art. 45, per CNIL Recommendation 4). Entries from under-15s need a separate flow, and age ranges of minors should not be published. [F]

6. Special category data: explicit consent under art. 9(2)(a) is the defensible route. Do not rely on art. 9(2)(e) ("manifestly made public by the data subject") as the main ground; the CJEU reads indirect revelation broadly (C-184/20, paras 123 and 128 [F]), and the exact content of 9(2)(e) has not been resolved from the judgment text in this session. Moderation must also handle third-party special-category data, which no contributor consent can cover.

7. A DPIA is very likely required or at least strongly advisable. The CNIL list of processing requiring a DPIA (deliberation 2018-327) does not name this case, but its criteria (sensitive data, vulnerable persons) are present, and the list is expressly non-exhaustive. Art. 30(5) (the fewer-than-250 exemption from the record of processing) does not apply because the processing includes special-category data. [F]

8. Withdrawal cannot recall copies already downloaded by third parties. The design must say so honestly, use a machine-readable withdrawal list, revise future editions, and leave tombstones with no personal data. CC BY 4.0 is irrevocable as to licensees (section 11), so the licence and the GDPR withdrawal operate on different axes; the terms should say which is which.

9. Copyright: the project needs an express, written, scoped grant from each contributor (CPI art. L131-3 formalism [S]) covering hosting, display, search, translation, redaction (integrity right, CPI art. L121-1 [S]), archival editions and redistribution. The grant can be paired with CC BY 4.0 for public reuse. Fully AI-generated text may not attract copyright at all (open question).

10. The EU/US transfer and CLOUD Act exposure is manageable only with EU-based processors, DPAs under art. 28(3), and a list of sub-processors. The EU-US Data Privacy Framework covers only certified organisations (Decision 2023/1795, art. 1 [F]).

11. If the service is a "hosting service" under the DSA, art. 16 (notice and action) and art. 17 (statement of reasons) apply to it even if it is micro or small. Art. 19 (micro and small enterprises exemption) only excludes the platform-specific Section 3 (arts. 20 to 28, including minors' protection at art. 28). The LCEN publisher and host duties apply in parallel. [F]

12. Whether the project is an "information society service" at all depends on whether it is provided for remuneration or as an economic activity (directive 2015/1535 art. 1(1)(b) [F]; directive 2000/31 recital 18 [F]). A free, non-commercial archive is arguably outside the definition. This is uncertain; the conservative assumption is that the DSA and LCEN hosting rules apply.

## 1. Roles: controller, publisher, host

### What the law says

GDPR controller (art. 4(7)) is the body that determines purposes and means of processing [N].

Under the LCEN as amended by the SREN law (loi no. 2024-449 of 21 May 2024), the consolidated text on Legifrance reads as follows [F]:

- Art. 1-1 I: persons whose activity is to publish an online communication service must make available to the public, in an open standard: (1) for natural persons, name, first names, domicile and phone number (and the commercial register number where registered); (2) for legal persons, name or corporate name, registered office and phone number; (3) the name of the director or co-director of publication within the meaning of art. 93-2 of loi no. 82-652 of 29 July 1982, and the editor-in-chief where applicable; (4) the name or corporate name, address and phone number of the hosting provider; (5) where applicable, the name and address of any person who stores data processed directly by the publisher, even free of charge. [F]
- Art. 1-1 II: a non-professional publisher may keep its identity private. It must only make available the host's name and address, provided it has already given its identification details to that host. Hosts are bound by professional secrecy under arts. 226-13 and 226-14 of the Code penal. [F]
- Art. 1-2: failure to comply with art. 1-1 I and II is punishable by one year's imprisonment and a EUR 75,000 fine for individuals (and corporate-liability rules apply). [F, from a summary; verify]
- Art. 6 I 2: a hosting provider is a person providing the services defined in DSA art. 3(g)(iii). Art. 6 I 3 refers to search engines by reference to DSA art. 3(j). [F]
- Art. 6 II: intermediary service providers within DSA art. 3(g) are not "producteurs" under art. 93-3 of loi no. 82-652. [F]
- Art. 6 IV B: hosts must give publishers the technical means to meet the art. 1-1 I identification requirements. [F]
- Art. 6 V A: access and hosting providers must hold data allowing the identification of anyone who contributed to the creation of content, under conditions set by a Conseil d'Etat decree adopted after CNIL opinion, under the regime of CPCE art. L34-1. Art. 6 V B makes failure punishable by one year's imprisonment and EUR 250,000. [F]

Directive 2000/31 recital 18 and the DSA definitions are discussed in section 5.

On the editorial/hosting line, the CJEU in C-291/13 Papasavvas (14 September 2014, ECLI:EU:C:2014:2209) held that the hosting safe harbour does not protect a publisher that knows and controls the content it posts, even where access is free. The secondary summary used here was not checked against the judgment text. [S]

### Application to the Guestbook

- The operator is the controller for: accounts, testimonies, optional metadata, moderation records, withdrawal records and logs. That is the default position and should be stated in the privacy notice.
- The operator is a publisher. Its public website is an online communication service. It must publish the art. 1-1 I identifiers. The publisher is named publicly (plan section 4 and 5 and the operator's name), so the art. 1-1 II anonymity route is not used by default.
- For a natural person, art. 1-1 I 1 requires the domicile and the phone number to be made available. Publishing a home address conflicts with the privacy goals in plan sections 4, 20 and 26. An alternative is the art. 1-1 II route (only the host's identity is published, provided the operator gave its identity to the host). Whether the operator can publicly name itself (as the plan proposes) while using a domiciliation address, or must publish the home domicile, is not settled in the sources read. It is the most important open question in this section.
- Director of publication: the operator must be named as director of publication (art. 1-1 I 3).
- Host: the VPS provider's name, address and phone must be published (art. 1-1 I 4). If the email provider or the backup provider stores data processed directly by the operator, art. 1-1 I 5 may require their name and address too (uncertain; see open questions).
- Hosting role: the operator stores contributor-supplied content before and after moderation. Under DSA art. 3(g)(iii) and LCEN art. 6 I 2, it is likely to be a hosting provider for those entries. Pre-publication moderation and editorial selection push the position toward publisher and weaken any hosting safe harbour for the published text (Papasavvas, secondary). The position should be documented, and the operator should comply with both sets of duties.
- The operator should not describe the archive as a "social network" or "platform" in its mentions legales unless it accepts the platform analysis (section 5).

### Open questions

- Does art. 1-1 I 1 require the domicile of a natural person who voluntarily publishes its name, or can it be satisfied by art. 1-1 II alone? [uncertain, not resolved in the sources read]
- Can a domiciliation or post-office address serve as "domicile" for art. 1-1 I 1? [uncertain]
- Does the email provider or backup provider count as a person storing data "processed directly" by the publisher (art. 1-1 I 5)? [uncertain]
- Does a non-professional publisher with a hosting role need the decree 2021-1362 retention regime (section 6)? [uncertain]

### Follow-up, 2026-11-15: no domicile under the art. 1-1 II route

Requested by the owner, who recalled that no physical address is needed.

- Current text of art. 1-1 II, as quoted from Legifrance in search results: "Les personnes éditant à titre non professionnel un service de communication au public en ligne peuvent ne tenir à la disposition du public, pour préserver leur anonymat, que le nom, la dénomination ou la raison sociale et l'adresse du fournisseur de services d'hébergement, sous réserve d'avoir communiqué à ce fournisseur les éléments d'identification personnelle mentionnés au I du présent article." [S, quotation of the Legifrance text; Legifrance chapter page: https://www.legifrance.gouv.fr/codes/section_lc/JORFTEXT000000801164/LEGISCTA000006117684/]
- A lawyer's guide confirms the route, says the identification data "ne peuvent être divulguées que sur réquisition de l'autorité judiciaire", and proposes this wording: "ce site est édité à titre non professionnel par un particulier qui a communiqué à son hébergeur l'ensemble de ses éléments d'identification personnelle", followed by the host's name, address and phone number [S, https://www.simonnetavocat.fr/mentions-legales-dun-site-internet-obligations-sanctions-et-modele/].
- The same section of the LCEN provides that, when a non-professional publisher stayed anonymous, a right-of-reply request goes to the host, which forwards it [S, same Legifrance quotation].
- Practical guides agree that the route is closed to professionals, including micro-entrepreneurs, and some argue that advertising, affiliate links or any commercial activity makes a site professional. That second point is a guide's interpretation, not the text [S].

Conclusion: the owner's recollection is correct for a non-professional publisher. The mentions légales can carry the art. 1-1 II statement and the host's details, with no domicile and no personal phone number. The Guestbook qualifies as long as it stays non-commercial: no ads, no affiliate links, no paid services. Whether donations would change this was not researched.

Remaining uncertainty [inference]: no source discusses a non-professional publisher who uses the art. 1-1 II route for the mentions légales and also names themselves voluntarily elsewhere on the site, for example on the About page. The text grants a permission ("peuvent ne tenir à la disposition du public ... que"), not a prohibition on saying more. "Pour préserver leur anonymat" states a purpose, not a condition. Naming oneself voluntarily therefore looks compatible, but no authority confirming this was found.

## 2. GDPR legal bases

### What the law says

- Art. 6(1) lists the bases (a) consent, (b) contract, (c) legal obligation, (e) public task, (f) legitimate interest [F for 6(1)(e) and (f) first lines; (a), (b), (c) and the rest N].
- Art. 6(3), first sentence: the basis for processing under points (c) and (e) must be laid down by Union or Member State law [F].
- Art. 7(3), first sentence: the data subject has the right to withdraw consent at any time [F]. The second sentence (withdrawal does not affect prior lawfulness) is N.
- Art. 5(1)(e): personal data kept in identifiable form no longer than necessary [F, truncated text].
- Art. 89(1): processing for archiving purposes in the public interest, scientific or historical research, or statistical purposes is subject to appropriate safeguards, which may include pseudonymisation [F]. Art. 89 is a set of safeguards; it is not itself a lawful basis.
- Art. 85(1)-(2): member states must reconcile data protection with freedom of expression, including journalistic, academic, artistic or literary expression, by law [F].
- Loi no. 78-17 (Loi Informatique et Libertes) art. 80 implements art. 85 [F]. Its heading covers "journalisme et expression litteraire et artistique". Art. 80 1 covers "expression universitaire, artistique ou litteraire" (not limited to professionals). Art. 80 2 covers journalistic activity "a titre professionnel" (professional journalism only) [F].
- Loi I&L art. 4 point 5 (storage limitation with archival exception for public-interest archiving) [F, from a summary of the page]. Art. 36 of the same law is about the CNIL's public register, not archives [F].

### Application to the Guestbook

Recommended mapping (for the self-review; each row to be confirmed by the DPIA):

| Data | Recommended basis | Notes |
|---|---|---|
| Account and email (login by magic link) | Art. 6(1)(b) for the account the user asks for, or art. 6(1)(f) for account security | Email is needed to authenticate and to process withdrawal. Art. 6(1)(b) is arguable only if the account is objectively necessary to provide the requested service [N for EDPB 2/2019 reasoning]. Consent is not appropriate for a login the user cannot avoid. |
| Testimony text (publication) | Art. 6(1)(a) consent plus art. 9(2)(a) explicit consent where special categories are present | Consent is the only basis that fits withdrawal. Legitimate interest for publication is weak once the text is archived and mirrored. |
| Optional public metadata (name, age range, country, region, language, profession, organisation, relationship to AI, link) | Art. 6(1)(a) consent | Each field optional. Withdraw one field without withdrawing the whole entry where practicable. |
| Moderation records | Art. 6(1)(f) legitimate interest; art. 6(1)(c) where LCEN or DSA duties apply | Moderation records for illegal content may be legal obligations under the DSA notice and action and statement-of-reasons framework (section 5). |
| Withdrawal records | Art. 6(1)(c) (demonstrating compliance) or art. 6(1)(f) | Keep the minimum: a request date and a non-reversible identifier, not the content. |
| Security and server logs | Art. 6(1)(f) (security of processing, GDPR art. 32 [N]) and art. 6(1)(c) where decree 2021-1362 applies | See section 6 for the decree's retention periods. |
| Email delivery logs | Art. 6(1)(f) | Keep short. |

Art. 6(1)(e) and Art. 89 are not a basis for this operator. A public task must be laid down by law (art. 6(3) [F]). No legal mandate names a private guestbook as a public archive. Public-interest archiving under art. 89 is a safeguard, and invoking it is not a substitute for a basis. A private individual should treat its archive as a voluntary service, and the archival editions as a consent-based and legitimate-interest publication.

Loi I&L art. 80 and GDPR art. 85 may support the expression interest in a balancing exercise (for example in the erasure analysis, where art. 17(3)(a) allows refusal to erase data needed for freedom of expression [F]). Art. 80 1 "expression litteraire" could arguably cover testimony, but this is untested, and it is not a basis for processing on its own. Art. 80 2 does not apply, since the operator is not a professional journalist.

Consent must satisfy art. 7 and be freely given, specific, informed and unambiguous. The EDPB consent guidelines (05/2020) say explicit consent requires an express statement [N, EDPB guidelines not fetched].

### Open questions

- Is account creation a contract in the sense of art. 6(1)(b), or should it be treated as consent? [uncertain]
- Does a "private individual running a public archive" have any legal mandate under art. 6(1)(e)? Our reading: no. Confirm.
- How should the archival editions be justified after withdrawal (consent, legitimate interest, or art. 17(3)(d) for archiving with art. 89 safeguards)? [uncertain; see section 10]
- Does art. 80 1 Loi I&L cover a testimony platform? [uncertain, untested]

## 3. Special-category data (art. 9)

### What the law says

- Art. 9(1) prohibits processing of data concerning health, beliefs, sexual life, and similar categories, subject to exceptions [N for 9(1) wording; the categories as listed in Loi I&L art. 6 I are F from a summary].
- Art. 9(2)(a): the data subject has given explicit consent for one or more specified purposes, except where Union or member state law provides that the prohibition may not be lifted by the data subject [F].
- Art. 9(2)(e): processing relates to personal data which are manifestly made public by the data subject [F].
- CJEU C-184/20 (OT v Vyriausioji tarnybines etikos komisija, 1 August 2022, Grand Chamber): data that indirectly reveals sensitive information (through deduction or cross-referencing) is special-category data (paras 123 and 126-127), and publication of data liable to disclose indirectly a person's sexual orientation constitutes processing of special categories (para 128 and operative point 2) [F, through summarised reading]. The paragraphs on 9(2)(e) were not located in the portion read (the summary read paras 1-108 and the text after 117); the phrase "manifestly made public" was not found in the portion read [F, partial].
- Loi I&L art. 6 I lists the special categories in French law (racial or ethnic origin, political opinions, religious or philosophical beliefs, union membership, genetic or biometric data, health, sex life or sexual orientation) and art. 6 II refers the exceptions to GDPR art. 9(2) and to the law [F, summary].

### Application to the Guestbook

- Explicit consent (9(2)(a)) is the defensible route for the testimony and any metadata that is special-category data (for example a religion, health condition, political view, or sexual orientation). Consent must be an express, separate statement. A checkbox near the publication terms, stating that the text may include health, belief or other sensitive information, is the minimum. Make the statement specific: "I agree that my entry, which may include personal information about my health, beliefs or other sensitive matters, is published and archived."
- Art. 9(2)(e) is not a safe main ground. The text speaks of data "manifestly made public by the data subject". Drafts and moderation queue content are not public. Publication is by the operator after review. The manifest-publication argument is strongest when a contributor independently publishes sensitive content and the operator copies it; it is weaker when the operator curates content for the archive. The CJEU's broad reading of indirect revelation (C-184/20) means a text that does not state a sensitive fact can still be special-category data. Treat 9(2)(e) as a fallback, not as a basis for the main flow.
- Inferred special categories: the operator must not infer special categories from metadata (for example, inferring religion from a profession, or sexuality from a relationship field). Structured fields such as "relationship to AI" should not invite sensitive disclosure.
- Third-party special-category data (for example, a contributor describes a colleague's illness) cannot be covered by the contributor's consent. Moderation must remove or redact it (plan section 10 agrees). The moderation policy should say so and the moderator should record the reason.
- Withdrawal of explicit consent stops further processing (GDPR art. 7(3)).

### Open questions

- Does 9(2)(e) apply if the contributor submitted the text through a public form that states it will be published? [uncertain; judgment text not read in full]
- If explicit consent is withdrawn for one entry, can the operator keep the entry on the basis of 9(2)(e)? Our reading: no, and the consent flow should not rely on 9(2)(e) to avoid this issue. [uncertain]

## 4. Minors (GDPR art. 8; Loi I&L arts. 45 and 51)

### What the law says

- Art. 8(1), GDPR: "Where point (a) of Article 6(1) applies, in relation to the offer of information society services directly to a child, the processing of the personal data of a child shall be lawful where the child is at least 16 years old. Where the child is below the age of 16 years, such processing shall be lawful only if and to the extent that consent is given or authorised by the holder of parental responsibility over the child. Member States may provide by law for a lower age for those purposes provided that such lower age is not below 13 years." [F, quoted in segments]
- Art. 8 therefore applies only where consent under art. 6(1)(a) is the basis, and only to information society services offered directly to a child [F].
- France: the threshold is 15, set by Loi I&L art. 45 (cited on the CNIL page [F]). Below 15, consent must be given jointly by the minor and the holder of parental authority. The CNIL states that consent of one holder of parental authority is sufficient in practice and that the other is presumed to agree but must be able to object [F, CNIL Recommendation 4, first published June 2021]. The CNIL scope wording is "dans le cadre des services en ligne" and does not say whether it covers all information society services or only those directed at children [F].
- Loi I&L art. 51 II: at the request of the data subject, the controller must erase "dans les meilleurs delais" personal data collected in the context of an offer of information society services when the person was a minor at the time of collection [F]. The text read does not state that parental consent is needed to exercise this right [F].
- CNIL Recommendation 7 (1 June 2021 per the page) on verifying the child's age and parental consent: the CNIL endorses no single method; it says purely declarative systems should be excluded for higher-risk processing; it describes email verification and self-declaration as easily circumvented; it calls a facial-recognition approach disproportionate; it recommends limiting collection to what is strictly necessary and not keeping verification data once verification is complete [F].

Member state thresholds (secondary; verify each against national law before use):

| Age | Member states (per a secondary comparison) |
|---|---|
| 13 | Belgium, Estonia, Finland, Latvia, Malta, Portugal, Sweden |
| 14 | Austria, Bulgaria, Cyprus, Italy, Lithuania, Spain |
| 15 | Czechia, France, Greece, Slovenia; Denmark listed as 15 in one source (from 2024) and 13 in older sources (conflict) |
| 16 | Croatia, Germany, Hungary, Ireland, Luxembourg, Netherlands, Poland, Romania, Slovakia |

[S, from a comparison page; the source was itself inconsistent on Denmark and some entries were garbled. Germany's 16 is by default, with no specific national rule confirmed. Verify each row.]

### Application to the Guestbook

- Art. 8 is engaged only for consent-based processing (publication, optional metadata). If the account is run on contract or legitimate interest, art. 8 may not be triggered for the account, but the publication path will be consent-based and so will need an age gate.
- Whether the service is "offered directly to a child" is uncertain. The service is open to all and the plan explicitly invites young people to contribute. Treat it as offered directly to children for design purposes.
- Recommended design: (1) ask for age range at the start of the flow, without making the age a public field for minors; (2) under 15 (France), require the joint parental flow (see Recommendation 4 and 7 above) before publication; (3) 15 and above: normal flow; (4) do not publish the age of any contributor under 15, and consider not publishing the exact age range for under 18s; (5) moderate minors' entries more closely; (6) use a verification method that CNIL Recommendation 7 would consider proportionate. A bare email click to the parent is the weakest method the CNIL describes; document why it was chosen and what the residual risk is.
- Verification data (parent email, declarations) should be deleted after the check, per CNIL Recommendation 7 [F].
- A minor aged 15 or older has the normal flow. A minor below 15 needs the joint parental flow in France. The GDPR allows a national age no lower than 13 (art. 8(1) [F]), so France at 15 is within the permitted range.
- Build the erasure right under art. 51 II into the withdrawal flow, so that an adult who contributed as a minor can request erasure without an adult's approval.
- Mention the minimum age and the parental flow in the terms and the privacy notice.

### Open questions

- Does art. 8 (and Loi I&L art. 45) apply to a service that is not directed at children but accepts minors? [uncertain]
- What is a "proportionate" verification for a free archive, given the CNIL says email verification is ineffective and declarative systems are excluded for higher-risk processing? [uncertain; no CNIL statement for this specific risk level was read]
- Does the French 2023 "majorite numerique" law (mentioned by one commentator as requiring under-15s to obtain parental authorisation to register on social networks) apply to the Guestbook, and is its article number verified? [S only; not verified, may not apply]
- Denmark's threshold (13 or 15) and other rows of the member-state table need verification against the national statutes.

## 5. DSA, information society services, and LCEN hosting duties

### What the law says

- Directive 2015/1535 art. 1(1)(b): an "information society service" is "tout service presté normalement contre remuneration, a distance, par voie electronique et a la demande individuelle d'un destinataire de services" [F].
- Directive 2000/31 recital 18: information society services "are not solely restricted to services giving rise to on-line contracting", and extend "in so far as they represent an economic activity, ... to services which are not remunerated by those who receive them" [F].
- DSA (Regulation (EU) 2022/2065) art. 3(i) (online platform: a hosting service that, at the request of a recipient, stores and disseminates information to the public) [F]. Art. 3(g)(iii) (hosting service) [F via LCEN cross-reference; DSA text not read directly at art. 3(g)].
- DSA art. 6(1): hosting exemption where an information society service "consists of the storage of information" provided by a recipient, conditioned on not having actual knowledge of illegal content, and acting expeditiously on obtaining it [F].
- DSA art. 14(1): terms and conditions must include information on restrictions imposed on the content [F, opening only].
- DSA art. 15(2): transparency reporting under art. 15(1) does not apply to intermediary service providers that qualify as micro or small enterprises [F].
- DSA art. 16(1): providers of hosting services must put mechanisms in place to allow any individual or entity to notify them of illegal content [F]. Section 2 of Chapter III (which includes art. 16) applies to all hosting providers, subject to the scope of art. 19 [F for art. 19 structure, see below].
- DSA art. 17(1): providers of hosting services must give a clear and specific statement of reasons to affected recipients when restricting content [F].
- DSA art. 19(1): "This Section, with the exception of Article 24(3) thereof, shall not apply to providers of online platforms" that qualify as micro or small enterprises (Recommendation 2003/361/EC) [F, opening text read; the full clause was not read].
- DSA art. 28(1): providers of online platforms accessible to minors shall put in place appropriate and proportionate measures [F, opening only].
- LCEN art. 6 I 2 and I 3 (post-SREN) define hosting and search engine providers by reference to the DSA [F].

### Application to the Guestbook

- Is it an information society service at all? The project is free, non-commercial and has no revenue (plan). Under directive 2015/1535 art. 1(1)(b), an ISS is one "normally provided for remuneration". Recital 18 of directive 2000/31 extends the notion to free services "in so far as they represent an economic activity". A non-economic personal archive is therefore arguably outside the notion. This is uncertain and could change with donations, sponsorships or grants (see open questions).
- Conservative assumption for the self-review: treat the service as an ISS, a hosting service and an online platform under the DSA.
- If DSA applies and the operator is a micro or small enterprise (the operator is an individual, so this is very likely the case), art. 19(1) excludes the platform-specific Section 3 (arts. 20 to 28) for online platforms. Art. 16 (notice and action) and art. 17 (statement of reasons) still apply to hosting providers. Art. 14 (terms) applies to all intermediary providers. Art. 15(2) exempts micro and small providers from transparency reporting.
- Practical consequence: a visible notice mechanism for illegal content, a written statement of reasons when content is removed, and terms that describe the restrictions. These are required even for a micro operator, subject to the verification of the full text of arts. 14, 16, 17 and 19.
- Moderation of pre-publication entries will count as editorial control. That is compatible with the DSA but weakens the hosting exemption for published text (Papasavvas, secondary). Treat the operator as publisher for published text and as hosting provider for the notice-and-action duties.
- The DSA also contains a notice route for minors' protection (art. 28) that applies only to online platforms, and is excluded for micro and small enterprises under art. 19(1). The GDPR art. 8 and Loi I&L art. 45 requirements still apply.
- The definition of "micro" and "small" enterprise is in Recommendation 2003/361/EC [N, thresholds not read in this session].

### Open questions

- Does the operator's activity count as an "economic activity" under recital 18 of directive 2000/31? [uncertain]
- Does an online archive with pre-publication review qualify as a "platform" (disseminating to the public at the request of the recipient) under art. 3(i)? Our reading: probably yes, which is why art. 19 matters. [uncertain]
- Exact contents required by art. 16(2) (the form of a notice) and art. 17 (statement of reasons) must be read in full before drafting the notice form. [N for full text]

## 6. French identification-data retention (decree 2021-1362 and LCEN art. 6 V A)

### What the law says

- LCEN art. 6 V A (post-SREN; formerly art. 6 II): access and hosting providers must keep data allowing identification of anyone who contributed to the creation of content, under conditions set by decree in Conseil d'Etat, after CNIL opinion, under CPCE art. L34-1 II bis to III bis [F].
- Decree no. 2021-1362 of 20 October 2021 (JORF 21 October 2021) on retention of data allowing identification of any person who contributed to content, adopted under "II de l'article 6" of the LCEN (old numbering) [F, Legifrance page, via summary; also S, search results].
- Art. 1: retention obligations under CPCE art. L34-1 [F].
- Art. 2: civil identity data (names, birth details, postal and email address, phone numbers): retain up to five years from the end of validity of the user's contract [F, summary].
- Art. 3: other account data (identifiers, pseudonyms, password-recovery data): one year from the end of contract or account closure [F, summary].
- Art. 4: payment data: one year [F, summary].
- Art. 5: technical connection data (connection identifier, IP address and port, protocols) for content creators: one year from the connection or from the creation of content, per operation [F, summary].
- Art. 6: traffic and location data: one year, only when the Prime Minister issues an order [F, summary].
- Art. 7: "contribution" to content creation includes initial creation, modification and deletion [F, summary].
- Art. 8: retention obligations in arts. 2 to 6 apply only to data that providers actually collect when they operate online communication services [F, summary].
- Conseil d'Etat, decision no. 459724 of 30 June 2023, upheld the decree and held that providers only keep data they actually collect [S, search summary].
- Art. 6 V B: failure to retain, or refusal to produce data to a judicial authority, is punishable by one year's imprisonment and EUR 250,000 [F].

### Application to the Guestbook

- Whether the operator is a "fournisseur de services d'hebergement" under the decree is the key question. If yes, it must keep: account identifiers (email, identifiers, recovery data) for one year after the account ends; civil identity data for five years if collected; and connection data (IP address and port) at content creation for one year per operation.
- Art. 8 of the decree suggests the duty only reaches data the operator actually collects. Choosing not to collect IP addresses is a legitimate minimisation measure, but it must be decided on the merits of the design, not to avoid the decree. Whether the operator can avoid the duty by not collecting the data is uncertain and should be confirmed.
- The magic-link email is an account identifier, so if the decree applies, it must be held for one year after the account closes even after a withdrawal request. This is a legal obligation (GDPR art. 6(1)(c) and art. 17(3)(b) [N]) and the privacy notice must say it.
- Civil name: the project collects only an optional display name, so art. 2 probably does not apply unless the operator collects civil identity elsewhere (open question).
- Decree text is out of date in its cross-references (it still refers to "II de l'article 6"). This is a drafting issue to flag, not a reason to ignore the decree.
- Tension with minimisation (GDPR art. 5(1)(c) and (e) [N]) and with erasure (art. 17): the decree duty is a legal basis for retention, so erasure is limited for those data. The design should keep this set as small as possible and separate from public data.

### Open questions

- Is a non-professional publisher hosting user-submitted testimony a "fournisseur de services d'hebergement de contenus en ligne" for the decree? Our working assumption is that it may be. [uncertain, decisive]
- If the decree applies, can the operator reduce the data collected so as to fall outside arts. 2 to 5 without breaching art. 6 V A? [uncertain]
- The Conseil d'Etat decision and the CNIL opinion on the decree should be read in full. [N]

## 7. DPIA, records (Art. 30), DPO, breach notification

### What the law says

- Art. 35(1): a DPIA is required where processing is likely to result in a high risk [N for 35(1) wording; the CNIL page on DPIA says the same, F summary].
- Art. 35(3)(b): DPIA required for large-scale processing of special categories under art. 9(1) [F].
- CNIL deliberation no. 2018-327 of 11 October 2018 (JO 6 November 2018), with a list of processing types requiring a DPIA, 14 items in the annex, and an express statement that the list is non-exhaustive ("Cette liste a un caractere non-exhaustif") [F]. The annex items that match sensitive data and vulnerable persons relate to health, genetic data, workplace alerts, biometrics and social support. None concerns a public archive or publication [F, summary].
- The CNIL annex refers to the EDPB criteria (nine criteria in the annex headings include sensitive data, vulnerable persons, evaluation or scoring, combining datasets, automated decisions, systematic monitoring, large-scale processing and others) [F, summary]. The EDPB WP248 rev.01 document was not readable in this session (PDF only) [N].
- Art. 30(1): controller must keep a record of processing [N].
- Art. 30(5): the obligation to keep a record does not apply to an enterprise or organisation employing fewer than 250 persons, unless the processing is likely to result in a risk to rights and freedoms, is not occasional, or includes special categories under art. 9(1) or criminal-offence data under art. 10 [F].
- Art. 33(1): notification to the supervisory authority within 72 hours, where feasible, unless the breach is unlikely to result in a risk [F for the first sentence; the exception N].
- Art. 34: communication to the data subject where the breach is likely to result in a high risk [N].
- Art. 37(1)(c): a DPO is required where core activities consist of large-scale processing of special categories under art. 9 [F].
- Art. 28(3) (processor contract) is in section 9.

### Application to the Guestbook

- A DPIA is strongly advisable and probably mandatory. Two criteria are likely present: sensitive data (voluntary self-disclosure is special-category data, and C-184/20 extends it to indirect revelation) and vulnerable persons (minors are invited). Publication is not a listed CNIL item, but the processing is public and archived, which heightens the risk. The CNIL annex is non-exhaustive, so it does not rule out a DPIA. The conservative position is to run one using the CNIL PIA tool and to document the result. [criteria count rule: uncertain, see open questions]
- The Art. 30(5) exemption does not apply: the processing includes special-category data (the exemption fails on that condition). Keep a record of processing regardless of headcount.
- The DPO is not mandatory: the processing is not large scale. Appoint a named privacy contact anyway, because the rights procedure needs a contact point.
- Breach procedure: a written procedure with a 72-hour CNIL notification path and a data-subject communication template is needed before launch. Include the moderation interface and backups in the scope.

### Open questions

- Does the WP248 rule ("two criteria usually require a DPIA") apply? Taken from memory, not verified in this session. [N]
- Does a voluntary publication of sensitive information by a contributor create a "high risk" for the archive as a whole, or only for each entry? [uncertain]

## 8. Cookies and trackers

### What the law says

- CNIL guidelines on cookies and other trackers (adopted 17 September 2020; page dated 29 September 2020) [F].
- The CNIL page lists trackers that do not require consent, including: (1) trackers that store the user's choice about trackers; (2) authentication trackers that secure the authentication mechanism (for example limiting automated access attempts); (3) shopping cart trackers; (4) user-interface personalisation trackers such as language, where the personalisation is an intrinsic and expected part of the service; (5) load-balancing trackers for equipment supporting a communication service; (6) paywall sampling trackers; (7) some audience-measurement trackers under conditions [F].
- The criterion is that the tracker is "strictement necessaire a la fourniture d'un service de communication en ligne" that the user expressly requested [F].
- The CNIL page does not name session cookies or CSRF tokens explicitly [F]. Their exemption rests on the general "strictly necessary" criterion [F on criterion, inference for CSRF and session].
- ePrivacy Directive 2002/58/EC art. 5(3) and Loi I&L art. 82 transpose the consent rule for trackers [N].

### Application to the Guestbook

- Session cookie for the login: exempt under the authentication and strictly-necessary criteria. Name and scope should be minimal.
- CSRF token: exempt under the strictly-necessary criterion. Confirm with the CNIL page wording in the privacy notice.
- Language preference: exempt if it is an intrinsic and expected part of the service (CNIL list item 4). Keep it as a first-party cookie or a URL path segment.
- No analytics, no advertising, no third-party embeds. Do not add tracking pixels to transactional emails.
- Server logs and error monitoring are processing under art. 6(1)(f) and are not trackers. They must still be disclosed in the privacy notice.
- Avoid third-party fonts, maps, video and social embeds, which can set trackers or transfer IP addresses outside the EU.

### Open questions

- Whether the operator needs a cookie banner at all (answer: no, if only exempt cookies are used; confirm after the final design). [uncertain until built]
- Whether a privacy-preserving audience measurement (for example server-side counts) is exempt. The CNIL page says some are, under conditions not read here. [uncertain]

## 9. Processors, subprocessors, EU transfers and US exposure

### What the law says

- Art. 28(3), first sentence: processing by a processor "shall be governed by a contract or other legal act under Union or Member State law" [F].
- Art. 28(3) required terms (instructions, confidentiality, security, subprocessor controls, assistance, deletion or return, audit) [N].
- Commission Implementing Decision (EU) 2023/1795 of 10 July 2023 (adequacy for the EU-US Data Privacy Framework): "For the purpose of Article 45 of Regulation (EU) 2016/679, the United States ensures an adequate level of protection", for transfers to organisations on the DPF list [F, partial text read; the full article 1 wording was not read].
- 18 U.S.C. 2713 (added by the CLOUD Act, Pub. L. 115-141): providers of electronic communication or remote computing services must preserve, backup or disclose contents and records within their possession, custody or control, "regardless of whether such communication, record, or other information is located within or outside of the United States" [F, Cornell LII].

### Application to the Guestbook

- Processors likely: the VPS provider, the email delivery provider (magic links), the backup storage provider, possibly a DNS or CDN provider, and possibly an error-monitoring service.
- Prefer EU-headquartered processors with EU-only data location. Each needs a DPA under art. 28(3) and a sub-processor list.
- If any processor is a US company or has a US parent, the CLOUD Act reach applies regardless of data location (18 U.S.C. 2713 [F]). That is a practical risk, not a legal bar, and should be recorded in the DPIA.
- Transfers to a DPF-certified US processor are covered by the adequacy decision only if the processor is on the DPF list (art. 1 [F]). Check certification before relying on it.
- Backups: the backup provider is also a processor and must be covered by a DPA. Encrypt backups before they leave the operator's control.

### Open questions

- Which processors have US parents or US sub-processors? [to do]
- Does a DPF listing remain valid if the adequacy decision is challenged? [uncertain; outside this session]

## 10. Right to erasure, withdrawal and archival editions

### What the law says

- Art. 17(1): right to obtain erasure of personal data "without undue delay" in listed cases [F, opening].
- Art. 17(2): where the controller has made personal data public and is obliged to erase it, it must "take reasonable steps, including technical measures, to inform controllers which are processing the personal data" of the erasure request [F].
- Art. 17(3)(a): erasure does not apply to processing necessary "for exercising the right of freedom of expression and information" [F]. Art. 17(3)(d): archiving in the public interest, scientific or historical research or statistical purposes, where erasure would seriously impair those purposes [F for the listing; the "seriously impair" condition is N].
- Art. 17(3)(b): erasure does not apply to processing necessary to comply with a legal obligation (decree 2021-1362 example) [N].
- Art. 5(1)(e): storage limitation [F].
- Art. 7(3): withdrawal of consent at any time [F].

### Application to the Guestbook

- Withdrawal removes the entry from the live site, excludes it from future editions and deletes it from the project's own systems (plan section 21), including search indexes, translations, caches, moderation interfaces and generated files.
- Downloaded copies by third parties: the operator cannot delete them. Art. 17(2) requires reasonable steps, not success. The operator should publish a machine-readable withdrawal list (plan section 20), notify known mirrors where it can, and state clearly in the privacy notice and the archive documentation that downloaded copies cannot be recalled.
- Archival editions already published (e.g. 2027.0): the operator's own copies are under its control. Issue revised editions (2027.1 etc.) that remove withdrawn entries and leave tombstones. Art. 17(3)(d) might justify retaining an archival edition that is not revised, but that exemption requires safeguards under art. 89 and a showing that erasure would seriously impair the purpose. Relying on it for explicit-consent special-category data is risky; the default should be to honour withdrawal.
- Honest contributor notice (draft wording to be reviewed): "Your entry will be removed from the live guestbook and from future archival editions. Copies that others have already downloaded are outside our control. We will notify archive mirrors through our withdrawal list, but we cannot guarantee that every copy will be removed."
- Tombstone: a content-free record that an entry existed and was withdrawn. It should carry only the stable identifier, status and a withdrawal date. It must not carry the public name, language, country or topic labels that could identify the contributor when combined (plan section 22 agrees). Do not use a hash of the email if the hash can be reversed.
- Backups: no CNIL rule fixing a backup deletion period was found [S, search results]. Document a rotation period (for example 30 to 90 days, to be decided) and an "erase on restore" procedure so that data deleted after backup is deleted again after a restore. Keep the backup encrypted and in the scope of the DPA.

### Open questions

- Is an un-revised edition that remains in a public repository lawful after a withdrawal? [uncertain; depends on the art. 17(3)(d) analysis]
- How long can backups hold a withdrawn entry? [uncertain, no CNIL rule read]

## 11. Copyright, moral rights and licences

### What the law says

- CPI art. L121-1 (moral rights are perpetual, inalienable and imprescriptible; the author's right to respect for the work and name): [S, lawplayer and Pappers reproductions; Legifrance text not read in this session].
- CPI art. L121-2 (right of disclosure) [N].
- CPI art. L122-4 (reproduction and communication require the author's consent) [N; cited in commentary].
- CPI art. L122-5 (exceptions, including quotation) [N].
- CPI art. L112-3: translations, adaptations, transformations and arrangements are protected as original works, without affecting the rights in the original work [S, search summary of the Legifrance page].
- CPI art. L131-3: transfers of economic rights must be in writing, identify each right separately and delimit the scope of exploitation (field, territory, duration) [S; secondary commentary; the Legifrance text not read].
- CPI art. L122-7: a total transfer is limited to the modes of exploitation stated in the contract [S].
- CC BY 4.0 legal code [F]:
  - Section 2(a)(1): the licensor grants a "worldwide, royalty-free, non-sublicensable, non-exclusive, irrevocable license".
  - Section 2(b)(1): "Moral rights, such as the right of integrity, are not licensed under this Public License".
  - Section 6(a): the licence applies for the term of the copyright.
  - Section 6(c): the licensor may stop distributing the work at any time without terminating the licence.
  - Section 1(a): "Adapted Material" includes material derived from or based on the licensed material.
  - Section 7(a): the licensor is not bound by additional terms from the licensee [F].
  - Attribution condition: section 3(a)(1)(A) (name where supplied) [N, wording not read].
- CC0 and moral rights in France: not verified [N].

### Application to the Guestbook

- Contributors own copyright in their own texts, subject to any AI-generated or third-party material. Copyright in fully AI-generated text may not exist; this is open (see below).
- Grant needed. Recommended grant from each contributor (in the publishing terms, accepted at submission), written and scoped:
  - non-exclusive, worldwide, royalty-free right to host, display, index, reproduce, and distribute the entry, including in archival editions and mirrors;
  - right to translate and adapt the entry (for canonical translations, machine translations clearly labelled, see plan section 8);
  - right to redact or correct the entry for privacy, legal or accuracy reasons, with the contributor's consent to modifications that are not substantive (this addresses the integrity right, CPI art. L121-1 [S]);
  - the scope and duration (perpetual for the duration of copyright) and the modes (online and printed archival editions).
- Public licence: CC BY 4.0 is the common choice and matches "third parties can mirror" (plan section 20). CC BY-NC 4.0 is an alternative if the project wants to prevent commercial reuse; it is not an open licence under the Open Definition [N].
- Attribution with anonymous entries: CC BY requires credit when the creator is identified; for anonymous or pseudonymous entries the credit line should be the chosen pseudonym or "Anonymous contributor", with the entry identifier.
- Translations: derivative works under CPI art. L112-3 [S]. A translation made by the operator is a new work; the operator's own copyright in the translation is limited to the translation itself and does not cover the original.
- Third-party text quoted in an entry: the contributor must warrant that quotations are lawful; the moderation policy should address this, and CPI art. L122-5 (quotation) may apply to short quotations [N].

### How withdrawal interacts with an irrevocable licence

- The GDPR withdrawal (art. 7(3), art. 17) addresses personal data and the operator's processing. It does not make a copyright licence ineffective, and it does not oblige the licensee to destroy copies (the copyright licence is separate, and CC BY section 2(a)(1) describes the licence as irrevocable).
- Practical consequence: after withdrawal, the operator removes the entry from its own systems and stops distributing it (CC section 6(c) allows the licensor to stop distributing), but third-party copies made under the licence remain licensed for copyright purposes. Those third-party holders, however, become controllers for any personal data they hold and must respond to erasure requests on their own account [N, GDPR art. 17 for third parties].
- The contributor should be told this in plain language, and the publishing terms should state that the licence is irrevocable as to copies already made under it.

### Open questions

- Is an AI-generated testimony (plan section 7 allows fully AI-generated text) protected by copyright in France? If not, what licence does the operator need? [uncertain]
- Does a contributor's moral right of integrity prevent the operator from redacting names or correcting text without consent? The terms should obtain an express consent. [uncertain]
- Does the French formalism of art. L131-3 apply to a non-exclusive licence granted to the public under a standard licence? [uncertain; the usual view is that it applies to transfers, not to a non-exclusive licence, but not verified]
- Is CC BY 4.0 or CC BY-NC 4.0 the right public licence? Decision for the maintainer.

## 12. Retention periods (recommended, to be confirmed in the DPIA)

These are recommendations, not legal minima, unless marked. Where a legal minimum exists it is quoted from section 6.

| Data category | Recommended retention | Legal anchor |
|---|---|---|
| Unfinished drafts never submitted | Delete after a fixed inactivity period (for example 30 to 90 days) | Art. 5(1)(e) [F]; period is a recommendation |
| Account email and login data | While the account is active; if decree 2021-1362 applies, one year after account closure (art. 3) | Decree art. 3 [F] (applicability uncertain) |
| Civil identity data, if ever collected | Five years after contract end if decree applies (art. 2) | Decree art. 2 [F]; avoid collecting if not needed |
| Connection and IP data at content creation, if collected | One year from creation (art. 5) if decree applies | Decree art. 5 [F] |
| Submitted testimony and public metadata | Until withdrawal or deletion, then removed from all systems | Art. 5(1)(e) [F]; art. 17 [F] |
| Pre-publication moderation notes | Until decision, then short period (for example 12 months) unless a dispute | Art. 5(1)(e) [F]; period is a recommendation |
| Withdrawal and deletion records (minimal) | Request date and non-reversible identifier, for the limitation period of any claim | Art. 6(1)(c)/(f) [N]; period to be confirmed |
| Parental consent record | While the minor's entry is held, plus the limitation period | Art. 8 [F]; period a recommendation |
| Age and parental verification data | Delete after verification | CNIL Recommendation 7 [F] |
| Security and server logs (without IP addresses if not required) | Short (for example 30 to 90 days) unless decree applies | Art. 6(1)(f) [N]; decree art. 5 if applicable |
| Email delivery logs | Short (for example 30 days) | Art. 6(1)(f) [N]; period a recommendation |
| Backups | Rotation period documented (for example 30 to 90 days) with erase-on-restore | No CNIL rule read [S]; recommendation |
| Archival editions | Retained as published; revised editions reflect withdrawals | Plan section 20 [F for plan]; art. 17(3)(d) uncertain |

## 13. Self-review checklist and documents to produce before launch

Documents:

- [ ] Privacy notice (information under arts. 13 and 14 [N]): operator identity, purposes and bases per category, recipients and processors, transfers, retention table (section 12), decree retention if applicable, rights, complaint to the CNIL, minors' section, archival editions, withdrawal limits.
- [ ] Register of processing (art. 30(1) [N]), kept regardless of headcount because special categories are processed (art. 30(5) [F]).
- [ ] DPIA using the CNIL PIA tool (section 7), with the risk analysis for minors, special categories, publication and mirrors, and a documented decision.
- [ ] Mentions legales (LCEN art. 1-1 I and II [F]): publisher identity or the art. 1-1 II route, director of publication, hosting provider name, address, phone, and storage provider if applicable.
- [ ] Terms of use and publishing rules: publication, AI disclosure, moderation criteria (plan section 9), third-party information warnings (plan section 10), notice-and-action policy (DSA art. 16 [F]), statement of reasons template (DSA art. 17 [F]), restrictions (DSA art. 14 [F]).
- [ ] Contributor licence and copyright grant (section 11), and a CC BY 4.0 notice for public reuse.
- [ ] Consent texts: explicit consent for special-category content (section 3), consent for optional metadata, consent to publication and archival editions, consent to redaction and translation.
- [ ] Parental consent flow for under-15s (section 4), including the verification method, the other-parent presumption and objection route, and the deletion of verification data (CNIL Recommendation 4 and 7 [F]).
- [ ] Data subject request procedure: identification of the requester (proportionate, per CNIL Recommendation 7 [F]), access, rectification, erasure (including the art. 51 II minor right [F]), restriction, objection, portability (if relevant), response times (art. 12(3) [N]), refusal grounds, logging of requests.
- [ ] Withdrawal procedure and machine-readable withdrawal list, with tombstone rules (plan section 20 and 22).
- [ ] Breach notification procedure (art. 33 [F], art. 34 [N]), including contacts and templates.
- [ ] Processor register and DPAs (art. 28(3) [F]), with sub-processor lists and transfer assessments (section 9).
- [ ] Retention schedule with recommended periods (section 12), and a backup policy with erase-on-restore.
- [ ] Cookie and tracker statement (section 8).
- [ ] Accessibility and language: French and English versions of all contributor-facing legal texts (plan section 8).

Self-review checks:

- [ ] Confirm the operator's status under the decree 2021-1362 (section 6) and record the answer.
- [ ] Confirm the art. 1-1 I 1 domicile approach (section 1) and record it.
- [ ] Confirm that the age gate is in place before any consent-based publication (section 4).
- [ ] Confirm that no tracker other than the exempt list is set (section 8).
- [ ] Confirm that publication of a withdrawn entry stops and that deletion propagates to search indexes, caches, translations and generated files (plan section 21).
- [ ] Confirm that test withdrawals work end to end, including tombstones and the withdrawal list.
- [ ] Confirm that the DPIA's residual risk for minors and sensitive content is accepted by the operator.
- [ ] Read the full texts of the instruments marked [S] or [N] and update this document.

## 14. Open questions for a lawyer (short list)

- LCEN art. 1-1 I 1 and II: domicile, and whether a publicly named natural person can use a domiciliation address.
- Decree 2021-1362: whether the operator is a covered "fournisseur d'hebergement".
- Art. 8 GDPR and Loi I&L art. 45: whether the service is "offered directly to a child", and the adequate verification method.
- Art. 9(2)(e) and the reading of C-184/20 for voluntary publication.
- Art. 17(3)(d) and the edition policy after withdrawal.
- Copyright in AI-generated text, and the French formalism for a licence to the public.
- ISS status given the non-commercial, free service.

## Sources

Primary, fetched in this session [F]:

- GDPR, Regulation (EU) 2016/679, EUR-Lex: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 (arts. 5(1)(e), 6(1)(e) and (f), 6(3), 7(3), 8(1), 9(2)(a), 9(2)(e), 17(1), 17(2), 17(3)(a) and (d), 28(3), 30(5), 33(1), 35(3)(b), 37(1)(c), 85(1)-(2), 89(1); recitals 38, 65, 69)
- DSA, Regulation (EU) 2022/2065, EUR-Lex: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065 (arts. 3(i), 6(1), 14(1), 15(2), 16(1), 17(1), 19(1), 28(1); recitals 7, 13, 22, 29, 49, 50, 57)
- Directive (EU) 2015/1535, art. 1(1)(b), EUR-Lex: https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:32015L1535
- Directive 2000/31/EC (e-commerce), recital 18, EUR-Lex: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32000L0031
- CJEU C-184/20, OT v Vyriausioji tarnybines etikos komisija, judgment of 1 August 2022, EUR-Lex: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62020CJ0184 (paras 23, 44, 108-128 read in part)
- Commission Implementing Decision (EU) 2023/1795 (EU-US Data Privacy Framework), EUR-Lex: https://eur-lex.europa.eu/eli/dec_impl/2023/1795/oj/eng (art. 1 partially read)
- LCEN, loi no. 2004-575 (consolidated, version as read in session, en vigueur au 15 novembre 2026), Legifrance: https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000801164 (arts. 1-1, 1-2, 6 I 2, 6 I 3, 6 II, 6 IV A-B, 6 V A-B)
- Loi no. 78-17 (Loi Informatique et Libertes, consolidated), Legifrance: https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000886460 (arts. 4 point 5, 6, 51 I-II, 80, 88 - art. 88 concerns the directive 2016/680 regime and does not apply here)
- Decree no. 2021-1362 of 20 October 2021, Legifrance: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044228912 (arts. 1 to 13, summarised)
- Deliberation no. 2018-327 of 11 October 2018 (CNIL list of processing requiring a DPIA), Legifrance JO: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000037559521 (annex)
- CNIL, Recommendation 4 (parental consent for minors under 15): https://www.cnil.fr/fr/recommandation-4-rechercher-le-consentement-dun-parent-pour-les-mineurs-de-moins-de-15-ans
- CNIL, Recommendation 7 (verifying age and parental consent): https://www.cnil.fr/fr/recommandation-7-verifier-lage-de-lenfant-et-laccord-des-parents-dans-le-respect-de-sa-vie-privee
- CNIL, cookies and trackers, "Que dit la loi": https://www.cnil.fr/fr/cookies-et-autres-traceurs/regles/cookies/que-dit-la-loi
- CNIL, DPIA page (AIPD): https://www.cnil.fr/fr/RGPD-analyse-impact-protection-des-donnees-aipd (fetch partial)
- Creative Commons Attribution 4.0 legal code: https://creativecommons.org/licenses/by/4.0/legalcode.en
- 18 U.S.C. 2713, Cornell LII: https://www.law.cornell.edu/uscode/text/18/2713
- Code de la propriete intellectuelle, Legifrance (table of contents only was read): https://www.legifrance.gouv.fr/codes/id/LEGITEXT000006069414/
- WP248 rev.01 (EDPB/Article 29 DPIA guidelines), not readable in session: https://ec.europa.eu/newsroom/just/document.cfm?doc_id=47711 [N]

Secondary [S] (used as leads only, verify before reliance):

- Legalnest (LCEN version dates): https://legalnest.io/en/guides/legal-notice-website-france/
- Village de la Justice, on the SREN rewrite of LCEN art. 6 (the art. 6 I 8 to 6-3 renumbering): https://www.village-justice.com/articles/nouvel-article-lcen-pour-retrait-plus-dynamique-des-contenus-ligne,40611.html
- Conseil d'Etat, decision no. 459724 of 30 June 2023 (decree 2021-1362 upheld): https://www.conseil-etat.fr/fr/arianeweb/CE/decision/2023-06-30/459724
- Lexbase, art. 8 decree 2021-1362: https://www.lexbase.fr/texte-de-loi/art-8-decret-n-20211362-du-20-octobre-2021-relatif-a-la-conservation-des-donnees-permettant-didentif/Z30069TM.html
- Papasavvas, C-291/13 (summary), McCann FitzGerald: https://www.mccannfitzgerald.com/knowledge/technology-and-innovation/cjeu-clarifies-civil-liability-for-internet-publishing ; judgment page https://ipcuria.eu/case?reference=C-291/13
- CPI art. L121-1 (commentary): https://lawplayer.com/fr/article/LEGITEXT000006069414/LEGIARTI000006278891
- CPI art. L131-3 (commentary): https://justice.pappers.fr/loi/LEGITEXT000006069414/article/LEGIARTI000006278958
- CPI art. L112-3 (Legifrance page reference): https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006278879
- Age-of-consent comparison table (Recording Law): https://www.recordinglaw.com/world-laws/world-data-privacy-laws/eu-data-privacy-laws/gdpr-consent-requirements/ ; Bastion: https://bastion.tech/learn/gdpr/childrens-data-protection/
- CNIL, retention periods FAQ: https://elections.cnil.fr/fr/cnil-direct/question/dois-je-fixer-une-duree-de-conservation-des-donnees-dans-mon-fichier (fetch did not complete)

Referenced from knowledge, not read in this session [N]: EDPB Guidelines 05/2020 on consent; EDPB Guidelines 2/2019 on art. 6(1)(b); WP248 rev.01 (see above); Recommendation 2003/361/EC (micro and small enterprise thresholds); Directive 2002/58/EC art. 5(3); Loi I&L art. 82; GDPR arts. 12(3), 13, 14, 17(3)(b) and (e), 32, 34, 37 full text; CPI arts. L121-2, L122-4, L122-5, L122-7, L131-3 full text; LCEN art. 6 I 4 and 5 full text; DSA arts. 2, 3(g), 11, 12, 20 to 28 full text; Code civil art. 2224 (limitation period, not checked).
