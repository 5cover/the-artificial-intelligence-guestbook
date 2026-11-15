# Moderation failures on small and volunteer-run platforms

Status: Research (2026-11-15), informative only. This is not legal advice; legal points must be checked by a French lawyer before launch.

## 1. Method and tags

Each claim carries one tag. [fetched] means the page was opened in this session and the statement was read there. [search] means the claim comes only from a search snippet or a secondary summary that was not opened. [inference] means reasoning from the sources above it.

Legal texts on Legifrance were read through a summarising fetch tool, marked [fetched, summarised] where they are used. Article numbers and short phrases were checked; verbatim wording must be re-read on Legifrance or EUR-Lex before any public use. Where a claim rests on this repository's earlier research, the source is named.

## 2. How moderation fails

### 2.1 Child sexual abuse material on a federated network

- The Stanford Internet Observatory report "Child Safety on Federated Social Media" (David Thiel and Renée DiResta, 24 July 2023) covers a two-day, time-boxed ingest of the local public timelines of the top 25 Mastodon instances by user count, with about 325,000 posts analysed and 112 instances of known CSAM found by PhotoDNA [fetched](https://stacks.stanford.edu/file/druid:vb515nd6874/20230724-fediverse-csam-report.pdf), section 3 and section 4.
- The report states that Mastodon "has no built-in mechanism to report CSAM to the relevant child safety organizations" and no default PhotoDNA integration [fetched](https://stacks.stanford.edu/file/druid:vb515nd6874/20230724-fediverse-csam-report.pdf), sections 2 and 5.4.
- A case study: in July 2023 reports on mastodon.xyz were "not immediately acted upon", an abuse report was sent to the hosting provider, and the operator of the .xyz top-level domain suspended the server's domain name, taking the whole service down; the administrator was also the sole moderator [fetched](https://stacks.stanford.edu/file/druid:vb515nd6874/20230724-fediverse-csam-report.pdf), section 2.1. The lesson for a small host is that a late response can bring the escalation chain down with it, not only the content [inference].
- Accounts posting CSAM "would remain active for hours or days", and when such accounts were removed no delete events were published, so federated servers may never learn that the content should go [fetched](https://stacks.stanford.edu/file/druid:vb515nd6874/20230724-fediverse-csam-report.pdf), section 4.2.
- The report recommends grayscale and blur tooling for moderators, which Mastodon lacked at the time [fetched](https://stacks.stanford.edu/file/druid:vb515nd6874/20230724-fediverse-csam-report.pdf), section 5.3.

### 2.2 Spam waves

- In February 2024, scripted account creation hit small Mastodon servers with open registration. TechCrunch (20 February 2024) reports that an administrator had fewer than 40 spam accounts to suspend that day, the first such day in four days [fetched](https://techcrunch.com/2024/02/20/spam-attack-on-twitter-x-rival-mastodon-highlights-fediverse-vulnerabilities/).
- Mastodon's founder advised requiring approval for sign-ups and blocking disposable email providers. The CTO said "there are no good built-in tools to handle this" and that the default for new instances would change [fetched](https://techcrunch.com/2024/02/20/spam-attack-on-twitter-x-rival-mastodon-highlights-fediverse-vulnerabilities/).
- The release that changed the default to closed registration and closing sign-ups after a week without an admin login is reported in a search summary [search](https://github.com/mastodon/mastodon/discussions/29267). Many small servers shut down during the wave, and admins built shared blocklists of abandoned instances [fetched](https://techcrunch.com/2024/02/20/spam-attack-on-twitter-x-rival-mastodon-highlights-fediverse-vulnerabilities/).

### 2.3 Closures and purges

- Refern: the IndieWeb site-deaths list records a shutdown on 13 September 2025, with all content deleted and the reason "increased reports of CSAM, project size, and expenses of running it". No export is recorded [fetched](https://indieweb.org/site_deaths). The reason is the operator's own, as quoted on that list.
- Mataroa: on 30 September 2022 the operator closed registrations to stop SEO spam blogs, and said reopening needs tooling that emails each blog's author an export of their words [fetched](https://hey.mataroa.blog/p/closing-registrations/). The homepage, fetched on 2026-11-15, calls the team "one person", says "This sets the bus factor to 1, which is not good", and invites sign-ups with "No email required for signup" [fetched](https://mataroa.blog/). Whether registrations are open again, and whether the export tool exists, is not established [inference]. The repository's custodial research (section 3.5) says registrations stayed closed; the homepage contradicts that.
- Bear Blog: unreviewed blogs carry noindex and nofollow tags and stay off the sitemap and discovery feed. The author reports spam among new blogs fell from about 30 percent to under 5 percent after an anti-spam measure; the figures are self-reported and the post is dated 20 September 2023 [fetched](https://herman.bearblog.dev/the-frustration-loop/).
- Bear Blog review time: about 35 to 60 minutes a day before the new workflow and about 5 minutes every two days after, in a post dated 18 May 2021 [fetched](https://herman.bearblog.dev/5-hours-to-15-minutes/). The dates show the workload was reduced; they do not show the current queue size.

### 2.4 Moderator wellbeing

- Gonzalez and Matias (Cornell, arXiv 2502.00244, a 2025 preprint not peer-reviewed) read 143 validation papers and report that harms are described mostly through news reports, lawsuits, qualitative research and some surveys: anxiety, depression, nightmares, fatigue, panic attacks and intrusive images. They do not estimate pooled prevalence of PTSD or burnout, note that the Maslach Burnout Inventory's validity is disputed, and warn against comparing employers with scales not validated for that purpose [fetched](https://arxiv.org/html/2502.00244).
- Kenya: more than 140 Facebook content moderators were reported in December 2024 as diagnosed with PTSD in a claim against Meta and its subcontractors; the figure of 81 percent with severe PTSD among 144 assessed is a search-summary figure [search](https://www.business-humanrights.org/en/latest-news/kenya-content-moderators-filed-a-lawsuit-against-meta-alleging-poor-working-conditions-including-insufficient-mental-health-support-and-low-pay/). The CNN article on the same case could not be fetched (HTTP 451) [search](https://edition.cnn.com/2024/12/22/business/facebook-content-moderators-kenya-ptsd-intl).
- The hotline's 2014 guide for hosts says a single employee should not handle such content alone, that the task should be shared between at least two people, and that regular breaks should be possible without justification [fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Vos contacts". The guide is dated and written for companies.

### 2.5 Volume and volunteer load

- Anaobi and colleagues (WWW 2023) studied administrators of Pleroma instances. A search summary reports the abstract's claim that "moderation is labor-intensive" and that admins of larger instances struggle to find resources [search](https://arxiv.org/pdf/2302.05915). The PDF did not extract on fetch, so no figures are quoted here.
- The Stanford report describes the "primarily volunteer nature of content moderators" as a structural limit [fetched](https://stacks.stanford.edu/file/druid:vb515nd6874/20230724-fediverse-csam-report.pdf), section 5.
- The Bear Blog review-time change in section 2.3 is the only measured before-and-after figure found for a small service [fetched](https://herman.bearblog.dev/5-hours-to-15-minutes/).

### 2.6 Inconsistent decisions and written rules

- Trujillo, Fagni and Cresci (arXiv 2312.10269) analysed 353.12 million statements of reasons from the largest EU platforms in the first 100 days of the DSA Transparency Database and report that "a remarkable fraction of the database data is inconsistent" [fetched](https://arxiv.org/abs/2312.10269). This measures consistency of submitted data, not whether like cases get like decisions [inference].
- A 2026 journal article reportedly finds that most moderation actions cite incompatibility with terms of service rather than illegality [search](https://www.tandfonline.com/doi/full/10.1080/13600834.2026.2712191). Not opened.
- Neocities removes content for legal or terms-of-service violations, and states that offensiveness alone is not grounds for removal [search](https://neocities.org/legal). A narrow published standard, cited in each decision, is what the repository's moderation principles already require ([moderation principles](../constitution/moderation-principles.md), practice 1 and 4) [inference].
- The DSA requires a statement of reasons with the facts relied on, the scope and duration, and the legal or contractual basis (art. 17(3)) [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065).

### 2.7 Appeals

- Mastodon: every moderation decision can be appealed, by the button in the notification email, in the app, or by email to [moderation@joinmastodon.org](mailto:moderation@joinmastodon.org), within 30 days. A moderator other than the one who acted reviews the appeal; the target is five business days; reversal is not guaranteed; a rejected appeal can be appealed once more by email to the moderation lead [fetched](https://help.joinmastodon.org/article/20-moderation-decisions-and-appeals).
- DSA art. 20(1) requires an internal complaint system for six months for providers of online platforms, and arts. 20 and 21 sit in Section 3 [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065). Art. 19(1) excludes Section 3 for online platforms that are micro or small enterprises [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065). A voluntary appeal route remains advisable [inference].

## 3. What works, on the evidence found

- Default-hidden publication: unreviewed content stays off search and discovery until review, as Bear Blog does [fetched](https://herman.bearblog.dev/the-frustration-loop/). This matches the repository's pre-publication queue.
- Friction at sign-up and default-closed registration for new services, as Mastodon moved to after February 2024 [fetched](https://techcrunch.com/2024/02/20/spam-attack-on-twitter-x-rival-mastodon-highlights-fediverse-vulnerabilities/).
- Hotlines as the reporting route: INHOPE describes 58 member hotlines in 53 countries and a secure cross-border exchange tool [fetched](https://www.inhope.org/EN). For France, the hotline is Point de Contact (section 4.4).
- Exposure controls for the moderator: grayscale and blur by default, recommended by the Stanford report [fetched](https://stacks.stanford.edu/file/druid:vb515nd6874/20230724-fediverse-csam-report.pdf), section 5.3.
- Published appeal windows and a second reviewer, as Mastodon does [fetched](https://help.joinmastodon.org/article/20-moderation-decisions-and-appeals).

## 4. French and EU legal duties

### 4.1 DSA notice and action, statement of reasons, criminal suspicions

- Art. 16(1): hosting services must offer a mechanism for any person to notify illegal content, and notices must be submitted electronically [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065).
- Art. 16(2): a notice must give the reasons, the exact location (such as a URL), the notifier's name and email, and a statement of bona fide belief. The name requirement does not apply to certain child-abuse offences listed in Directive 2011/93/EU [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065).
- Art. 16(4) to (6): confirm receipt promptly where contact details are given; tell the notifier the decision and redress options promptly; handle notices in a timely, diligent, non-arbitrary and objective manner, and disclose any automated tools [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065).
- Art. 17(1) to (3): a clear and specific statement of reasons for restrictions of content and accounts; it is owed only where the provider knows the user's electronic contact details, and no later than when the restriction takes effect [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065).
- Art. 18(1): where a hosting provider becomes aware of information suggesting a criminal offence involving a threat to the life or safety of a person, it must promptly inform the law enforcement or judicial authorities of the Member State concerned. Art. 18(2) covers the case where the Member State cannot be identified [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065).
- Art. 19(1): Section 3 (arts. 20 to 28, except art. 24(3)) does not apply to online platforms that are micro or small enterprises. Section 2, which contains arts. 16 to 18, is not excluded by that sentence [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065). Whether a private individual running a non-commercial archive is an "enterprise" at all is not established [inference].

### 4.2 Does the DSA apply to a non-commercial individual?

- DSA art. 2(1) covers intermediary services offered to recipients in the Union, whether or not the provider is established there [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065). Art. 3(g) defines intermediary services as information society services of three kinds, including hosting, which "consist[s] of the storage of information provided by, and at the request of" a recipient [fetched](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065).
- Whether a free archive is an information society service at all depends on whether it is normally provided for remuneration (Directive 2015/1535 art. 1(1)(b)), as the repository's legal research records, citing the directive text [fetched](https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:32015L1535) in that research. This is uncertain.
- Working assumption: the duties in section 4.1 apply, in particular arts. 16 to 18, because art. 19(1) does not exempt them. The exemption for Section 3 does not reach them [inference].

### 4.3 LCEN as amended (consolidated text on Legifrance dated 26 August 2026 for art. 6)

- Art. 6 I 2 defines a hosting provider by reference to DSA art. 3(g)(iii) [fetched, summarised](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000801164).
- Art. 6 IV A: hosting providers must promptly inform the competent authorities of the illegal activities that are reported to them and that recipients carry out. The list of offences includes the child offences in arts. 227-18 to 227-24 of the Code pénal and apology of terrorism (art. 421-2-5). Failure to inform carries one year's imprisonment and EUR 250,000 [fetched, summarised](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049577522). The text quoted in the search snippet is "elles informent promptement les autorités compétentes de toutes les activités illicites ... qui leur sont signalées" [search](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049577522).
- Conflict to resolve: a 2024 commentary says the LCEN then contained no general reporting provision for hosts after the DSA took effect [fetched](https://www.reynaud-avocat.com/2024/07/25/o%C3%B9-sont-pass%C3%A9es-les-dispositions-de-l-article-6-de-la-lcen-relatif-%C3%A0-la-responsabilit%C3%A9-des-h%C3%A9bergeurs-sur-internet/). The 2026 consolidated text includes IV A. The version that applies on the day of a report must be checked on Legifrance [inference].
- Art. 6-1 I: following an administrative request, child sexual abuse images must be removed within 24 hours, otherwise access providers may be ordered to block [fetched, summarised](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000801164). A criminal penalty for non-compliance is reported in secondary sources, which disagree on whether it exists [search](https://cms.law/fr/fra/news-information/censure-partielle-de-la-proposition-de-loi-sur-les-contenus-haineux-sur-internet).
- Art. 6 V A and V B: hosting providers must keep data that identify anyone who contributed to content, under the conditions of a decree; failure is punishable by one year and EUR 250,000 [fetched, summarised](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000801164). The decree's retention periods are in the repository's legal research, section 6, with its applicability left open [fetched in the legal research].
- Art. 6 VII: knowingly presenting content as illegal to obtain its removal is punishable by one year and EUR 15,000 [fetched, summarised](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000801164).
- Art. 1-1 II and art. 1-2: a non-professional publisher may publish only the host's name and address, and failure to comply with arts. 1-1 I and II is punishable by one year and EUR 75,000 for individuals [fetched, summarised](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000801164).

### 4.4 Reporting channels

- PHAROS: the government portal for reporting illegal online content, run by the police and gendarmerie in the OCLCTIC. It lists ten categories, including "endangering people" (with imminent threats to life), terrorism, threats or incitement to violence, child sexual abuse, incitement to hatred and online fraud. For an emergency it says to call 17 [fetched](https://www.police-nationale.interieur.gouv.fr/actualite/contenus-illicites-sur-internet-comment-fonctionne-portail-officiel-pharos). The 2014 hotline guide describes reports as "de simples renseignements", not complaints [fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le signalement".
- PHAROS address: the 2014 guide gives [www.internet-signalement.gouv.fr](https://www.internet-signalement.gouv.fr) [fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf). The police page says the platform is reached through the Ma Sécurité site [fetched](https://www.police-nationale.interieur.gouv.fr/actualite/contenus-illicites-sur-internet-comment-fonctionne-portail-officiel-pharos). The address itself returned an empty response on 2026-11-15. The current address is unverified.
- Point de Contact: an association run by the AFA (the French internet access providers' association), a member of INHOPE, which accepts reports of child sexual exploitation, hate speech and terrorist content [fetched](https://www.pointdecontact.net/). The reporting form is at [pointdecontact.net/signaler](https://www.pointdecontact.net/signaler/) [fetched](https://www.pointdecontact.net/). The 2014 guide says that embedding the form, rather than linking to it, requires AFA membership under its terms of use; this must be checked before any link is added [fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le signalement".
- INHOPE: 58 member hotlines in 53 countries [fetched](https://www.inhope.org/EN).
- A 2023 parliamentary question reports a funding reduction at Point de Contact and asks about continuity; not confirmed [search](https://www.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE4786.pdf). This is a dependency risk [inference].

### 4.5 Criminal law that bounds the moderator's handling

- Code pénal art. 227-23 (child sexual abuse images): fixing, recording or transmitting the image of a minor "en vue de sa diffusion" carries five years and EUR 75,000; offering, making available or distributing it carries the same penalties; habitual consultation of an online service offering such images, or acquiring or possessing one, carries five years and EUR 75,000. The article applies to images that appear to show a minor, unless the person was shown to be 18 when the image was made. No exemption for people who handle such images for reporting was found in the text [fetched, summarised](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043409170).
- The 2014 hotline guide quotes an older text of art. 227-23 with two years and EUR 30,000 for consultation and possession, and reads the offence as covering text as well as images [fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "La législation" and "Le traitement". The current penalty is the one above. The reading that the offence covers text is the guide's interpretation and must be confirmed for a text-based archive [inference].
- Code pénal art. 434-4 (destruction or concealment of an object that could help discover a crime): deleting material that could assist an investigation may fall under 434-4, and the hotline guide warns against deletion on that basis [search](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006418608/2021-08-26), [fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le traitement".
- Code pénal art. 434-1 (failure to report a crime): anyone who knows of a crime whose effects can still be prevented or limited must inform the judicial or administrative authorities. Family members (except where the crime is against a minor) and people bound by professional secrecy are excluded. The penalty is three years and EUR 45,000 in the base case [search](https://www.autonome-solidarite.fr/articles/la-non-denonciation-de-crimes-et-delits/). Read the Légifrance text before relying on it.
- Code pénal art. 434-3 covers failure to report ill-treatment or sexual offences against minors [search](https://violences-sexuelles.info/comprendre-definitions-loi/non-denonciation-et-intimidation/).
- Code pénal art. 223-6 (non-assistance to a person in danger): the first paragraph covers failure to stop a crime against bodily integrity, the second failure to help a person in peril, with five years and EUR 75,000, and seven years and EUR 100,000 when the victim is under 15 [search](https://kohenavocats.com/non-assistance-personne-en-danger-elements-constitutifs-peines-defense/). Not read on Legifrance.
- Code pénal art. 223-1-1 (doxxing): disclosing information that identifies or locates a person, to expose that person or their family to a direct risk of harm that the perpetrator could not have ignored, carries three years and EUR 45,000. It rises to five years and EUR 75,000 where the victim is a minor or particularly vulnerable, among other cases [fetched, summarised](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043974282).
- Loi du 29 juillet 1881 art. 24, seventh alinea: provoking discrimination, hatred or violence against a person or group because of origin, ethnicity, nation, race or religion carries one year and/or EUR 45,000 [fetched, summarised](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000043982456). Other grounds sit in other alineas, not read.

### 4.6 Data-protection clocks that touch moderation

- GDPR art. 12(3): a response to a data subject's request is due within one month, extendable by two months with notice of the extension and reasons [fetched](https://gdpr-info.eu/art-12-gdpr/).
- GDPR art. 33(1): notify the supervisory authority within 72 hours of becoming aware of a breach, where feasible; art. 33(5) requires documentation of every breach [fetched](https://gdpr-info.eu/art-33-gdpr/). The CNIL's notification service is at [notifications.cnil.fr](https://notifications.cnil.fr/notifications/) and is for controllers [fetched](https://www.cnil.fr/fr/services-en-ligne/notifier-une-violation-de-donnees-personnelles).

### 4.7 CSAM: what must not be done, and what to preserve

- Must not: possess or acquire, copy, record, transmit or distribute (art. 227-23 [fetched, summarised](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043409170)). The hotline guide applies this to hosts' staff.
- Must not delete the content as a first step (the hotline guide, [fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le traitement"; art. 434-4 as above).
- Should do: transmit it to the authorities as soon as it is qualified, take it offline, and suspend the associated account rather than delete content, according to the guide [fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le traitement".
- What the authorities do: PHAROS verifies the content, qualifies it, takes conservatory measures (keeping the content and investigation elements), and forwards it, with foreign content routed through Interpol [fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf), section "Le signalement".
- Gap: the sources read give no instruction for a small host that holds an item it must neither view, copy nor delete. This must be asked of the hotline or the authorities before launch [inference].

## 5. What this changes in the moderation design

1. Triage suspected CSAM on the text and metadata only, and never open media. The MVP's text-only scope reduces this risk, but a text description of a minor in a sexual context must still be treated as a suspected CSAM case [inference].
2. Add a quarantine state distinct from rejected: not published, not visible, not previewable, and not deleted. Each quarantined item needs an authority reference field.
3. Keep an escalation contact for the hosting provider and the domain registrar, with a documented response time. The mastodon.xyz case shows that an unanswered report can reach the domain level [fetched](https://stacks.stanford.edu/file/druid:vb515nd6874/20230724-fediverse-csam-report.pdf), section 2.1.
4. Publish the removal standard in plain terms, and cite the rule in each decision (repository constitution, practice 1 and 5).
5. Write a DSA-style statement of reasons template covering the facts, the rule, the legal basis and the redress route (art. 17(3)).
6. Offer a 30-day appeal, reviewed by someone other than the decider, as Mastodon does (voluntary, since art. 20 does not apply to micro and small providers) [fetched](https://help.joinmastodon.org/article/20-moderation-decisions-and-appeals).
7. Arrange an outside qualifier before launch, because the hotline guide advises that no one handle such content alone [fetched](https://www.pointdecontact.net/wp-content/uploads/2023/10/2014-04-guide_pedopornographie.pdf).
8. Keep the existing pending caps and bulk tools (ADR 0003), which match the volume problems above.

## 6. Open questions and dropped items

- Open: the current PHAROS address (section 4.4); whether a notice filed without viewing the content is accepted by Point de Contact or PHAROS [inference]; the penalty status of LCEN art. 6-1 (section 4.3); the scope of art. 434-1 and art. 223-6 (read on Legifrance); whether the art. 6 V A decree applies to the operator; whether the DSA covers a non-commercial archive as an information society service (section 4.2); the status of Mataroa's registrations and export tool.
- Dropped as unsubstantiated: the "Misskey to Mastodon" sequence in the February 2024 wave (one unverified comment); the 2024 New Media and Society paper on volunteer moderators (citation only); the Guardian report on Kenya (not reachable); the 2024 survey figure of 53 percent in clinical distress (search only, not opened).
