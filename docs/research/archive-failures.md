# Archive failures and survivors

Status: Research (2026-11-15)

Issue: #13

## 1. Scope and method

This research asks how archives, testimony collections and digital-preservation efforts have failed or nearly failed, what the survivors did, and which requirements follow for the canonical archive format and edition packaging (issue #13, which will produce `docs/specs/archive-format.md`). It was written against [AGENTS.md](../../AGENTS.md), [the archival model](../constitution/archival-model.md), [the deletion philosophy](../constitution/deletion-philosophy.md), [ADR 0006](../decisions/0006-archive-first-replaceable-application.md), [the identifiers specification](../specs/identifiers.md) and section 4 of [the domain and persistence research](domain-and-persistence.md).

Searches and page fetches were run on 2026-11-15. Every factual claim carries one tag. [fetched] means the page was opened with WebFetch, or a PDF was extracted to text with pdftotext, and the claim appears in the returned text. WebFetch returns a model-written digest, so text in quotation marks is as the digest rendered it. Where a fetched page is secondary, such as Wikipedia, the bullet says so. [search] means the claim appears only in a search-result snippet and was not verified. [inference] means the claim is my reasoning from the cited sources, not a statement by them.

Some pages could not be opened: the ISO page returned 403, CNN returned 451 and an NPR fetch timed out. Claims that rest on those are tagged [search]. The 2023 to 2026 British Library facts come from a secondary summary, and the Internet Archive litigation facts come from search snippets; both should be checked against primary reports before any public use.

## 2. Ranked lessons

Each lesson lists the cases (section 3) that support it. The ranking reflects how much each lesson changes the planned design.

1. A single copy does not survive, and bytes change silently. Independent copies, fixity manifests and a repair path are the minimum (cases 3.4, 3.5, 3.10, 3.12).
2. The canonical bytes must be readable by a stranger with no platform, application, decoder or original hardware. Platform exports and opaque binaries are where content is lost (cases 3.3, 3.6, 3.7, 3.8).
3. Promise contributors only what the custodian controls. An archive cannot promise immunity from lawful compulsion, and its confidentiality text must say so (case 3.2).
4. Decide access, embargo, licence and withdrawal rules before collecting, not after. Terms change and platforms change them (cases 3.1, 3.9, 3.13).
5. Bulk download must not depend on login, CAPTCHA or per-item requests, and every edition must state what it does not contain (cases 3.6, 3.7, 3.5).
6. Custody must outlive the founder, the host and the web copy. Migrations and web relaunches break links and can take content offline (cases 3.3, 3.14, 3.15).
7. Identifiers and citations rot unless the archive carries its own identity inside each package (case 3.11).
8. Operational stores holding personal data are attack targets, and restoring them takes years (cases 3.12, 3.13).
9. Standards help, but tooling is thin and some standards conflict with deletion. The simplest transfer container is the safest choice (case 3.18).
10. Plain UTF-8 text with JSON and CSV is defensible for canonical content. Markdown has no single standard and is absent from the Library of Congress list (case 3.19).

## 3. Cases

### 3.1 Library of Congress Twitter archive (2010 to 2017)

- What happened: in 2010 the Library announced a gift from Twitter of the public tweet archive, beginning with 2006 tweets and continuing forward. [fetched] <https://blogs.loc.gov/loc/2017/12/update-on-the-twitter-archive-at-the-library-of-congress/>
- On 26 December 2017 the Library announced that from 1 January 2018 it would acquire tweets selectively. The 2006 to 2017 collection stays embargoed "until access issues can be resolved in a cost-effective and sustainable manner". [fetched] <https://blogs.loc.gov/loc/2017/12/update-on-the-twitter-archive-at-the-library-of-congress/>
- Cause, as the Library gives it: a sharp rise in platform use and new platforms, terms of service and functionality "shifting frequently", and "lessons learned about privacy and other concerns". The post gives no volume figures. [fetched] <https://blogs.loc.gov/loc/2017/12/update-on-the-twitter-archive-at-the-library-of-congress/>
- Access was the failure point: tweets could not be made available for bulk download and researchers struggled to search them. [search] <https://www.academia.edu/38380877/_Archiving_and_Preserving_Social_Media_at_the_Library_of_Congress_Institutional_and_Cultural_Challenges_to_Build_a_Twitter_Archive_>
- Lesson: the collection was taken before an access model, terms of reuse and a scope rule existed. The guestbook's cut-off and publication rules (archival model, property 2) must be settled before the first edition. [inference]
- Lesson: the archive should own a copy it can publish, not rely on a platform's terms or feed. [inference, ADR 0006]

### 3.2 Boston College Belfast Project (oral history, 2000 to 2014)

- What happened: the project launched in 2000 and interviews concluded in 2006. Boston College signed an agreement with Ed Moloney that guaranteed interviewee confidentiality "to the extent American law allows". [fetched, secondary] <https://en.wikipedia.org/wiki/Belfast_Project>
- In May and August 2011, US Department of Justice subpoenas were issued under the US-UK Mutual Legal Assistance Treaty at the request of the Police Service of Northern Ireland (PSNI). [fetched, secondary] <https://en.wikipedia.org/wiki/Belfast_Project>
- The district court ordered release of 85 interviews of eight people. The First Circuit narrowed the order to 11 interviews of seven people, relevant to the 1972 killing of Jean McConville. [fetched] <https://www.wbur.org/news/2013/06/02/bc-release-ira-tapes>
- The appeals court said: "The choice to investigate criminal activity belongs to the government and is not subject to veto by academic researchers." [fetched, secondary] <https://en.wikipedia.org/wiki/Belfast_Project>
- The Supreme Court declined to hear the challenge in April 2013. [search] <https://www.wbur.org/news/2013/04/15/ira-tapes-boston-college>
- In 2014 Boston College terminated the project and offered to return materials to living participants on request. [fetched, secondary] <https://en.wikipedia.org/wiki/Belfast_Project>
- In 2018 the PSNI subpoenaed the recorded interview of interviewer Anthony McIntyre, and in April 2024 courts ruled for the PSNI. This rests on one secondary source and should be verified before citing. [fetched, secondary] <https://en.wikipedia.org/wiki/Belfast_Project>
- Cause: the confidentiality promise was conditional on law, and the materials sat in a jurisdiction and institution that a treaty request could reach. [fetched, secondary] <https://en.wikipedia.org/wiki/Belfast_Project>
- Lesson: an archive can promise what it controls: custody, what it holds, access rules and how it answers requests. It cannot promise that a court or police will not compel disclosure. The contributor text must say so, for example "to the extent French and EU law allows". [inference]
- GDPR article 89 requires "appropriate safeguards" for processing for archiving purposes in the public interest, including data minimisation and pseudonymisation where those purposes can be fulfilled that way. Member-state law may restrict some data-subject rights where exercising them would seriously impair those purposes. [fetched] <https://gdpr-info.eu/art-89-gdpr/>
- Lesson: minimise what could be compelled. Keep names and contact data out of the archival packages, and hold any link between a public ID and a person only in the operational store, with a retention limit. This follows archival model property 7 and identifiers section 1. [inference]
- Lesson: embargoes are weaker than they look. The Oral History Association's 2018 principles warn that subpoenas and open-records requests may make restrictions unenforceable. [search] <https://www.oralhistory.org/wp-content/uploads/2019/03/OHA-Principles-and-Best-Practices-Adopted-2018.pdf>

### 3.3 BBC Domesday Project (1986; obsolescence and recovery)

- What happened: published in 1986 to mark 900 years since the Domesday Book, on two LV-ROM laserdiscs of about 300 MB per side. Viewing needed a BBC Master with a SCSI controller and a Philips VP415 player. [fetched, secondary] <https://en.wikipedia.org/wiki/BBC_Domesday_Project>
- In 2002 "concerns emerged over the potential unreadablility of the discs" as compatible computers and drives became scarce. [fetched, secondary] <https://en.wikipedia.org/wiki/BBC_Domesday_Project>
- The 2002 CAMiLEON project (Leeds and Michigan) built an emulation route: text and database files were copied to Linux, and images were digitised uncompressed at about 70 GB per disc side. [fetched, secondary] <https://en.wikipedia.org/wiki/BBC_Domesday_Project>
- In 2003 a National Archives team located the original 1-inch videotape masters and archived them to Digital Betacam. [fetched, secondary] <https://en.wikipedia.org/wiki/BBC_Domesday_Project>
- A Windows PC version reverse-engineered from a Community disc went online in July 2004 and was taken offline early in 2008, after its programmer died. [fetched, secondary] <https://en.wikipedia.org/wiki/BBC_Domesday_Project>
- Domesday Reloaded, a web republication of about 25,000 images, went online in May 2011 and was offline by June 2018. Its archived form is hosted at The National Archives. [fetched, secondary] <https://en.wikipedia.org/wiki/BBC_Domesday_Project>
- Cause: a proprietary medium, a specific machine and a specific player. Each recovery was a separate engineering project. [inference from the sources above]
- Lesson: canonical content must be plain, documented and independent of any machine. Recovery was possible only because the source masters existed. Keep the source material of each edition, not just the rendered output. [inference]
- Lesson: web relaunches are not preservation copies; this one lasted about seven years. [inference]

### 3.4 MySpace uploads lost in a server migration (2019)

- What happened: in March 2019 MySpace said that uploads from 2003 through 2015 might no longer be available. [fetched] <https://www.theregister.com/2019/03/18/myspace_server_migration_data_loss/>
- The company message, as The Register reported it, said: "Due to a server migration, files were corrupted and unable to be transferred over to our updated site." It added: "There is no way to recover the lost data." [fetched] <https://www.theregister.com/2019/03/18/myspace_server_migration_data_loss/>
- Scale reported as more than 50 million songs from 14 million artists, with videos and photos possibly also gone. [fetched] <https://www.theregister.com/2019/03/18/myspace_server_migration_data_loss/>
- Andy Baio said he was "deeply skeptical this was an accident", and Laurie Voss said it was "unbelievable that they didn't have more than one copy of this data". [fetched] <https://www.theregister.com/2019/03/18/myspace_server_migration_data_loss/>
- The Internet Archive's Jason Scott publicly questioned the account. [search] <https://globalnews.ca/news/5068062/myspace-music-controversy-2019/>
- Cause: the reported cause is a migration of a single copy. The company's account is not independently verified. [inference from the sources above]
- Lesson: a migration is the highest-risk operation. Verify copies before and after it with fixity manifests, and keep the old copy until the new one is verified. [inference]

### 3.5 GeoCities closure (2009)

- What happened: GeoCities closed in reality at about 12:30 pm Pacific time on 27 October 2009. [fetched] <https://wiki.archiveteam.org/index.php/GeoCities>
- The Archive Team harvest ran from April to October 2009 and "involved several dozen people and hundreds of machine instances". Yahoo published no list of hosted sites, so the crawl was seeded from lists. [fetched] <https://wiki.archiveteam.org/index.php/GeoCities>
- The original torrent had about 0.1 percent corruption, and a patched version is the recommended copy. [fetched] <https://wiki.archiveteam.org/index.php/GeoCities>
- Mirrors died: geocitiesarchive.org was dead by August 2022 and geociti.es by March 2013. [fetched] <https://wiki.archiveteam.org/index.php/GeoCities>
- Cause: a platform closure with no export and a short timeline. Coverage gaps were filled by parallel efforts. [fetched] <https://wiki.archiveteam.org/index.php/GeoCities>
- Lesson: a distributed copy can be corrupted, so each distributed copy must be checked against a manifest published separately from it. [inference from the 0.1 percent figure]
- Lesson: mirrors are not permanent. The archival model's position that mirrors are welcome but not controllable is right, and the project should not count mirrors as copies it holds. [inference, archival model property 6]

### 3.6 Yahoo Groups shutdown (2019 to 2020)

- What happened: a November 2019 post quoted the deletion notice: "On December 14, everything ever posted to Yahoo! Groups in its 20-year history will be permanently deleted from the web." Groups remained as email-only lists. [fetched] <https://waxy.org/2019/11/the-deletion-of-yahoo-groups-and-archive-teams-rescue-effort/>
- Archive Team's initial crawl found nearly 1.5 million groups with public message archives, with an estimated 2.1 billion messages. It had archived 1.8 billion public messages by 28 October. [fetched] <https://waxy.org/2019/11/the-deletion-of-yahoo-groups-and-archive-teams-rescue-effort/>
- Files, photos and attachments were harder to save because members had to sign in, which "requires answering a reCaptcha". Private groups "may very well be lost for good". [fetched] <https://waxy.org/2019/11/the-deletion-of-yahoo-groups-and-archive-teams-rescue-effort/>
- The web interface and mailing lists closed in December 2020. Yahoo also banned the email addresses volunteers used to join groups. [search] <https://wiki.archiveteam.org/index.php/Yahoo!_Groups>
- Lesson: content behind login or CAPTCHA is hard to save, so the edition must be downloadable in bulk without login (requirement 4.4.4). [inference]
- Lesson: state the coverage of each edition, including what is not in it. A group that was not part of the save was missing from the collection. [fetched] <https://waxy.org/2019/11/the-deletion-of-yahoo-groups-and-archive-teams-rescue-effort/>

### 3.7 Google+ consumer shutdown (2019)

- What happened: consumer Google+ shut down in April 2019, after Google brought the date forward. [search] <https://www.androidpolice.com/2019/01/30/google-reveals-shutdown-timeline-for-consumers-and-its-coming-fast/>
- Before the rescue, the Internet Archive and Archive.today held "less than 1%" of Google+ pages, by one author's estimate. Archive Team's tracker showed 20,004,087 items archived by 27 March 2019. [fetched] <https://ws-dl.blogspot.com/2019/02/2019-02-08-google-is-being-shuttered.html>
- Crawlers miss content that needs scrolling and private posts that need login. A March 2019 update suggested the 2 April date was "likely a hard shutdown", so exports in progress may not finish. [fetched] <https://ws-dl.blogspot.com/2019/02/2019-02-08-google-is-being-shuttered.html>
- Only up to 500 comments per post could be archived. [fetched] <https://ws-dl.blogspot.com/2019/02/2019-02-08-google-is-being-shuttered.html>
- Lesson: an edition must be generated from the canonical data, never from crawled pages. Scroll-dependent or login-dependent rendering loses content. [inference, supports ADR 0006 static rendering]

### 3.8 Vine (announced 2016)

- What happened: Twitter announced the closure of Vine in 2016, and Archive Team backed up its videos. [fetched] <https://techcrunch.com/2025/11/12/jack-dorsey-funds-divine-a-vine-reboot-that-includes-vines-video-archive/>
- Archive Team kept the content as "40-50 GB binary files", which were not practical for people who only wanted to watch the videos. A developer spent a couple of months writing scripts to work out the file structure, then rebuilt videos, profiles, view counts and a subset of comments. [fetched] <https://techcrunch.com/2025/11/12/jack-dorsey-funds-divine-a-vine-reboot-that-includes-vines-video-archive/>
- The rebuilt app reports more than 100,000 videos. The developer later said about 150,000 to 200,000 videos from about 60,000 creators, and "I wasn't able to get all of them out". [fetched] <https://techcrunch.com/2025/11/12/jack-dorsey-funds-divine-a-vine-reboot-that-includes-vines-video-archive/>
- Lesson: a package must be decodable without a special decoder. Metadata, content and relations belong in plain, schema-documented files, not in an opaque container. [inference]
- Lesson: the popular items survived and the long tail did not. The coverage statement in each edition must say so. [fetched] <https://techcrunch.com/2025/11/12/jack-dorsey-funds-divine-a-vine-reboot-that-includes-vines-video-archive/>

### 3.9 Flickr free-account limit (2018 to 2019)

- What happened: Flickr announced that from 8 January 2019 free accounts would be limited to 1,000 photos and videos. The post does not say what happens to photos above the limit. [fetched] <https://blog.flickr.net/en/2018/11/01/changing-flickr-free-accounts-1000-photos/>
- A Flickr staff reply says the limit was not being enforced on accounts already over it, but "that doesn't mean we will not in the future". Over-limit accounts cannot upload new photos. [fetched] <https://www.flickr.com/help/forum/en-us/72157720512449119/>
- Press reports gave conflicting deletion dates. [search] <https://alternativeto.net/news/2018/11/flickr-is-limiting-its-free-service-to-1-000-total-photos-and-videos-per-account>
- Lesson: a host's terms can change after content is deposited. The archive's copies must be under the custodian's control, and no public host may be the only copy. [inference, ADR 0006]

### 3.10 Silent corruption, fixity and LOCKSS

- What happened: Bairavasundaram and colleagues analysed production storage systems with 1.53 million disk drives over 41 months. They found more than 400,000 checksum mismatches. Nearline disks produced them an order of magnitude more often than enterprise drives, and mismatches clustered in space and time. [fetched] <https://www.usenix.org/conference/fast-08/analysis-data-corruption-storage-stack>
- The LOCKSS principle, "Lots of Copies Keep Stuff Safe", says that more copies tend to make data safer. LOCKSS compares copies with each other rather than trusting a central fixity store. With two copies a disagreement cannot show which one is corrupted, so three is the practical minimum, and four is recommended for LOCKSS networks. [fetched] <https://www.lockss.org/about/frequently-asked-questions>
- The NDSA Levels of Digital Preservation require fixity checks on all ingests at Level 2, checks "at fixed intervals" with logs at Level 3, and "ability to replace/repair corrupted data" plus no single person with write access to all copies at Level 4. [fetched] <https://www.digitalpreservation.gov/documents/NDSA_Levels_Archiving_2013.pdf>
- What fixity catches: any byte change after the manifest was written. What it does not catch: wrong content exported before the manifest was written, a file missing from the manifest, or a manifest regenerated together with altered content. A bag is valid only if every payload file is listed in every payload manifest and every checksum verifies. [inference from the RFC 8493 text in case 3.18]
- Lesson: fixity needs a second copy to repair from. Store manifest digests outside the package, and set a check interval. [inference]

### 3.11 Link rot and identifiers

- Zittrain, Albert and Lessig (2014) found that more than 70 percent of URLs in the journals they studied, and 50 percent of URLs in United States Supreme Court opinions, do not produce the information originally cited. [fetched] <https://harvardlawreview.org/wp-content/uploads/2014/03/forvol127_zittrain.pdf>
- Klein and colleagues (2014) found that one in five STM articles suffers from reference rot, and that among articles with web references the fraction rises to seven in ten. [fetched] <https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0115253>
- Klein and Balakireva (2020) tested DOI resolution under different request methods and networks. They found that scholarly content providers "respond differently" and concluded that persistence "is not warranted". [fetched] <https://arxiv.org/abs/2004.03011>
- Lesson: a DOI or domain name is a pointer, not a guarantee. Each package must carry its own identity: public ID, edition ID and the record's path, so that a citation resolves from the package alone. This matches identifiers section 6. [inference]
- Lesson: do not treat a DOI as the permanent identifier of an edition until its resolution has been tested for the chosen registrar. [inference from the Klein and Balakireva result]

### 3.12 British Library cyberattack (2023)

- What happened: the Library confirmed on 31 October 2023 that an outage was caused by a cyberattack. The Rhysida group claimed it on 20 November 2023 and had copied about 600 GB, including personal details of users and staff. [fetched, secondary] <https://en.wikipedia.org/wiki/British_Library_cyberattack>
- The main online catalogue returned in read-only form on 15 January 2024. Some digital services were still being restored well after that, according to the same summary. [fetched, secondary] <https://en.wikipedia.org/wiki/British_Library_cyberattack>
- Lesson: an operational store that holds personal data is a target. Keep archival packages out of the operational network, keep at least one copy offline or read-only, and keep personal data out of packages. [inference]
- Lesson: recovery of digital access took well over a year. The restore drill (requirement 4.5.1) must measure time as well as success. [inference]

### 3.13 Internet Archive: 2024 breach and lost litigation

- What happened: a breach dated September 2024 exposed email addresses, screen names and bcrypt password hashes for about 31.1 million accounts. It was added to Have I Been Pwned on 9 October 2024. [fetched] <https://haveibeenpwned.com/Breach/InternetArchive>
- In Hachette v. Internet Archive, the Second Circuit affirmed in September 2024 that the Archive's controlled digital lending was not fair use, and the Archive did not seek Supreme Court review. [search] <https://communia-association.org/2024/09/25/internet-archive-loses-appeal-what-does-it-mean/>
- Lesson: keep user accounts and credentials away from the archive. The guestbook's account store is the riskiest data it holds, so it should hold as little as possible. [inference]
- Lesson: redistributing third-party material carries legal risk even for a well-known archive. Each reference item and each embedded artefact needs a recorded right. [inference, ADR 0009]

### 3.14 September 11 Digital Archive (2002 to 2021)

- What happened: the archive was organised by the American Social History Project and the Roy Rosenzweig Center for History and New Media, and initially funded by the Alfred P. Sloan Foundation. [fetched] <https://911digitalarchive.org/about>
- The Library of Congress accepted a copy into its permanent collections in September 2003, which the archive calls the Library's first major digital acquisition. [fetched] <https://911digitalarchive.org/about>
- The project closed to new contributions in 2021. [fetched] <https://911digitalarchive.org/about>
- Migrations: a 2011 grant moved it to Omeka, a 2014 move to a new underlying system changed many item links, and it was relaunched as a static site generated by Hugo, described as "as of 2026", for sustainability. [fetched] <https://911digitalarchive.org/about>
- Contributors keep copyright: "original contributors maintain copyright over all objects". The page says nothing about file formats, metadata standards, or consent and privacy for submitters. [fetched] <https://911digitalarchive.org/about>
- The archive reports more than 150,000 items and over 40,000 first-hand stories. [search] <https://en.wikipedia.org/wiki/September_11_Digital_Archive>
- Lesson: an independent deposit early, a defined end to collection, and a planned migration path. The static-site move matches ADR 0006. [inference]
- Lesson: publish the consent and privacy handling. The 9/11 archive's public page does not, so this is a gap the guestbook should not repeat. [inference]

### 3.15 Mass Observation (1937 onward)

- What happened: Mass Observation was founded in 1937 to create an "anthropology of ourselves". Its Mass Observation Project, launched in 1981, is a national writing panel. Almost 4,500 people have volunteered since it began, and over 500 write actively. [fetched] <https://massobs.org.uk/about-mass-observation/>
- The archive is in the care of the University of Sussex Special Collections at The Keep. [fetched] <https://massobs.org.uk/about-mass-observation/>
- Lesson: continuity came from institutional custody and a stable, pseudonymous numbering of contributors, held apart from names. The research at docs/research/domain-and-persistence.md section 4 reports the referencing guidance as secondary material. [inference]
- Lesson: custody by an institution is the strongest answer to the question of who holds the archive after the founder. [inference, docs/operations succession]

### 3.16 COVID-19 testimony collections

- Mass Observation's COVID-19 collection documents everyday life "from March 2020 to Autumn 2021", with a database of "nearly 10,000 documents". Its page does not describe consent, anonymity or pseudonym handling. The Paper Trails article it links gives the period as "between March 2020 and early 2022". [fetched] <https://massobs.org.uk/research/covid19/>
- The Library of Congress COVID-19 American History Project was created in early 2023 and collected from 2023 to 2024. Congress tasked the Library to "record, collect, and keep the stories of Americans impacted by the pandemic". [fetched] <https://guides.loc.gov/covid-19-folklife/library-collections>
- The Library's Coronavirus Web Archive was made public in early 2022 after two years of collection, with new content held back for a year before release. [search] <https://www.infodocket.com/2022/02/02/library-of-congress-coronavirus-web-archive-collection-now-available-online/>
- Lesson: time-boxed calls with stated dates and a stated cut-off are how these projects stayed coherent. Each edition should state its call period and cut-off in its README. [inference]
- Lesson: state the consent and anonymity practice publicly, as a method note, not only in internal documents. [inference]

### 3.17 Software Heritage (2016 onward)

- What happened: Software Heritage was unveiled in 2016 by Inria as an open, non-profit infrastructure, in collaboration with UNESCO. It states that it does "not inspect or filter the source code, and archive anything that we can get hold of". [fetched] <https://www.softwareheritage.org/software-heritage-faq/>
- It says "all software source code artifacts are preserved for the long-term", including from deleted repositories. [fetched] <https://www.softwareheritage.org/software-heritage-faq/>
- Its identifiers are intrinsic: SWHIDs "pinpoint the exact version" of an artefact "without relying on any central registry or naming authority". The specification says it does not require the use of Software Heritage. [fetched] <https://www.swhid.org/specification/v1.2/0.Introduction/>
- Lesson: a content-derived digest lets anyone check a copy without the archive. The guestbook can keep its random public ID and add a digest of each record's canonical content. [inference]
- Lesson: an archive that keeps everything, including deleted items, is the opposite of the guestbook's withdrawal right. The guestbook should not copy that policy, and its deletion philosophy stands. [inference, deletion philosophy]

### 3.18 Standards in practice: OAIS, PREMIS, BagIt and OCFL

- OAIS: ISO 14721:2025, the third edition of the reference model, was published in March 2025 and replaces the 2012 edition. [search] <https://www.iso.org/standard/87471.html>
- OAIS critique: Lavoie's 2014 guide ties the model's limitations to its abstract design. [search] <https://www.dpconline.org/docs/technology-watch-reports/1359-dpctw14-02/file> Lavoie's 2004 report notes that "OAIS-compliant" can mean either an explicit application of the model or concepts merely recoverable from an implementation. [search] <https://www.dpconline.org/docs/dpc-technology-watch-publications/technology-watch-reports-1/2859-lavoie-oais-twr0401/file>
- PREMIS 3.0 was released in June 2015 and is maintained by the Library of Congress PREMIS Maintenance Activity. [search] <https://www.loc.gov/standards/premis/v3/premis-3-0-final.pdf>
- BagIt (RFC 8493) is Informational and was published in October 2018. Tools "MUST support the SHA-256 and SHA-512 algorithms" and "SHOULD enable SHA-512 by default". The bagit.txt file "MUST consist of exactly two lines", encoded in UTF-8 without a byte order mark. A fetch file "allows a bag to be transmitted with holes", and the RFC "does not mandate any particular action" for errors. [fetched] <https://www.rfc-editor.org/rfc/rfc8493>
- BagIt practice: Franklin Furnace wrote its own Python wrapper to bag and validate collections of 42 TB and 1.8 TB in batches, and notes that adding files requires regenerating the checksums of every file in the folder. [fetched] <https://franklinfurnace.org/refining-franklin-furnaces-digital-preservation-practices-with-bagit/>
- BagIt practice: a 2021 DPC post reports that profile setup "requires a bit of skill editing JSON files", that a tag manifest went stale after an edit, and that tools "generally create and verify their own checksum files but do not check existing ones", with different filenames. [fetched] <https://www.dpconline.org/blog/putting-archives-into-bags>
- BagIt tooling: bagit-python shows active development, with open issues from March 2026 on Python 3.14 deprecation warnings. No deprecation notice was found. [search] <https://github.com/LibraryOfCongress/bagit-python/issues>
- OCFL 1.1: "Once created, the contents of a version directory are expected to be immutable" (section 3.3). Checksums use sha512 by preference, with sha256 allowed (section 3.4). The specification contains no mechanism for deleting or purging content from earlier versions. [fetched] <https://ocfl.io/1.1/spec/>
- OCFL practice: a 2019 University of Technology Sydney write-up names concurrent update software as the main implementation hurdle. [search] <https://ptsefton.com/2019/07/01/OCLF/index.html>
- OCFL practice: an empty directory holds only filesystem metadata and cannot be preserved in an OCFL object. [search] <https://www.mdpi.com/2304-6775/7/2/39>
- Lesson: BagIt is the simplest transfer container with the most tooling. OCFL's immutability means a privacy purge is a designed procedure the spec does not provide. The layout in domain-and-persistence.md section 4, an OCFL object whose versions are BagIt bags, therefore needs revisiting. [inference]

### 3.19 Recommended formats, and where Markdown stands

- The Library of Congress Recommended Formats Statement 2025-2026 rates formats on seven sustainability factors: disclosure, adoption, transparency, self-documentation (including accessibility support), external dependencies, impact of patents, and technical protection mechanisms. [fetched] <https://www.loc.gov/preservation/resources/rfs/RFS%202025-2026.pdf>
- For digital textual works, the statement lists character encodings in order UTF-8, UTF-16 (with BOM), US-ASCII. XML-based markup with an included schema, EPUB3, PDF/UA and PDF/A (ISO 19005) are preferred. Plain text appears among the "other formats" in the acceptable column, after RTF. This reading comes from the layout of the extracted PDF text. [fetched] <https://www.loc.gov/preservation/resources/rfs/RFS%202025-2026.pdf>
- For datasets, the statement ranks "platform-independent, character-based formats" above native or binary formats, and lists line-oriented formats such as TSV and CSV among them. [fetched] <https://www.loc.gov/preservation/resources/rfs/RFS%202025-2026.pdf>
- The 2025-2026 statement does not mention Markdown. This was checked in the extracted text of the PDF. [fetched] <https://www.loc.gov/preservation/resources/rfs/RFS%202025-2026.pdf>
- text/markdown was registered by RFC 7763 (Informational, March 2016). The RFC describes Markdown as "a family of related plain-text formatting syntaxes and implementations". The charset parameter is "REQUIRED" with "no default value", and the variant parameter is only "a hint". [fetched] <https://www.rfc-editor.org/rfc/rfc7763>
- The current CommonMark specification is version 0.31.2, dated 2024-01-28. [fetched] <https://spec.commonmark.org/>
- JSON (RFC 8259, an Internet Standard, STD 90) requires UTF-8 for text exchanged outside a closed ecosystem, and says that when names within an object are not unique "the behavior of software that receives such an object is unpredictable". [fetched] <https://www.rfc-editor.org/rfc/rfc8259>
- CSV (RFC 4180, Informational, October 2005) notes that no single master specification existed. It registers text/csv, uses CRLF line breaks, and allows an optional header line signalled by a parameter. [fetched] <https://www.rfc-editor.org/rfc/rfc4180>
- Lesson: canonical testimony text as UTF-8 plain text, metadata as JSON, indexes as CSV or TSV, and any Markdown as a derived rendering with a declared variant. This is defensible but sits in the Library's acceptable tier for text, so a PDF/A or XML-based rendition is worth considering for the preferred tier (open question 4). [inference]

## 4. Requirements for the archive format and editions

These requirements are proposals for issue #13 and are not binding until the owner accepts them and the specification is written. Each cites the cases that motivate it.

### 4.1 Format and content

1. Each edition is a BagIt 1.0 bag (RFC 8493), with payload manifests in both SHA-512 and SHA-256 so that either common validator can check it. Basis: 3.18, 3.10.
2. An edition contains no fetch.txt and is complete: every payload file appears in every payload manifest. An edition with missing files is not published. Basis: 3.18, 3.10.
3. Testimony bodies are plain text, encoded in UTF-8 and stored without a byte order mark. Basis: 3.19, 3.18.
4. Each testimony's metadata is one JSON document in UTF-8 that validates against the schema shipped with the edition, with no duplicate member names. Basis: 3.19.
5. Indexes (edition contents, identifier-to-path table, withdrawal log) are CSV with a header row, following RFC 4180 line rules, or TSV. Basis: 3.19.
6. Markdown is never the canonical form. Any Markdown copy is a derived file with its variant declared. Basis: 3.19.
7. Each edition includes static HTML renderings of the published testimonies and of the reference shelf, which the Library of Congress lists as an acceptable structured format. Basis: 3.19, ADR 0006.
8. Binary artefacts (images, audio, video) use formats the Recommended Formats Statement lists as preferred or acceptable for their type. Each has its own description record and fixity entry. Basis: 3.3, 3.8, 3.19.
9. No database dump, application-specific serialisation or opaque container is part of the canonical content. A database dump may ship as a convenience copy only. Basis: 3.3, 3.8.
10. Each edition has its own schema documentation in plain text: every field, its type, its allowed values, its schema version, and how absent values are represented. The edition can be read without the application. Basis: 3.3, 3.18.
11. Each edition has a plain-text README in English and French that states what the edition contains and excludes, its licence, how to verify it, how to cite it, its relation to earlier revisions, and the call period and cut-off that define it. Basis: 3.6, 3.7, 3.16.
12. Each record carries its own identifiers: the public ID, the edition ID and the record's path within the bag. A citation resolves from the package alone. Basis: 3.11, identifiers section 6.
13. The edition ships an identifier-to-path table covering every public ID, including withdrawn IDs as tombstones with no personal data. Basis: 3.11, deletion philosophy 4.

### 4.2 Fixity and integrity

1. The edition's tag manifest lists every payload manifest. A SHA-256 digest of each manifest is published outside the bag, on the website and in the deposit record, because a manifest inside the bag can be regenerated together with altered content. Basis: 3.5, 3.10, 3.18.
2. The project publishes each edition's full file list with sizes and SHA-256 digests (archival model property 5). Basis: 3.5, 3.6.
3. Every copy of every edition is checked against the published digests at a fixed interval set by the custodian, with a log kept. Basis: 3.10 (NDSA Level 3), 3.4.
4. Repair is only from a copy that matches the published digests. Manifests are never regenerated to match a changed file. Basis: 3.10, 3.4.
5. Before publication, each edition is read by an independent reader, a script written from the schema documentation alone, in a different language from the export code. The reader must pass. Basis: ADR 0006 (round trip), 3.8.

### 4.3 Revision and withdrawal

1. Editions are never edited in place. A privacy revision is a new, complete bag with its own identifier under identifiers section 4, plus a plain-text revision note giving the general reason. Basis: archival model property 4, deletion philosophy 5, 3.18.
2. The withdrawal log is a CSV file listing withdrawn public IDs, the revision in which each was removed, and the date. It holds no content and no personal data. Basis: archival model property 6, deletion philosophy 4 and 7.
3. OCFL version directories are not used for editions unless a purge procedure is designed and tested. The OCFL 1.1 specification defines none. Basis: 3.18. This conflicts with the layout in domain-and-persistence.md section 4 and must be resolved there.
4. Every hosted edition states the withdrawal policy and says that copies distributed before a revision cannot be recalled. Basis: deletion philosophy 6, 3.5, 3.6.

### 4.4 Access, consent and contributor promises

1. The contributor-facing text, shown before submission, states the legal limits of confidentiality, for example "to the extent French and EU law allows", and says that lawful requests may reach what the archive holds. Basis: 3.2.
2. Archival packages hold no names, contact details, account identifiers or the mapping from a public ID to a person. Any such mapping, needed for withdrawal, stays in the operational store with a retention limit. Basis: 3.2, 3.12, 3.13, identifiers section 1.
3. Each testimony record has a machine-readable access field (public, public after a dated embargo, or closed), set at submission and shown in the edition, so that closure is recorded rather than implicit. Basis: 3.2.
4. Editions are downloadable in bulk without login, CAPTCHA or per-item requests. Basis: 3.6, 3.7.
5. Each testimony and each reference item records its licence and the basis for redistribution. Editions include third-party material only with a recorded right. Basis: 3.13, ADR 0009.

### 4.5 Operations

1. Once a year, one edition is restored from one copy into an empty directory and read by the independent reader. The drill records elapsed time as well as success. Basis: deletion philosophy 9, ADR 0006, 3.12.
2. The operational store and the archival copies are separated. The operational store's backups are encrypted, and no credentials are placed in any package. Basis: 3.12, 3.13.
3. Each edition is deposited with at least one independent institution at release, and the deposit identifier is fixed when the deposit is first made (identifiers section 4). Basis: 3.14, 3.15.
4. At each release the custodian records the formats and schema versions in use and checks them against the Recommended Formats Statement categories. Basis: 3.3, 3.19.

## 5. Open questions for the owner

1. Which confidentiality promise can the project make? Which French and EU bodies should be consulted on whether any contributor-facing promise can be stronger than "to the extent the law allows"? The research document already flags the status of article 85 of the Loi Informatique et Libertes as disputed. Basis: 3.2, including the GDPR article 89 bullet.
2. Which independent institution receives each edition deposit, and what does a deposit agreement require? The research document raises the BnF legal-deposit question and marks it as needing legal review. Basis: 3.14, 3.15.
3. How many copies, in which places, and at what fixity interval? Requirement 4.2.3 proposes a check interval but leaves the number to the owner. Basis: 3.10, 3.12.
4. Are the canonical testimony bodies plain UTF-8 only, or also published as PDF/A or XML-based renditions, which the Library of Congress lists as preferred? Basis: 3.19.
5. Does Markdown ever appear in the contributor interface? If yes, is it converted to plain text on ingest, so that the canonical body never depends on a variant? Basis: 3.19.
6. Is an embargo or closure option offered at submission? If yes, what is the maximum length, and what is said about subpoenas and other legal demands? Basis: 3.2, OHA (search).
7. Does the project drop OCFL from the layout in domain-and-persistence.md section 4, or design and test a purge procedure? Basis: 3.18.
8. Should editions receive a DOI, for example through Zenodo, given the DOI resolution findings and the open GDPR erasure question in the research document? Basis: 3.11.
9. Who is the named successor custodian if the owner cannot continue? Basis: 3.3, 3.14, 3.15.

## 6. Sources

Each source is listed once with the URL used. Tags in section 1 indicate how each was used.

- Library of Congress, update on the Twitter archive (2017): <https://blogs.loc.gov/loc/2017/12/update-on-the-twitter-archive-at-the-library-of-congress/>
- Academic paper on the Library of Congress Twitter archive (search snippet): <https://www.academia.edu/38380877/_Archiving_and_Preserving_Social_Media_at_the_Library_of_Congress_Institutional_and_Cultural_Challenges_to_Build_a_Twitter_Archive_>
- Belfast Project, Wikipedia (secondary): <https://en.wikipedia.org/wiki/Belfast_Project>
- WBUR, Boston College must release IRA tapes (2013): <https://www.wbur.org/news/2013/06/02/bc-release-ira-tapes>
- WBUR, court rejects appeal over IRA tapes (2013, search snippet): <https://www.wbur.org/news/2013/04/15/ira-tapes-boston-college>
- Oral History Association, Principles and Best Practices (2018, search snippet): <https://www.oralhistory.org/wp-content/uploads/2019/03/OHA-Principles-and-Best-Practices-Adopted-2018.pdf>
- BBC Domesday Project, Wikipedia (secondary): <https://en.wikipedia.org/wiki/BBC_Domesday_Project>
- The Register, MySpace server migration (2019): <https://www.theregister.com/2019/03/18/myspace_server_migration_data_loss/>
- Global News, MySpace (2019, search snippet): <https://globalnews.ca/news/5068062/myspace-music-controversy-2019/>
- Archive Team, GeoCities wiki: <https://wiki.archiveteam.org/index.php/GeoCities>
- Waxy, the deletion of Yahoo Groups (2019): <https://waxy.org/2019/11/the-deletion-of-yahoo-groups-and-archive-teams-rescue-effort/>
- Archive Team, Yahoo Groups wiki (search snippet): <https://wiki.archiveteam.org/index.php/Yahoo!_Groups>
- Android Police, Google+ shutdown timeline (2019, search snippet): <https://www.androidpolice.com/2019/01/30/google-reveals-shutdown-timeline-for-consumers-and-its-coming-fast/>
- Web Science and Digital Libraries blog, Google+ is being shuttered (2019): <https://ws-dl.blogspot.com/2019/02/2019-02-08-google-is-being-shuttered.html>
- TechCrunch, Vine archive and diVine (2025): <https://techcrunch.com/2025/11/12/jack-dorsey-funds-divine-a-vine-reboot-that-includes-vines-video-archive/>
- Flickr blog, changing free accounts (2018): <https://blog.flickr.net/en/2018/11/01/changing-flickr-free-accounts-1000-photos/>
- Flickr help forum, 1,000 photo limit: <https://www.flickr.com/help/forum/en-us/72157720512449119/>
- AlternativeTo, Flickr limit (2018, search snippet): <https://alternativeto.net/news/2018/11/flickr-is-limiting-its-free-service-to-1-000-total-photos-and-videos-per-account>
- USENIX FAST 2008, An analysis of data corruption in the storage stack: <https://www.usenix.org/conference/fast-08/analysis-data-corruption-storage-stack>
- LOCKSS, frequently asked questions: <https://www.lockss.org/about/frequently-asked-questions>
- NDSA, The NDSA Levels of Digital Preservation (2013): <https://www.digitalpreservation.gov/documents/NDSA_Levels_Archiving_2013.pdf>
- Zittrain, Albert and Lessig, Perma (Harvard Law Review, 2014): <https://harvardlawreview.org/wp-content/uploads/2014/03/forvol127_zittrain.pdf>
- Klein et al., Scholarly context not found (PLOS ONE, 2014): <https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0115253>
- Klein and Balakireva, On the persistence of persistent identifiers of the scholarly web (arXiv, 2020): <https://arxiv.org/abs/2004.03011>
- British Library cyberattack, Wikipedia (secondary): <https://en.wikipedia.org/wiki/British_Library_cyberattack>
- Have I Been Pwned, Internet Archive breach: <https://haveibeenpwned.com/Breach/InternetArchive>
- Communia, Internet Archive loses appeal (2024, search snippet): <https://communia-association.org/2024/09/25/internet-archive-loses-appeal-what-does-it-mean/>
- September 11 Digital Archive, About: <https://911digitalarchive.org/about>
- September 11 Digital Archive, Wikipedia (search snippet): <https://en.wikipedia.org/wiki/September_11_Digital_Archive>
- Mass Observation, About: <https://massobs.org.uk/about-mass-observation/>
- Mass Observation, COVID-19 collection: <https://massobs.org.uk/research/covid19/>
- Library of Congress, COVID-19 guide (folklife and collections): <https://guides.loc.gov/covid-19-folklife/library-collections>
- Infodocket, Library of Congress Coronavirus Web Archive (2022, search snippet): <https://www.infodocket.com/2022/02/02/library-of-congress-coronavirus-web-archive-collection-now-available-online/>
- Software Heritage, FAQ: <https://www.softwareheritage.org/software-heritage-faq/>
- SWHID specification, version 1.2, introduction: <https://www.swhid.org/specification/v1.2/0.Introduction/>
- ISO 14721:2025 (search snippet; the page returned 403): <https://www.iso.org/standard/87471.html>
- Lavoie, OAIS introductory guide, DPC Technology Watch 14-02 (search snippet): <https://www.dpconline.org/docs/technology-watch-reports/1359-dpctw14-02/file>
- Lavoie, The OAIS reference model, DPC Technology Watch 04-01 (search snippet): <https://www.dpconline.org/docs/dpc-technology-watch-publications/technology-watch-reports-1/2859-lavoie-oais-twr0401/file>
- PREMIS Data Dictionary 3.0 (search snippet): <https://www.loc.gov/standards/premis/v3/premis-3-0-final.pdf>
- Franklin Furnace, refining digital preservation practices with BagIt: <https://franklinfurnace.org/refining-franklin-furnaces-digital-preservation-practices-with-bagit/>
- DPC, Putting archives into bags (Harwood, 2021): <https://www.dpconline.org/blog/putting-archives-into-bags>
- bagit-python issues (search snippet): <https://github.com/LibraryOfCongress/bagit-python/issues>
- RFC 8493, The BagIt File Packaging Format (v1.0): <https://www.rfc-editor.org/rfc/rfc8493>
- OCFL 1.1 specification: <https://ocfl.io/1.1/spec/>
- University of Technology Sydney, OCFL repository write-up (2019, search snippet): <https://ptsefton.com/2019/07/01/OCLF/index.html>
- MDPI, The Oxford Common File Layout (search snippet): <https://www.mdpi.com/2304-6775/7/2/39>
- Library of Congress, Recommended Formats Statement 2025-2026 (PDF, extracted with pdftotext): <https://www.loc.gov/preservation/resources/rfs/RFS%202025-2026.pdf>
- RFC 7763, The text/markdown media type: <https://www.rfc-editor.org/rfc/rfc7763>
- CommonMark specification: <https://spec.commonmark.org/>
- RFC 8259, The JavaScript Object Notation (JSON) data interchange format: <https://www.rfc-editor.org/rfc/rfc8259>
- RFC 4180, Common format and MIME type for CSV files: <https://www.rfc-editor.org/rfc/rfc4180>
- GDPR article 89, gdpr-info.eu: <https://gdpr-info.eu/art-89-gdpr/>
- British Library, legal deposit and web archiving (search snippet): <https://www.bl.uk/services/legal-deposit/web-archiving>
