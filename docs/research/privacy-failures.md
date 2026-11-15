# The Artificial Intelligence Guestbook - Privacy failures research

Status: Research (2026-11-15)

## 1. Scope and method

This research looks at how privacy, anonymity, deletion and the protection of minors have failed in real systems, archives and publications, and turns those failures into design requirements for #14 (data model), #16 (deletion lifecycle), #17 (minors flow), #18 (retention schedule) and #27 (public filters).

It is not legal advice. Legal points are taken from the repository's [legal landscape research](legal-landscape.md) and are labelled where they are used.

Method: web searches, then pages read with WebFetch. Each claim carries one tag. [fetched] means the page was read in this session; for law-firm, press and encyclopedia pages, the claim is what that page reports and has not been checked against a primary source. [search] means the claim was seen only in search results or in a source that could not be read (several primary PDFs came back as unreadable binary: Sweeney's paper, the Article 29 Working Party opinion WP216, the INSEE secret-statistics guide, and the OHA 2018 principles). [inference] means a conclusion drawn by this document.

Not found or not verified: a numeric Eurostat cell threshold (the Eurostat guidance PDF was unreadable and no threshold was confirmed elsewhere); a CNIL position on backup retention periods (none was found in the CNIL pages and guides read); the Irish DPC primary decisions on TikTok and Instagram (the DPC press page did not list them, so the figures come from secondary reports); the Internet Archive's official removal policy (its help page returned HTTP 404).

## 2. Ranked lessons

Each lesson points to the cases in section 3 that support it. Ranking is by how much it changes the planned design.

1. Anonymity is lost through combinations of ordinary attributes, not through missing names. A ZIP code, birth date and sex identify most of a population, and a testimony is a self-description with far more fields. Cases 3.1, 3.2, 3.3, 3.4, 3.12.
2. Aggregates and filters leak. Small cells, differencing across tables and density maps reveal individuals even when each single number looks safe. Cases 3.5, 3.6, 3.11.
3. Writing style identifies people, and metadata removal cannot strip it. Stylometry works on short samples and, since 2026, LLM agents make it cheap at scale, so the archive cannot promise anonymity against a determined reader. Cases 3.7, 3.8, 3.9.
4. Timestamps, file metadata and location data identify people. A minute-level printer timestamp singled out one person; GPS tags in uploads exposed homes. Cases 3.10, 3.13, 3.14.
5. Reversible hashing and opaque pseudonymous identifiers are not anonymity. Cases 3.1, 3.12.
6. Copies outlive withdrawal. Case law and archives act at the access point (a search index, one archived article); third-party copies stay out of reach. Cases 3.16, 3.17, 3.18.
7. Erasure failures are judged as process failures: undocumented retention, late answers, and automatic deletion offered as if it were a reply. Retention statements must be true and checkable. Cases 3.14, 3.19.
8. Minors' data fails through public defaults, contact-detail exposure and nudges, and age checks fail in both directions while creating breach assets. Cases 3.20, 3.21, 3.22, 3.23.
9. Membership of a sensitive community can be special-category data even when nobody states it, and monitoring other people's speech fails even for good aims. Cases 3.15, 3.24.
10. Oral-history practice rests on consent, openness and negotiated restrictions. Public archives rely on statutory closure periods; the project has neither a closure law nor a legal mandate to lean on. Case 3.25.

## 3. Cases

### 3.1 AOL search logs, 2006

- What happened: On 4 August 2006 AOL Research published about 20 million search queries from more than 650,000 users over three months. AOL removed the file within days, but it had already been copied. The New York Times identified one user by matching the anonymous queries against phone-directory listings. [fetched] ([Wikipedia: AOL search log release](https://en.wikipedia.org/wiki/AOL_search_log_release))
- Cause: pseudonymous user numbers attached to free text that describes the person (places, health, family, local services).
- Lesson: an opaque ID is not anonymity when the content describes its author. Testimonies are self-descriptions, so the text is the identifier. [inference]

### 3.2 Netflix Prize dataset, 2007 to 2010

- What happened: Narayanan and Shmatikov showed that "anonymous" ratings of about 500,000 subscribers could be matched to identified IMDb profiles. The paper says an adversary "who knows only a little bit about an individual subscriber" can succeed. [fetched] ([arXiv cs/0610105](https://arxiv.org/abs/cs/0610105)) The paper appeared at IEEE S&P 2008 (DOI 10.1109/SP.2008.33). [search] ([Princeton publication record](https://collaborate.princeton.edu/en/publications/robust-de-anonymization-of-large-sparse-datasets/))
- Netflix dropped a planned second prize in March 2010 after an FTC inquiry and a privacy lawsuit. [search] ([EPIC archive, March 2010](https://archive.epic.org/2010/03/netflix-cancels-contest-over-p.html))
- Cause: sparse, high-dimensional records. A few known facts about one person select one record.
- Lesson: sharing any dataset of testimonies with several attributes invites linkage, even with random IDs. Research access must be controlled, not assumed safe. [inference]

### 3.3 Sweeney: ZIP code, birth date and sex, 2000

- What happened: Using 1990 census data, Sweeney found that 87% of the US population (216 million of 248 million) could be identified from a combination of 5-digit ZIP code, gender and date of birth. [fetched] ([Carnegie Mellon Data Privacy Lab](https://dataprivacylab.org/projects/identifiability/))
- Cause: quasi-identifiers that look harmless one at a time. No name is needed.
- Lesson: three coarse, ordinary attributes are enough at national scale. A testimony with optional age range, country, region, profession, organization and language carries more than three. [inference]

### 3.4 Rocher, Hendrickx and de Montjoye, 2019

- What happened: A generative model estimated that 99.98 per cent of Americans could be correctly re-identified in an "anonymised" dataset using 15 characteristics, such as age, gender and marital status. The paper was published in Nature Communications on 23 July 2019. [fetched] ([Imperial College London news](https://www.imperial.ac.uk/news/192112/anonymising-personal-data-enough-protect-privacy/))
- The paper's title speaks of "estimating" success on incomplete datasets, so the figure is a model output, not a count from a real attack. [inference, from the title in the same source]
- Lesson: incomplete data does not protect. Optional metadata is exactly partial data, and a few optional fields may be enough to single out a contributor. [inference]

### 3.5 US Census 2010: reconstruction from published tables

- What happened: The Census Bureau's own simulated attack, using only published aggregate tables, reconstructed records that matched the confidential 2010 microdata exactly for about 46 per cent of the population (about 142 million people), and within one year of age for 71%. [search] ([Abowd, Cornell blog](https://blogs.cornell.edu/abowd/special-materials/245-2/)) The official appendix gives 46.48%. [search] ([Census Bureau appendix B](https://www2.census.gov/about/policies/foia/records/disclosure-avoidance/appendix-b-summary-of-simulated-reconstruction-abetted-re-identification-attack.pdf))
- The Bureau adopted differential privacy for the 2020 census in response. [search] ([CES working paper 23-63](https://www2.census.gov/library/working-papers/2023/adrm/ces/CES-WP-23-63.pdf))
- Lesson: fine-grained published aggregates can be inverted back to records. Filter facets are aggregates, so they are a release of data about the contributors. [inference]

### 3.6 Small-cell rules at statistical offices

- What happened: INSEE's secret-statistics guide (September 2025 update) states that no table cell may cover fewer than three units, a rule set by a 1980 decision of its director general, and adds an 85% dominance rule. [search] ([INSEE guide](https://www.insee.fr/fr/statistiques/fichier/1300624/GUIDE%20DU%20SECRET%20STATISTIQUE%20MAJ%202509.pdf)) For the 2025 release of QPV data, INSEE moved from suppression alone to a random-key perturbation method. [search] ([INSEE blog](https://blog.insee.fr/qpv-nouvelle-methode-secret-statistique/))
- The UK Data Service handbook describes a threshold of at least three observations for frequency tables. [search] ([SDC handbook v2.0](https://ukdataservice.ac.uk/app/uploads/sdc-handbook-v2.0.pdf)) The ONS secure research service sets a default low-count threshold of 10 for one data set, and the ONS policies found disagree among themselves (3, 5 or 10 depending on product). [search] ([ONS SRS policy for DfE data](https://assets.publishing.service.gov.uk/media/69dcee3aeb7e7bc5651702be/Statistical_disclosure_control_policy_for_DfE_data_-_Office_for_National_Statistics_Secure_Research_Service.pdf))
- The Centre of Excellence SDC handbook says identification "may occur from any cells with a count of 1", that differencing can reveal small cells of 0, 1 or 2, and that suppression must be backed by secondary suppression so that protected cells cannot be derived from published totals. [fetched] ([SDC handbook, chapter 5](https://sdctools.github.io/HandbookSDC/05-frequency-tables.html))
- Cause: thresholds are applied per table. Each view can be safe alone and unsafe when several are compared.
- Lesson: there is no single standard threshold. The archive must pick one, and test it across combinations and across editions, because a withdrawal changes counts. [inference]

### 3.7 Juola's stylometric analysis of The Cuckoo's Calling, 2013

- What happened: Juola split the novel into 1,000-line chunks and compared them with four candidate authors (Rowling's The Casual Vacancy, and works by Ruth Rendell, P.D. James and Val McDermid), using four measures: word-length distribution, the 100 most common words, character 4-grams and word pairs. Rowling was the only candidate ranked first or second in every analysis. Juola wrote that "the most likely candidate author is probably Rowling", which he did not present as proof. [fetched] ([Language Log, 16 July 2013](https://languagelog.ldc.upenn.edu/nll/?p=5315))
- Rowling acknowledged authorship in July 2013. [search] ([NPR](https://www.npr.org/2013/07/26/205794448/uncovering-the-mystery-of-j-k-rowlings-latest-novel))
- A 2024 preprint disputes that the Burrows' Delta results clearly confirm the match. [search] ([arXiv 2407.10301](https://arxiv.org/pdf/2407.10301))
- Lesson: a full novel was not needed to shortlist a writer. When the candidate set is small, as in one contributor's circle of family and colleagues, a few thousand words can be enough. [inference]

### 3.8 Stylometry at scale, and LLM agents in 2026

- What happened: Narayanan and co-authors (IEEE Symposium on Security and Privacy, 2012) reported that, among up to 100,000 candidate authors, the classifier identified the anonymous author first in over 20% of cases and had the true author among its top 20 guesses in about 35% of cases. They warned that anonymous bloggers may be unmasked unless they obfuscate their style. [search] ([IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/6234420))
- In February 2026 Lermen et al. reported that LLM agents with web access reached up to 68% recall at 90% precision when linking pseudonymous accounts to real profiles, while the best non-LLM method was near 0%. They concluded that "the practical obscurity protecting pseudonymous users online no longer holds" and that matching takes "hours for a dedicated human investigator". [fetched] ([arXiv 2602.16800](https://arxiv.org/abs/2602.16800))
- Lesson: the archive cannot promise anonymity against style-based identification, and the cost of attempting it has fallen. Anonymous testimonies need a plain warning, and the project should not offer features that make style comparison easy (for example, "related testimonies" or author-similarity views). [inference]

### 3.9 The Unabomber manifesto, 1995 to 1996

- What happened: After the bomber demanded that a manifesto be printed, the New York Times and the Washington Post published it in September 1995. David Kaczynski recognised his brother's writing in it and contacted the FBI. Ted Kaczynski was arrested on 3 April 1996, the date most sources give. [search] ([Biography.com](https://www.biography.com/crime/a73873705/unabomber-manifesto-family-tip))
- Lesson: recognition by people who know the author needs no technology. An archive of testimonies will be read by family, colleagues and employers of the contributor, so anonymity against acquaintances is weaker than anonymity against strangers. [inference]

### 3.10 Reality Winner: printer tracking dots, 2017

- What happened: An internal audit found that six people had printed a classified NSA report. Yellow tracking dots on the printed pages, decoded by a security researcher, gave the printer serial number and the print time, 9 May at 6:20 p.m. Of the six, only one had emailed the outlet, from a work computer. [fetched] ([CBS News](https://www.cbsnews.com/news/nsa-leaker-reality-winner-secret-printer/))
- Lesson: one precise timestamp, combined with a small group of possible actors, identifies a person. Publication times can also be correlated with events the contributor is known to have attended. Public dates should be at day precision at most, with no time of day anywhere public. [inference]

### 3.11 Strava global heatmap, 2018

- What happened: Strava's public heatmap of aggregated fitness activity revealed the layout and routines of military bases. Strava said the map used only public activity and that privacy zones existed; The Register reported that the zones were not enabled by default. [search] ([The Register](https://www.theregister.com/2018/01/29/strava_heatmap_military_base_locations/))
- Lesson: aggregation protects individuals only where the crowd is large. Where few people are present, a density map is a per-person map. Geographic display must respect the same thresholds as tables. [inference]

### 3.12 NYC taxi trip data, 2014

- What happened: The city published 2013 trip records with taxi medallion and licence numbers hashed with MD5. Vijay Pandurangan reversed the hashes by computing them for every valid number in the small keyspace, and recovered pickup and drop-off data for about 173 million trips. [search] ([Route Fifty](https://www.route-fifty.com/management/2014/09/how-software-engineer-deanonymized-data-173-million-nyc-taxi-trips/93320/)) His write-up is at [Medium](https://medium.com/vijay-pandurangan/of-taxis-and-rainbows-f6bc289679a1). [search]
- Lesson: unsalted hashing of identifiers with a small or guessable space is not anonymisation. Any email- or IP-derived value in the design must be a keyed HMAC with the key held outside the database, or must not be stored. This confirms the caution already in the [threat model](../specs/threat-model.md). [inference]

### 3.13 Parler, 2021

- What happened: Roughly eight terabytes of public posts were scraped shortly before the platform went offline in January 2021. Wired reported that, because metadata had not been scrubbed, the GPS coordinates of many users' homes "had likely been exposed". [fetched] ([Wikipedia: Parler](https://en.wikipedia.org/wiki/Parler))
- Lesson: uploaded media carry location metadata. The testimony upload flow must strip EXIF, GPS and document properties at intake. [inference]

### 3.14 Whisper, 2014

- What happened: The Guardian alleged that Whisper tracked users who had opted out of geolocation and that its data was "stored indefinitely". Whisper's editor-in-chief said the app did not store coordinates from opt-out users and kept posts briefly under its terms. Four days after the report, Whisper changed its terms. [fetched] ([Engadget](https://www.engadget.com/2014/10/17/whisper-app-shares-location/))
- Lesson: a confessional service's location and retention claims were contested in public, and the operator's word was not checkable. The retention schedule must be specific, documented and auditable. [inference]

### 3.15 Samaritans Radar, 2014

- What happened: The charity's app scanned the public tweets of people a user followed to flag signs of distress. It was suspended nine days after launch, on 7 November 2014, after about 3,000 users had activated it, a petition and complaints to the UK Information Commissioner's Office. The charity later closed it permanently (announced March 2015). Users could only be "whitelisted" by sending a direct message to the charity. [fetched] ([Wikipedia: Samaritans Radar](https://en.wikipedia.org/wiki/Samaritans_Radar))
- Lesson: processing other people's speech without their consent fails even for good aims. The archive must not scan or score testimonies for third-party risk beyond moderation of what contributors publish. [inference]

### 3.16 Google Spain, 2014

- What happened: The Court of Justice (Grand Chamber, 13 May 2014, case C-131/12, ECLI:EU:C:2014:317) held that a search engine must remove from name-search results links to lawful third-party pages when the information is "inadequate, irrelevant or excessive", even if the page stays online. The data subject's rights generally override the operator's economic interest and the public's interest in name searches, unless the person plays a role in public life. The court also weighed the 16 years since publication. [fetched] ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62012CJ0131))
- Lesson: a remedy can remove the access point and leave the source untouched. Withdrawal must reach the project's own search indexes, and anonymous testimonies must not be retrievable by name or by metadata. [inference]

### 3.17 Hurbain v. Belgium, 2023

- What happened: On 4 July 2023 the Grand Chamber of the European Court of Human Rights, by 12 votes to 5, upheld an order that Le Soir anonymise (first name and surname) a 1994 article placed in its online archive in 2008. The court preferred anonymisation to removal, rejected an added note because it would keep the stigma alive, and accepted the Liège court's concern that the article would act as a "virtual criminal record". The original print archive stayed intact. [fetched] ([Inforrm](https://inforrm.org/2023/07/26/case-law-strasbourg-hurbain-v-belgium-grand-chamber-upholds-decision-that-order-anonymising-newspaper-archive-did-not-violate-article-10-hugh-tomlinson-kc/)) Application no. 57292/16. [search] ([judgment copy](https://www.concernedhistorians.org/le/782.pdf))
- Lesson: for archive copies, pseudonymising the record is a recognised, least-restrictive remedy, and the time elapsed matters. For editions, a pseudonymised revision is defensible; a visible note that repeats the subject is weaker. [inference]

### 3.18 Archived copies and the Internet Archive

- What happened: Removal from the Wayback Machine is handled case by case, by email, and robots.txt is reported as no longer a reliable removal tool; excluded material may still be stored in a non-public archive. [search] ([Forbes, 2016](https://www.forbes.com/sites/kalevleetaru/2016/01/18/the-internet-archive-turns-20-a-behind-the-scenes-look-at-archiving-the-web/)) The Internet Archive's own help page could not be read (HTTP 404). [fetched]
- In October 2024 an authentication database of 31 million records (email addresses, screen names, bcrypt-hashed passwords) was taken using a GitLab token exposed since 2022. Reports also describe a second intrusion into the support platform, with tickets dating back to 2018, some containing personal ID documents. [search] ([BleepingComputer, first breach](https://www.bleepingcomputer.com/news/security/internet-archive-hacked-data-breach-impacts-31-million-users/); [BleepingComputer, second breach](https://www.bleepingcomputer.com/news/security/internet-archive-breached-again-through-stolen-access-tokens/))
- Lesson: archives keep copies by design, and they are breach targets. The project should not hold email addresses alongside testimony text in one store, and its support channel must not accumulate ID documents. [inference]

### 3.19 CNIL sanction against Extia, 2026

- What happened: The CNIL restricted committee (deliberation SAN-2026-010 of 21 July 2026, published 9 September 2026) fined Extia EUR 300,000 for breaches of Articles 12 and 17 of the GDPR. The company had deleted the data of unshortlisted candidates after 60 days, a period that appeared in no internal document and was first raised in its reply to the sanction report. An automatic email had wrongly told candidates that data was kept for two years. At least 26 erasure requests were answered late, some after five or six months. The committee said the duty to respond is autonomous and cannot be offset by automatic erasure. [fetched] ([Legifrance](https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000054810440))
- The CNIL's erasure guidance says the request must be met as soon as possible and at the latest within one month, extendable to three months for complex requests, with reasons given. It names archiving in the public interest and freedom of expression as exceptions, and does not say how erasure applies to backups. [fetched] ([CNIL, droit à l'effacement](https://www.cnil.fr/fr/comprendre-mes-droits/le-droit-leffacement-supprimer-vos-donnees-en-ligne))
- Lesson: write the retention rule down before launch, make every user-facing statement match it, and answer every request within the deadline even when deletion happens automatically. [inference]

### 3.20 TikTok, Irish DPC, 2023

- What happened: The DPC adopted its final decision on 1 September 2023 and fined TikTok EUR 345 million; the announcement followed on 15 September 2023. [fetched] ([McCann FitzGerald](https://www.mccannfitzgerald.com/knowledge/data-privacy-and-cyber-risk/data-protection-commission-fines-tiktok-345-million-over-gdpr-infringements-in-processing-childrens-personal-data)) [search] ([Byrne Wallace Shields](https://byrnewallaceshields.com/news-and-recent-work/publications/dpc-calls-time-on-tiktoks-data-processing-practices-concerning-children.html))
- Findings, as summarised by McCann FitzGerald: child users' accounts were public by default, so their content reached an indeterminate audience (Articles 25(1), 25(2), 5(1)(c)); registration and posting pop-ups nudged users towards public settings, breaching fairness (Article 5(1)(a)); the DPIA did not assess the risk of under-13s on the platform (Article 24(1)); child users were not told the categories of recipients (Article 13(1)(e)). The DPC acknowledged there is no "perfect age verification method". Remedies: a reprimand, an order to comply within three months, and the fine. [fetched] (McCann FitzGerald, above)
- Lesson: public-by-default settings and nudges are the enforcement pattern for minors. The minors flow must default to private, use neutral choice screens and collect only what it needs. [inference]

### 3.21 Instagram, Irish DPC, 2022

- What happened: The DPC's EUR 405 million fine was announced in the first week of September 2022. A DPC spokesperson said the final decision had been adopted "last Friday"; some reports date it to 2 September 2022, an inference from that phrase. The inquiry began when a data scientist found that users under 18 who switched to business accounts had their contact information, including email addresses and phone numbers, displayed on their profiles. [fetched] ([Euronews](https://www.euronews.com/next/2022/09/06/ireland-fines-instagram-405-million-over-protection-of-childrens-data))
- The EDPB describes a second subject: public-by-default personal accounts of children. [search] ([EDPB](https://www.edpb.europa.eu/news/news/2022/record-fine-instagram-following-edpb-intervention_es)) Meta said it would appeal. [search] ([Irish Times](https://www.irishtimes.com/technology/2022/09/05/irish-data-protection-commissioner-fines-instagram-405m/))
- Lesson: never display contact details for minors, and never offer them as an option. The archive has no contact fields, and moderation checks minors' texts for pasted contact details. [inference]

### 3.22 Age assurance: why checks fail

- What happened: The CNIL's page on online age verification (publication date 22 September 2022) says that age verification "is likely to alter the protection of the Internet user's privacy", that current systems are "circumventable and intrusive", that sites should rely on trusted third parties, and that "there is currently no solution that satisfactorily meets these three requirements". [fetched] ([CNIL](https://www.cnil.fr/en/online-age-verification-balancing-privacy-and-protection-minors))
- CNIL Recommendation 7 (dated 1 June 2021) says purely declarative systems should be excluded for higher-risk processing, that email verification is easily circumvented by minors, that verification data should not be kept once the check is complete, and that collection should be limited to what is strictly necessary. [fetched] ([CNIL, Recommendation 7](https://www.cnil.fr/fr/recommandation-7-verifier-lage-de-lenfant-et-laccord-des-parents-dans-le-respect-de-sa-vie-privee))
- CNIL Recommendation 4 is cited for parental consent for minors under 15. [search] ([Lexis Veille](https://www.lexisveille.fr/droits-numeriques-des-mineurs-les-recommandations-de-la-cnil))
- A UK government survey (May 2026) of 2,299 children found that nearly two in five aged 11 to 17 said they had got past an online age check, most by giving a false date of birth. [search] ([MediaNama](https://www.medianama.com/2026/07/223-uk-children-bypass-age-checks/))
- Lesson: self-declared age is the default failure mode, and verification is circumvented and creates a data store. Under-15 handling in France needs a designed co-consent flow; a bare email is the weakest option. [inference]

### 3.23 Breaches of verification material, 2025

- What happened: In October 2025 Discord disclosed that a third-party customer-support vendor, used for age-related appeals, had been breached; about 70,000 users may have had government ID photos exposed; names, emails and partial card details were also reported. [search] ([TechCrunch](https://techcrunch.com/2025/10/09/discord-suffers-data-breach-impacting-at-least-70000-users/))
- In July 2025 the dating-safety app Tea reportedly left a cloud storage archive unsecured, holding about 72,000 images, including around 13,000 verification selfies and ID photos. [search] ([Security.org](https://www.security.org/identity-theft/breach/tea-app/))
- Lesson: any selfie or ID kept for verification or appeals becomes a breach asset, including at vendors. The design should not collect such material; if the owner accepts a verification step, it should use a processor under a DPA that deletes the material after the check. [inference]

### 3.24 Grindr, Norway, 2021 to 2025

- What happened: Datatilsynet fined Grindr NOK 65 million in December 2021 for sharing personal data with advertising partners. [search] ([Digital Policy Alert](https://digitalpolicyalert.org/event/14736-issued-ruling-upholding-datatilsynet-nok-65-million-fine-on-grindr)) The Borgarting Court of Appeal upheld the fine on 21 October 2025, finding that "data about the use of the app is special category personal data" and that Grindr lacked valid consent to share it. [fetched] ([Datatilsynet](https://www.datatilsynet.no/en/news/news-2025/the-court-of-appeal-upholds-the-fine-against-grindr/))
- Lesson: data showing membership of a sensitive community is special-category data even when nobody states it. Analytics, filters and exports must not reveal sensitive membership, even by inference. [inference]

### 3.25 Oral-history archives: consent, withdrawal and closure

- What happened: The UK Oral History Society says that requests to delete archived interview material "does not normally apply" as erasure for historical research. It notes that consent can be withdrawn, so it recommends a public-task or legitimate-interests basis for archives, and it says consent-based open licences are not appropriate for most oral history work. [fetched] ([Oral History Society, GDPR guidance](https://ohs.org.uk/gdpr-2/))
- The same OHS guidance advises parental consent for children under 16, plus the child's own consent from 13, and says the child's consent or withdrawal prevails in a conflict. [fetched] (same page)
- The US Oral History Association's principles say narrators may refuse topics, restrict access and choose anonymity, and that informed consent does not cover copyright. [search] ([OHA 2018 principles](https://www.oralhistory.org/wp-content/uploads/2019/03/OHA-Principles-and-Best-Practices-Adopted-2018.pdf); [OHA glossary](https://oralhistory.org/best-practices-glossary/)) Its best-practices page warns that subpoenas or open-records requests may make some restrictions unenforceable. [search] ([OHA best practices](https://oralhistory.org/best-practices/))
- French public archives use statutory closure periods: 50 years from the most recent document for files whose disclosure would harm privacy, and 25 years after death for medical secrecy. [fetched] ([Legifrance, Code du patrimoine L213-2](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043887707))
- Lesson: a private archive has no closure law to fall back on; the repository's legal research concludes that the public-task basis is not available to a private individual ([legal landscape, executive summary](legal-landscape.md)). Its protection is consent, withdrawal and redaction, and each must be stated honestly. Restrictions a narrator is promised must be technically enforceable. [inference]

## 4. Requirements

Each requirement is an inference from the lessons and cases in brackets. Items marked "owner decision" need a value that the research cannot supply.

### 4.1 For #14 (data model)

- R14.1 Classify every field as public, private or operational. Optional metadata stays individually optional, and nothing is set automatically for anonymous testimonies (no IP, user agent, device or time of day). [lessons 1, 4; 3.1, 3.2]
- R14.2 Store submission and publication instants as private timestamps. Publish only the day, never the time of day. [lesson 4; 3.10]
- R14.3 Keep the account email in a table with no path to testimony content in exports. Any email-derived value is a keyed HMAC, with the key held outside the database, or is not stored. [lesson 5; 3.12]
- R14.4 Strip EXIF, GPS and document properties from every upload, and re-encode images before storage. [lesson 4; 3.13]
- R14.5 No fields for ID documents, selfies, contact details or verification results. If a minors flow needs a status, it stores an outcome flag only. [lesson 8; 3.23]
- R14.6 Record redaction and withdrawal as state transitions on the same internal ID, never as copies of text. Original and redacted versions are classified separately. [lesson 6; 3.17]
- R14.7 Public IDs are random and never derived from internal IDs, dates or counts. Exports carry no sequence that reveals submission order. [identifiers spec; 3.1]

### 4.2 For #16 (deletion lifecycle)

- R16.1 Open a deletion record on receipt with the one-month deadline. Answer within the deadline even when deletion is automatic, and record any extension with its reasons. [lesson 7; 3.19]
- R16.2 Keep a store-by-store deletion table (database, search index, caches, exports, translations, moderation tools, generated files, backups, mirror list), with a test for each store. [deletion philosophy, principle 2; 3.16]
- R16.3 Remove withdrawn testimonies from name and full-text indexes at withdrawal, not at the next rebuild. [3.16]
- R16.4 Publish a backup rotation period and an erase-on-restore step. No CNIL backup rule was found, so the period is an owner decision. [3.19; owner decision]
- R16.5 Tombstone content: public ID, status "withdrawn" and month of withdrawal. No content, no contributor metadata and no hash of the email. [deletion philosophy, principle 4; 3.12]
- R16.6 Publish a machine-readable withdrawal list that mirrors can poll, and state in the terms that third-party copies are outside the project's control. [lesson 6; 3.17, 3.18]
- R16.7 Support tickets must not carry ID documents. Any that arrive are deleted under the same deletion record. [3.18, 3.23]
- R16.8 Redaction notes say that text was removed and never repeat its subject. Whether a visible note appears in editions is an owner decision. [3.17]

### 4.3 For #17 (minors flow)

- R17.1 A testimony from a self-declared minor is unpublished by default and goes public only after a separate, explicit choice. No option is pre-selected. [3.20; lesson 8]
- R17.2 Minors' records show no age, no age range and no contact details publicly. Public filters exclude age for contributions by under-18s. [3.21; legal landscape, section 4]
- R17.3 Do not use third-party identity or age verification that stores documents. If a check is required, use a method the owner documents as weak, and delete verification data once the check is complete. [3.22, 3.23; CNIL Recommendation 7]
- R17.4 For under-15s in France the owner chooses between refusing them, requiring a designed co-consent flow, or accepting self-declaration with the residual risk recorded in the DPIA. Bare email confirmation is the weakest option. [owner decision; 3.22]
- R17.5 A person who contributed as a minor can withdraw without a parent's approval, and a child's withdrawal prevails over a parent's consent. [3.25; legal landscape, section 4]
- R17.6 Minors' testimonies get a second moderation pass for third-party data and contact details before publication. [3.21]
- R17.7 Publication choice screens are neutral: no default-public state and no pop-up that nudges. [3.20]

### 4.4 For #18 (retention schedule)

- R18.1 Write the schedule before launch. Every automatic deletion rule matches the text users see. A rule that appears only in a reply to a regulator does not count. [3.19]
- R18.2 Application logs contain no testimony text, email or full IP address. Proxy logs are kept short. Final values are set in this schedule. [threat model, section 3.6; 3.14]
- R18.3 Support tickets have a short retention and are purged on closure. [3.18, 3.23]
- R18.4 Verification data, if any exists, is deleted once the check is complete. [3.22]
- R18.5 Withdrawal records keep the request date and the outcome, not the content. Their period follows limitation periods, to be confirmed by a lawyer. [legal landscape, section 12]
- R18.6 Once a year, the custodian checks the schedule against live systems and the consent text. [3.14, 3.19]
- R18.7 The backup period, and the time needed to re-apply withdrawals after a restore, appear in the schedule and in the consent text. [3.19; owner decision]

### 4.5 For #27 (public filters)

- R27.1 A filter value is shown only when at least N published testimonies match it. N is an owner decision; 10 is proposed as the starting point. INSEE uses 3 for enterprise tables and one UK service defaults to 10. Testimonies are richer rows than statistical cells, so the higher figure is the safer default. [3.6; inference]
- R27.2 Combinations are checked too. A filter result below N is not shown, even when each single value passes. [3.5, 3.6]
- R27.3 Facet counts are computed on the public set only, and are rounded or withheld. A withdrawal between two views can reveal the removed item by difference. [3.6]
- R27.4 No filter on age, religion, health, sexuality, minor status or other special-category content, even when the field is optional. No filter pairs profession with organization or country. [3.2, 3.24]
- R27.5 Geography shows country by default. Region appears only where R27.1 holds. No map below country level. [3.3, 3.11]
- R27.6 Listings show publication year and month. The testimony page shows the day, for citation (owner decision). No time of day is shown anywhere. [3.10]
- R27.7 Sorting by publication date uses the day. Ties are broken by public ID, not by submission order. [3.1, 3.10]
- R27.8 Name-based search covers only display names that contributors chose. Anonymous and pseudonymous testimonies are not retrievable by any metadata. [3.16, 3.17]
- R27.9 No "related testimonies" feature, no author-similarity feature and no display of writing-style statistics. [3.8]
- R27.10 Exports and editions apply R27.1 to R27.8 by construction. A test cross-tabulates exported fields against the thresholds. [threat model, section 3.6; 3.5]

## 5. Honest limits, and suggested consent wording

What the project cannot promise to contributors:

- Protection against stylometric identification, even when no name or metadata is published. [3.8]
- Anonymity from the operator. The operator holds the account email and can link it to a testimony; anonymity is toward the public and third parties. [inference, from the threat model's asset list]
- Recall of copies downloaded, mirrored or archived by others. [3.16, 3.18]
- Removal from backups before the rotation period ends. [3.19; owner decision]
- Removal from search engines that have already indexed a page, beyond what the project can request. [3.16]
- Protection from people who know the author. Recognition needs no technology. [3.9]
- Prevention of re-identification from what the contributor chooses to write. [3.1, 3.4]
- Withdrawal where a legal retention duty applies. [legal landscape, section 6]
- Protection of timing. A publication date can be correlated with events. [3.10]

Suggested consent wording, in English, for drafting. The French public text must be written and reviewed separately, and the wording must be checked by a French lawyer before publication.

```text
Your testimony will be published on the Guestbook and kept for the long term, including in downloadable editions that others may copy.

If you publish anonymously or under a pseudonym, we do not publish your name, your email address or any link to your account. We cannot promise that no one will recognise you. Your writing style, the events you describe, places, dates and the people you mention can point to you, especially for people who know you.

You can publish only your text and none of the optional details. Each optional detail, such as country, region, profession or organization, can make you easier to identify when combined with the others.

If you withdraw your testimony, we remove it from the site, from the search index and from future editions, and we publish a withdrawal notice that mirrors can use. We cannot remove copies that others have already downloaded or archived. Our backups keep withdrawn material for up to [backup period, to be set by the owner] before they are overwritten.

Before you publish, check your text for names of other people, contact details and anything you do not want to be public.
```

The sentence about identity checks was left out on purpose; if the minors flow requires an age check, the text must say so.

## 6. Open questions for the owner

1. What is the threshold N for filter values and for combinations (R27.1, R27.2)? Check whether the archive will ever reach N for rarer filters, and whether those filters should exist at all.
2. Are under-15s accepted, and if so by which co-consent method (R17.4)? Refusing under-15s is the simplest option and needs no verification.
3. If a minors flow needs an age check, the statement "we do not check your identity" in the consent text must change. Which is it?
4. Date precision: month and year on listings with the day on the testimony page, or month only (R27.6)?
5. What backup rotation period is acceptable, and is erase-on-restore workable operationally (R16.4, R18.7)?
6. Does withdrawal depend on the account email, which is the only link between a person and their testimonies, or on a one-time withdrawal code shown at publication and stored hashed? Each option has a failure mode: a lost code cannot be recovered, and an email link keeps the operator able to connect the two.
7. Should facet counts exist at all, or should listings be unfaceted (R27.3)?
8. Should editions carry a visible redaction note, given that the Hurbain court rejected a note as perpetuating stigma (R16.8)?
9. Should anonymous contributors see a stylometry warning before they submit (lesson 3)?
10. Is a yearly retention audit (R18.6) accepted as a custodial duty?

## 7. Sources

### 7.1 Repository documents

- [Legal landscape research](legal-landscape.md)
- [Privacy assumptions](../constitution/privacy-assumptions.md)
- [Deletion philosophy](../constitution/deletion-philosophy.md)
- [Threat model](../specs/threat-model.md)
- [Identifiers and permanent URLs](../specs/identifiers.md)

### 7.2 Re-identification and statistical disclosure

- [Wikipedia: AOL search log release](https://en.wikipedia.org/wiki/AOL_search_log_release)
- [arXiv cs/0610105, Narayanan and Shmatikov](https://arxiv.org/abs/cs/0610105)
- [Princeton publication record, Netflix de-anonymization](https://collaborate.princeton.edu/en/publications/robust-de-anonymization-of-large-sparse-datasets/)
- [EPIC archive, Netflix cancels contest, March 2010](https://archive.epic.org/2010/03/netflix-cancels-contest-over-p.html)
- [Carnegie Mellon Data Privacy Lab, identifiability project](https://dataprivacylab.org/projects/identifiability/)
- [Imperial College London news, Rocher et al. 2019](https://www.imperial.ac.uk/news/192112/anonymising-personal-data-enough-protect-privacy/)
- [Abowd, Cornell blog, 2010 census reconstruction](https://blogs.cornell.edu/abowd/special-materials/245-2/)
- [Census Bureau, appendix B, simulated reconstruction attack](https://www2.census.gov/about/policies/foia/records/disclosure-avoidance/appendix-b-summary-of-simulated-reconstruction-abetted-re-identification-attack.pdf)
- [Census Bureau CES working paper 23-63](https://www2.census.gov/library/working-papers/2023/adrm/ces/CES-WP-23-63.pdf)
- [INSEE, Guide du secret statistique, September 2025](https://www.insee.fr/fr/statistiques/fichier/1300624/GUIDE%20DU%20SECRET%20STATISTIQUE%20MAJ%202509.pdf)
- [INSEE blog, QPV and the new method](https://blog.insee.fr/qpv-nouvelle-methode-secret-statistique/)
- [UK Data Service, Handbook on SDC for outputs v2.0](https://ukdataservice.ac.uk/app/uploads/sdc-handbook-v2.0.pdf)
- [ONS SRS, SDC policy for DfE data](https://assets.publishing.service.gov.uk/media/69dcee3aeb7e7bc5651702be/Statistical_disclosure_control_policy_for_DfE_data_-_Office_for_National_Statistics_Secure_Research_Service.pdf)
- [Centre of Excellence SDC handbook, chapter 5](https://sdctools.github.io/HandbookSDC/05-frequency-tables.html)

### 7.3 Stylometry, LLMs and timing

- [Language Log, Patrick Juola, 16 July 2013](https://languagelog.ldc.upenn.edu/nll/?p=5315)
- [NPR, Rowling and the Cuckoo's Calling, July 2013](https://www.npr.org/2013/07/26/205794448/uncovering-the-mystery-of-j-k-rowlings-latest-novel)
- [arXiv 2407.10301, Burrows' Delta and the Rowling case](https://arxiv.org/pdf/2407.10301)
- [IEEE Xplore, Narayanan et al., internet-scale author identification (2012)](https://ieeexplore.ieee.org/abstract/document/6234420)
- [arXiv 2602.16800, Lermen et al., large-scale online deanonymization with LLMs](https://arxiv.org/abs/2602.16800)
- [Biography.com, Unabomber manifesto and family tip](https://www.biography.com/crime/a73873705/unabomber-manifesto-family-tip)
- [CBS News, Reality Winner and printer tracking dots](https://www.cbsnews.com/news/nsa-leaker-reality-winner-secret-printer/)
- [The Register, Strava heatmap, January 2018](https://www.theregister.com/2018/01/29/strava_heatmap_military_base_locations/)
- [Route Fifty, NYC taxi data de-anonymized, 2014](https://www.route-fifty.com/management/2014/09/how-software-engineer-deanonymized-data-173-million-nyc-taxi-trips/93320/)
- [Medium, Vijay Pandurangan, of taxis and rainbows](https://medium.com/vijay-pandurangan/of-taxis-and-rainbows-f6bc289679a1)
- [Wikipedia: Parler](https://en.wikipedia.org/wiki/Parler)
- [Engadget, Whisper location report, October 2014](https://www.engadget.com/2014/10/17/whisper-app-shares-location/)
- [Wikipedia: Samaritans Radar](https://en.wikipedia.org/wiki/Samaritans_Radar)

### 7.4 Archives, removal and deletion

- [EUR-Lex, judgment C-131/12 Google Spain](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62012CJ0131)
- [Inforrm, Hurbain v. Belgium Grand Chamber, 2023](https://inforrm.org/2023/07/26/case-law-strasbourg-hurbain-v-belgium-grand-chamber-upholds-decision-that-order-anonymising-newspaper-archive-did-not-violate-article-10-hugh-tomlinson-kc/)
- [Judgment copy, Hurbain v. Belgium (application 57292/16)](https://www.concernedhistorians.org/le/782.pdf)
- [Forbes, how the Internet Archive handles removals, 2016](https://www.forbes.com/sites/kalevleetaru/2016/01/18/the-internet-archive-turns-20-a-behind-the-scenes-look-at-archiving-the-web/)
- [BleepingComputer, Internet Archive breach, October 2024](https://www.bleepingcomputer.com/news/security/internet-archive-hacked-data-breach-impacts-31-million-users/)
- [BleepingComputer, Internet Archive breached again through stolen tokens](https://www.bleepingcomputer.com/news/security/internet-archive-breached-again-through-stolen-access-tokens/)
- [Legifrance, CNIL deliberation SAN-2026-010 (Extia)](https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000054810440)
- [CNIL, right to erasure guidance](https://www.cnil.fr/fr/comprendre-mes-droits/le-droit-leffacement-supprimer-vos-donnees-en-ligne)

### 7.5 Minors, age assurance and breaches of verification data

- [McCann FitzGerald, DPC fines TikTok EUR 345 million](https://www.mccannfitzgerald.com/knowledge/data-privacy-and-cyber-risk/data-protection-commission-fines-tiktok-345-million-over-gdpr-infringements-in-processing-childrens-personal-data)
- [Byrne Wallace Shields, DPC calls time on TikTok's processing of children's data](https://byrnewallaceshields.com/news-and-recent-work/publications/dpc-calls-time-on-tiktoks-data-processing-practices-concerning-children.html)
- [Euronews, Ireland fines Instagram EUR 405 million, September 2022](https://www.euronews.com/next/2022/09/06/ireland-fines-instagram-405-million-over-protection-of-childrens-data)
- [Irish Times, Instagram fine, September 2022](https://www.irishtimes.com/technology/2022/09/05/irish-data-protection-commissioner-fines-instagram-405m/)
- [EDPB, record fine for Instagram following EDPB intervention](https://www.edpb.europa.eu/news/news/2022/record-fine-instagram-following-edpb-intervention_es)
- [CNIL, online age verification: balancing privacy and protection of minors](https://www.cnil.fr/en/online-age-verification-balancing-privacy-and-protection-minors)
- [CNIL, Recommendation 7: verify the child's age and parental consent](https://www.cnil.fr/fr/recommandation-7-verifier-lage-de-lenfant-et-laccord-des-parents-dans-le-respect-de-sa-vie-privee)
- [Lexis Veille, CNIL recommendations on minors' digital rights](https://www.lexisveille.fr/droits-numeriques-des-mineurs-les-recommandations-de-la-cnil)
- [MediaNama, UK children bypassing age checks, 2026](https://www.medianama.com/2026/07/223-uk-children-bypass-age-checks/)
- [TechCrunch, Discord vendor breach, October 2025](https://techcrunch.com/2025/10/09/discord-suffers-data-breach-impacting-at-least-70000-users/)
- [Security.org, Tea app breach, 2025](https://www.security.org/identity-theft/breach/tea-app/)
- [Digital Policy Alert, Grindr fine upheld](https://digitalpolicyalert.org/event/14736-issued-ruling-upholding-datatilsynet-nok-65-million-fine-on-grindr)
- [Datatilsynet, Court of Appeal upholds the fine against Grindr](https://www.datatilsynet.no/en/news/news-2025/the-court-of-appeal-upholds-the-fine-against-grindr/)

### 7.6 Oral history and archives law

- [Oral History Society, GDPR guidance](https://ohs.org.uk/gdpr-2/)
- [OHA Principles and Best Practices (2018)](https://www.oralhistory.org/wp-content/uploads/2019/03/OHA-Principles-and-Best-Practices-Adopted-2018.pdf)
- [OHA glossary](https://oralhistory.org/best-practices-glossary/)
- [OHA best practices](https://oralhistory.org/best-practices/)
- [Legifrance, Code du patrimoine, article L213-2](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043887707)
