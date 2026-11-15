# Custodial independent projects: research notes for The Artificial Intelligence Guestbook

## 1. Title, date, scope and method

Date of research: 2026-11-15.

Scope: independent projects run by one private person or a tiny volunteer team that take on an ongoing custodial obligation (hosting other people's content, archives, testimony or oral-history collections, community services, long-lived free web services), plus the institutional and legal context that shapes them. France and the EU are weighted, with strong non-EU cases included where the lesson transfers. Successes and failures are both covered.

Method: WebSearch and WebFetch, run on 2026-11-15. Each factual claim is tagged. [fetched] means the page was opened and the cited statement was read there. [search] means the claim appears only in a search-result snippet or summary, which was not opened; treat it as lower confidence. [inference] means my reasoning from the sources. Where sources conflict, the conflict is stated. Legal points come from primary texts only where marked [fetched]; the French lawyer article and the CNIL guidance PDF are flagged because they could not be verified against primary texts. Nothing here is legal advice; the plan's own requirement for legal validation still applies.

## 2. Summary of transferable lessons

Ranked by importance to this project. Case numbers refer to section 3.

1. The legal basis for testimony must be decided per data category before launch, and consent is the weakest basis for an archive. The UK Oral History Society guidance says consent is only one legal basis, recommends public-interest archiving where legally available, says special-category data needs an additional basis, and says that once consent is withdrawn another basis cannot be substituted for the same data [fetched] (case 3.14). The GDPR text allows special-category processing of data "manifestly made public by the data subject" (Art. 9(2)(e)) and for "archiving purposes in the public interest" (Art. 9(2)(j)) [fetched] (case 3.14). The plan's withdrawal promise (section 22) and the archive-release language (section 20) therefore cannot be unconditional; the erasure exemption for archiving (Art. 17(3)(d)) exists but is conditional [fetched] (case 3.14, section 4).
2. Moderation and abuse handling, not storage, is what usually wears down a small custodial service. The ZeroBin author says he no longer has time to maintain it and the repository is now marked unmaintained [fetched] (case 3.1). Mataroa closed free sign-ups in 2022 to remove spam blogs [fetched] (case 3.5). Refern shut down in September 2025 citing reports of CSAM, project size and running costs, as recorded in the IndieWeb site-deaths list [fetched] (case 3.8). Framasoft's 2019 decision to close 30 of 38 services cited maintenance load beyond team capacity [fetched] (case 3.2).
3. Bus factor is the most common structural risk for solo projects, and the operators say so publicly. Mataroa's homepage states the team is one person, that "this sets the bus factor to 1", and that a successor plan targets 2030 [fetched] (case 3.5). The Pinboard founder's "bus" remark is quoted in discussion threads, and users reported unresponsiveness in 2024 (case 3.4, unverified in detail). Plan section 29 should be treated as a release deliverable, not a later task.
4. Notice and a working export are the norm for credible closures, and export quality decides whether the archive survives. Framasoft gave 9 to 18 months' notice per closing service [fetched] (case 3.2). The Mastodon Covenant commits operators to at least three months' warning so users can export data and move [fetched] (case 3.3). Cohost's shutdown was staged: announcement in September 2024, data exports in October 2024, archiving by the Archive Team, completion on 12 January 2025 [fetched via the IndieWeb list] (case 3.9). Mozilla Solo (shutdown on 30 November 2026) offers an HTML-only export with images downloaded separately, and The Register describes this as leaving users to "go it alone" [fetched] (case 3.10). Plan sections 20 and 23 should require a complete, documented export that someone other than the founder has restored.
5. A custodian must be arranged before closure, because a rescue after closure is done by volunteers and is partial. The GeoCities rescue ran from April to October 2009 with "several dozen people and hundreds of machine instances", and the size of what was saved is reported inconsistently [fetched] (case 3.11). Cohost's shutdown date was extended so the Archive Team could finish archiving [fetched via the IndieWeb list] (case 3.9). In France, departmental archives and the BnF have already taken on web-based testimony collection [fetched] (case 3.16). Plan section 29 should name a candidate institutional custodian for the annual editions.
6. Withdrawal and deletion do not reach copies outside the project's control. The plan already says this (section 20); the evidence is consistent. The Internet Archive's exclusion route is discretionary and does not touch screenshots or other archives [search] (case 3.12). Zenodo's takedown procedure restricts access during review, informs the uploader, and does not share personal information between requester and uploader [fetched] (case 3.19). Build a takedown procedure that copies the Zenodo model: restrict first, verify, notify, decide, and record.
7. Link rot is fast, so references and contextual material should be captured when published. Pew (May 2024) found a quarter of webpages that existed between 2013 and 2023 were no longer accessible in October 2023, with 38 percent of 2013 pages gone against 8 percent of 2023 pages [fetched] (case 3.13). Plan sections 16 and 18 should store a snapshot of each reference at publication, not rely on a live link.
8. Minors: the French CNIL guidance sets 15 as the age below which online-service consent needs one holder of parental authority alongside the child, and the other holder's consent is presumed [fetched] (section 4 and case 3.23). Whether a testimony archive is an information-society service "directly offered" to children is an open legal question [inference].
9. Keep personal data minimal and have a breach runbook. The Internet Archive's October 2024 breach exposed a user database of about 31 million records, according to third-party coverage [search] (case 3.12). GDPR Art. 33 requires notification to the supervisory authority "without undue delay and, where feasible, not later than 72 hours" [fetched] (case 3.12). The magic-link design avoids password storage, but email addresses and IP logs remain personal data (plan section 21).
10. Gate publication before it becomes public. Bear Blog keeps unreviewed blogs out of search and discovery until reviewed, and its creator reports spam fell from about 30 percent of new blogs to under 5 percent (self-reported) [search] (case 3.6). Neocities removes content only for legal or Terms-of-Service violations and relies on user reports rather than monitoring [search] (case 3.7). This supports the plan's pre-publication moderation (section 9).
11. When an original project is abandoned, a maintained fork can carry the users forward. ZeroBin's README tells users to switch to PrivateBin [fetched] (case 3.1), and a Mastodon instance announced for closure in 2023 was kept running after a caretaker was appointed [search] (case 3.3). Plan section 29 should keep the code open and the data formats documented, so a fork is possible.

Reviewer's note on lesson 1 (2026-11-15): read it together with [the legal research](legal-landscape.md), sections 2 and 3. Art. 9(2)(j), art. 89 and the art. 17(3)(d) exemption need a basis in Union or Member State law (art. 6(3)), which a private individual operating without a legal mandate does not have. For this project, consent and explicit consent remain the workable bases. Withdrawal is therefore unconditional for copies under the project's control, as the [deletion philosophy](../constitution/deletion-philosophy.md) already states. What cannot be unconditional, and must be explained honestly, is the reach of withdrawal over copies held by others. The lesson stands as a reason to reconsider the bases if an institutional partner with a public-interest archiving mandate takes custody of the editions later.

The lead on "sebsauvage.net services closed because of abuse or legal burden" is only partly substantiated (case 3.1). The lead on "Pinboard essay: we're not going anywhere" was not found and should not be quoted.

## 3. Case studies

### 3.1 sebsauvage.net and ZeroBin

What it is. sebsauvage.net is the personal site of the French developer Sébastien Sauvage. ZeroBin is a client-side-encrypted pastebin he wrote, which was offered as a test service on his site [fetched].

Who runs it. Sebastien Sauvage, individually.

What happened. The ZeroBin wiki page says the test paste service may be deleted or shut down at any time, and asks users not to abuse it [fetched]. The same page says administrators can remove a document on court order or infringement notice, but cannot tell whether identical content has been reposted [fetched]. The page says the author no longer has time to maintain ZeroBin and recommends PrivateBin [fetched]. The ZeroBin GitHub README now reads "This repo is unmaintained and outdated! Do not use this code anymore!" and points to PrivateBin [fetched]. One search summary dates the end of active maintenance to 2014 and says PrivateBin can read ZeroBin 0.19 data [search, unverified].

What worked. The fork PrivateBin kept the users' path open and the code was carried forward by others [search, plus README link fetched].

What failed. No announcement was found that sebsauvage.net closed services because of abuse or legal pressure. The lead as stated in the brief is therefore not substantiated. The substantiated part is maintenance burden and removal-on-notice.

Lesson for the Guestbook. Documenting how legal removals work, and how copies are handled, is cheap and was done here. Plan a successor fork path for the code (plan section 29).

Sources: sebsauvage wiki (<https://sebsauvage.net/wiki/doku.php?id=php%3Azerobin>), GitHub README (<https://github.com/sebsauvage/ZeroBin>), PrivateBin project (<https://github.com/PrivateBin/PrivateBin>).

### 3.2 Framasoft (Déframasoftisons Internet)

What it is. Framasoft is a French non-profit association that offers free-software online services. In 2019 it announced a plan to close most of its services because maintenance load had outgrown the team [fetched via Next.ink].

Who runs it. An association; the technical team was described as "un administrateur système et deux ou trois développeurs selon les périodes" [fetched].

What happened. The association had 38 services and announced it would close 30 of them and keep 8. Its own words: "nous avons atteint notre capacité maximale" [fetched]. Each closing service got between 9 and 18 months' notice, and most closures were planned between mid-2020 and 2021 [fetched]. Framadrive kept existing accounts but stopped accepting new sign-ups [fetched]. The announcement date is 24 September 2019 [fetched].

What worked. The staged notice, the explicit capacity argument, and the pointers to other providers in the CHATONS network [fetched]. The Framasoft documentation pages for closed services point to export tools and alternatives [search].

What failed or remains unclear. Closures of Framasite and Framaslides in 2021 and 2022 were reported in search summaries [search, unverified]. A 2025 "in numbers" article exists [search, not opened]. I did not confirm the final state of each service.

Lesson for the Guestbook. Give a published capacity argument early. Keep a list of what the project can actually run; the plan's MVP exclusions (section 34, and "no comments, no messaging" in section 28) already follow this logic. Give long notice in the published closure policy.

Sources: Next.ink article (<https://next.ink/6608/108225-deframatisons-internet-framasoft-fermera-progressivement-30-services/>), Framablog 2019 post (<https://framablog.org/2019/09/24/deframasoftisons-internet/>, not opened because fetches timed out), Framablog 2025 numbers (<https://framablog.org/2025/12/23/framasoft-in-numbers-2025-edition/>, search only).

### 3.3 Mastodon and fediverse closures

What it is. Mastodon is a free software social network; anyone can run a server ("instance"). Many instances are run by volunteers.

Who runs it. Varies: volunteers, companies, governments [inference from the examples below].

What happened. The Mastodon Covenant commits operators to "at least 3 months of advance warning in case of shutting down", framed as time "to export their data and find another server" [fetched]. Mozilla announced in September 2024 that mozilla.social would close on 17 December 2024, with 270 active users at the time, and users could export data or migrate [search]. In February 2023 the administrator of mastodon.au announced closure on 16 May 2023, citing lack of help from the Mastodon founder; the decision was reversed when a caretaker took over [search]. A French lawyer's article dated 25 October 2026 says an instance operator is "in principle" the GDPR controller, that closure should be announced, the server kept running through the notice period for exports, and then data deleted; it also discusses hosting-liability rules [fetched, but a secondary legal commentary, not verified against the statutes].

What worked. The covenant gives a concrete notice period. The caretaker handover in the mastodon.au case kept the instance alive [search].

What failed. Abrupt closures prevent followers from being redirected [fetched via the lawyer article, secondary]. Data deletion for mastodon.au was not found [search].

Lesson for the Guestbook. Adopt a written closure rule with a minimum notice period. Treat "no notice" as a failure mode. The French article's claim that the DSA may apply to small non-commercial hosts is unresolved and should go to the legal review (section 4).

Sources: Mastodon Covenant (<https://joinmastodon.org/covenant>), Mozilla notice (<https://wedistribute.org/2024/09/mozilla-social-shutting-down/> and <https://techcrunch.com/2024/09/17/mozilla-exits-the-fediverse-and-will-shutter-its-mastodon-server-in-december>, search only), mastodon.au (<https://news.ycombinator.com/item?id=34817612>, search only), French lawyer article (<https://kohenavocats.com/mastodon-france-instance-moderation-compte-suspendu-serveur-ferme-donnees-obligations-administrateurs-2026/>, fetched via www).

### 3.4 Pinboard

What it is. Pinboard is a paid social bookmarking service created by Maciej Cegłowski, with a paid full-text archive option [search].

Who runs it. One person, according to the public record [search].

What happened. Cegłowski wrote in a blog post, quoted in a Hacker News thread, "What does the future hold for Pinboard? Death! The bus that one day comes for us all!" [search]. The date is uncertain: one summary says 31 October 2016, another HN thread links the passage with 2019 [search, conflicting]. Michael Tsai's 2024 post "The End of Pinboard?" reports a user who saw more outages with less communication, and could download only a fraction of their bookmarks through the API [search, not opened].

What worked. The service has run for many years and the founder is open about the risk [search].

What failed or is unclear. No formal succession plan or export-on-death arrangement was found [search]. The "we're not going anywhere" essay in the brief could not be found and should not be quoted.

Lesson for the Guestbook. A joke about the bus is not a succession plan. The plan's section 29 requirement that important knowledge not exist solely in the founder's memory is the right control.

Sources: Hacker News thread quoting the post (<https://news.ycombinator.com/item?id=20397745>, search only), Michael Tsai on Pinboard (<https://mjtsai.com/blog/2024/09/20/the-end-of-pinboard/>, search only), Pinboard blog (<https://blog.pinboard.in/>, not opened).

### 3.5 Mataroa

What it is. Mataroa is a minimalist blogging platform, open-source, with a small paid operation.

Who runs it. Its homepage says the team is currently one person [fetched].

What happened. In September 2022 the operator closed registrations to purge spam blogs. Registrations stay closed until the operator builds "moderation functionality that emails these blog 'authors' an export of their words", which would also delete those blogs [fetched]. The homepage says the single-person team "sets the bus factor to 1, which is not good", that a succession plan aims to find people to continue by Mataroa's tenth anniversary in 2030, and that the service keeps running "maybe indefinitely, as long as monthly payments continue" [fetched].

What worked. The operator stated the risk plainly and set a dated succession goal. Closing registrations removed a spam problem quickly [fetched].

What failed. Spam forced the closure of a public sign-up path. The export tool needed to reopen was still a precondition at the time of the fetch [fetched].

Lesson for the Guestbook. Export tooling is a precondition for opening or reopening a public submission path; the plan's section 20 export must exist before public launch. State the bus-factor risk on the public site, as Mataroa does.

Sources: <https://mataroa.blog/> (fetched), <https://hey.mataroa.blog/p/closing-registrations/> (fetched).

### 3.6 Bear Blog

What it is. Bear is a minimal blogging service by Herman Martinus.

Who runs it. Its creator, with help recruited as signups grew [search].

What happened. Bear's "Frustration Loop" hides spam from spammers, and the creator says spam dropped from about 30 percent of new blogs to under 5 percent (self-reported) [search]. New blogs are kept out of search indexes and the discovery feed until reviewed, and owners can request review [search]. The creator reports a sharp rise in signups, including spam, and co-opted help to clear the review queue [search].

What worked. Keeping unreviewed content out of discovery limited exposure. Manual review was kept for each publication, with appeals by email [search].

What failed or is unknown. The sources are 2022 to 2024; current figures are not known [search].

Lesson for the Guestbook. The default-hidden model of Bear is the same principle as the plan's pre-publication queue (section 9). The review workload scales with signups, which is why the plan's magic-link login, which limits automated signup, matters. Watch the queue backlog metric (section 31).

Sources: <https://herman.bearblog.dev/the-frustration-loop/> (search), <https://docs.bearblog.dev/code-of-conduct/> (search).

### 3.7 Neocities

What it is. Neocities is a free static-website host.

Who runs it. Not confirmed in this research; the searches did not return current operator information.

What happened. The Neocities legal guide says a site may be removed if it violates US law or the terms of service, and that offensiveness alone is not grounds for removal [search]. Enforcement is based on user reports, because the terms say Neocities does not monitor communications unless notified [search]. A confirmed violation leads to removal, a ban, and a block on new sites [search]. Neocities retains the IP address used to create a site for abuse handling [search].

What worked. A clear, narrow removal standard and reliance on reports, which keeps the operator's monitoring burden small [inference from search].

What failed or is unknown. No recent controversy was found [search].

Lesson for the Guestbook. Publish the removal standard in plain terms. The plan's "narrow publishing rules" (section 9) should be written in the same form.

Sources: <https://neocities.org/legal> (search), <https://neocities.org/terms> (search).

### 3.8 Refern and the IndieWeb site-deaths list

What it is. Refern was a small community site. The IndieWeb wiki maintains a "site deaths" list of closed independent sites with dates, stated reasons and export status [fetched].

Who runs it. Its operators; the closure notice is quoted on the IndieWeb page.

What happened. The IndieWeb page records Refern's shutdown on 2025-09-13, with all content deleted, and gives the reason quoted as "This was for several reasons: increased reports of CSAM, project size, and expenses of running it." [fetched]. No export is recorded [fetched]. The same page lists other closures with mixed export practice, including Read.cv (export as JSON, Markdown or Next.js formats, per the list) and Typepad (exports end on the shutdown date) [fetched].

What worked. The IndieWeb list is a useful tracker of export practices across closures [fetched].

What failed. Refern's closure deleted content without a recorded export [fetched].

Lesson for the Guestbook. Illegal-content reporting is a real operating cost for a small public site, and it can be the reason a site closes. The plan's section 9 lists "illegal material" but does not yet say how reports are handled, or where mandatory reports go. This needs a written protocol and a legal check (section 4).

Sources: <https://indieweb.org/site_deaths> (fetched).

### 3.9 Cohost

What it is. Cohost was a small social network.

Who runs it. A small team whose principal funder controlled the code, according to press reports [search].

What happened. Cohost's staff post, as quoted by Michael Tsai, cites "lack of funding and burnout" and says "cohost will become read-only on Tuesday, October 1st" [fetched via a quote]. The IndieWeb list records the announcement on 2024-09-09, data exports sent on 2024-10-14, a shutdown date extended so the Internet Archive Team could finish archiving, and "archival complete" on 2025-01-12 [fetched]. Press coverage gives the read-only date as 2 October 2024 [search], which conflicts with the staff post. Control of the code went to the principal funder [search].

What worked. Staged notice, a data export, and a deliberate archiving handover with the Archive Team; the shutdown date was moved to allow the archiving [fetched].

What failed. Funding and burnout forced the closure, and the source code was controlled by the funder [search].

Lesson for the Guestbook. Plan the closure for funding and burnout, not only for abuse. The sequence announcement, read-only, export, archiving partner, shutdown is a template. Decide in advance who would hold the code and the data if the founder cannot continue.

Sources: <https://mjtsai.com/blog/2024/09/23/cohost-to-shut-down> (fetched), <https://indieweb.org/site_deaths> (fetched), Yahoo Finance report (<https://finance.yahoo.com/news/cohost-x-rival-founded-anti-200951160.html>, search only).

### 3.10 Mozilla.social and Mozilla Solo

What it is. Mozilla.social was a Mastodon instance run by Mozilla. Mozilla Solo was a site builder run by Mozilla. Both are corporate, not indie. They are included as export examples.

What happened. Mozilla.social was announced for closure in September 2024 for 17 December 2024, with export or migration available [search]. The IndieWeb list records no export for it, which conflicts with the search reports [fetched and search]. Mozilla Solo: Mozilla says it first notified users on 1 October 2026 and gave 60 days; the site and data are deleted on 30 November 2026 [fetched]. The export is a ZIP with an HTML version of the site, a CSV of form submissions, and images that must be downloaded separately; domains must be moved to Name.com [fetched]. The article says the FAQ does not explain how to get a complete working site running elsewhere [fetched].

What worked. A notice window and a partial export [fetched].

What failed. The export left users to rebuild the parts it omitted, which is the central risk for a testimony archive.

Lesson for the Guestbook. An export of "HTML plus separate media" is not a complete archive. The plan's section 20 and 23 export should carry testimony IDs, metadata, withdrawal tombstones, and media in one package, and a stranger should be able to restore it from the documentation.

Sources: <https://www.theregister.com/software/2026/11/13/mozilla-leaves-solo-website-owners-to-go-it-alone-as-hosting-shuts-down/5309632> (fetched), <https://wedistribute.org/2024/09/mozilla-social-shutting-down/> (search).

### 3.11 GeoCities and Archive Team

What it is. GeoCities was Yahoo's free web-hosting service for personal pages, closed in 2009. Archive Team is a volunteer group that rescues web content.

Who runs it. Archive Team, led by Jason Scott, with dozens of volunteers [search], and Yahoo as the closing operator [fetched].

What happened. Yahoo announced the closure in April 2009 and fixed 26 October 2009 in July 2009 [fetched]. The shutdown happened around 12:30 pm Pacific time on 27 October 2009, and some pages lingered for days [fetched]. Archive Team's harvesting ran from April to October 2009 with "several dozen people and hundreds of machine instances" [fetched]. The size of the rescue is reported inconsistently: a "900GB Torrent" headline and "One Terabyte" in a research project [fetched]. Some collections are in the Internet Archive, and a torrent with about 0.1 percent corrupted data needed a patched version [fetched]. The Archive Team page does not discuss privacy or personal data, and marks the main collection as restricted download with no reason given [fetched].

What worked. A volunteer team harvested a large public archive in months, and the copies were distributed to several institutions [fetched].

What failed. The rescue happened after the operator had decided, and it was partial. Personal data in the rescued pages was not addressed [fetched].

Lesson for the Guestbook. A closure rescue is possible but depends on volunteers, so the Guestbook should not rely on it. The annual editions with a prearranged custodian (case 3.16) are the better plan. The restricted-download flag shows the privacy question has to be decided separately.

Sources: <https://wiki.archiveteam.org/index.php/GeoCities> (fetched), <https://www.computerworld.com/article/1333713/yahoo-geocities-closes-on-oct-26.html> (search).

### 3.12 Internet Archive: Hachette litigation, 2024 breach, removal requests

What it is. The Internet Archive is a US non-profit digital library and the operator of the Wayback Machine.

Who runs it. The Internet Archive, a non-profit with large staff and infrastructure, not a tiny team.

What happened. In Hachette Book Group v. Internet Archive, the district court granted summary judgment to the publishers in March 2023, and the Second Circuit affirmed on 4 September 2024 [search]. The Internet Archive decided in December 2024 not to seek Supreme Court review [search]. In October 2024 a breach of a user authentication database was reported, with about 31 million records including emails, screen names and bcrypt-hashed passwords, while the site was under DDoS attack [search]. The breach was disclosed about a week after the discoverer alerted the organization, and critics said the disclosure was slow [search]. The Internet Archive's removal process is discretionary: exclusion requests are reviewed case by case, and copies held elsewhere are not affected [search, several vendor guides, weak].

What worked. The Wayback Machine has kept a large archive available despite these events, and the 2026 Internet Archive post reports rescue figures (case 3.13) [fetched].

What failed. A large user database was exposed and disclosure was slow [search]. Litigation over lending imposed a legal cost on a non-profit archive [search].

Lesson for the Guestbook. A breach of account data is the most likely high-impact personal-data incident for a login-based site. Keep the stored personal data minimal, prepare a 72-hour notification path (Art. 33, [fetched]), and do not promise removal from third-party archives (section 20 of the plan already says this).

Sources: Infodocket on the Second Circuit ruling (<https://www.infodocket.com/2024/09/04/appellate-court-affirms-district-court-ruling-in-hachette-v-internet-archive/>, search), BleepingComputer on the breach (<https://www.bleepingcomputer.com/news/security/internet-archive-hacked-data-breach-impacts-31-million-users/>, search), Internet Archive blog (<https://blog.archive.org/2026/04/23/gone-but-not-forgotten-recovering-the-dead-web/>, fetched).

### 3.13 Link rot evidence

What it is. Empirical studies of how fast web references disappear. This is evidence about the environment, not a project.

Who. Pew Research Center (2024); Klein and colleagues (PLOS ONE, 2014 and 2016); the Internet Archive's 2026 post.

What happened. Pew reports that "a quarter of all webpages that existed at one point between 2013 and 2023 are no longer accessible" as of October 2023, with 38 percent of 2013 pages gone and 8 percent of 2023 pages gone; 23 percent of news pages and 21 percent of government pages had at least one broken link [fetched]. Klein and colleagues' 2014 paper is titled "Scholarly Context Not Found: One in Five Articles Suffers from Reference Rot" [search]; a 2016 follow-up reports a much larger share of URI references changed or rotten [search]. The Internet Archive's April 2026 post argues that archived copies recover a large share of the Pew losses, reducing the 2013 figure to about 15 percent of pages [fetched; this is the Archive's own analysis].

What worked. Archiving tools such as Save Page Now recover a large share [fetched].

What failed. Most links are not archived at the time of use [fetched in Pew context and IA post].

Lesson for the Guestbook. For the reference shelf and contextual material (plan sections 16 and 18), store a copy at publication, with a record of the snapshot and date. The review in plan section 28 should check these.

Sources: <https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/> (fetched), <https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0115253> (search), <https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0167475> (search), <https://blog.archive.org/2026/04/23/gone-but-not-forgotten-recovering-the-dead-web/> (fetched).

### 3.14 UK Oral History Society guidance on GDPR

What it is. Guidance for oral-history projects, the closest published body of practice for testimony archives.

Who runs it. The Oral History Society, a UK learned society.

What happened. The guidance (version 5.0, August 2019, no publication date shown) says consent is only one legal basis; that archival processing should normally rely on "the performance of a task carried out in the public interest" where legally able, otherwise legitimate interests; that special-category processing "requires an additional legal basis"; that deceased interviewees raise the question of third-party sensitive data and copyright; that consent "can be withdrawn at any time"; and that "If consent is withdrawn then you cannot substitute another legal basis to continue processing that data" [fetched]. It recommends two documents: a participation agreement before the interview and a recording agreement after [fetched]. The UK rule for archiving special-category data cites the Data Protection Act 2018 Schedule 1, which does not apply in France [fetched].

What worked. Separating participation from copyright and access, and treating consent as one basis among several [fetched].

What failed or is unclear. The guidance is UK-specific and dated. I did not find a French equivalent from the AFAS (section 4).

Lesson for the Guestbook. Choose the legal basis per data category, and write the withdrawal promise to match. If consent is the basis for a testimony, withdrawal must work; if public-interest archiving is the basis, the controller must qualify under French law, which is the central open question (section 4). The GDPR text supports special-category processing for data "manifestly made public by the data subject" (Art. 9(2)(e), [fetched]) and for archiving in the public interest (Art. 9(2)(j), [fetched]). Art. 89 requires safeguards such as data minimisation and allows Union or Member State law to derogate from certain rights where the purposes would be impossible or seriously harder to achieve [fetched, paraphrased]. Art. 17(3)(d) exempts archiving from erasure only within that same test [fetched in part; the full "render impossible" condition was not fetched].

Sources: <https://ohs.org.uk/gdpr-2/> (fetched), <https://gdpr-info.eu/art-9-gdpr/> (fetched), <https://gdpr-info.eu/art-89-gdpr/> (fetched), <https://gdpr-info.eu/art-17-gdpr/> (fetched).

### 3.15 Archivio Diaristico Nazionale (Pieve Santo Stefano, Italy)

What it is. A national archive of autobiographical writing (diaries, letters, memoirs), founded in 1984 by the journalist Saverio Tutino at the wish of the local council, and run as a foundation since 1991 [search, Atlas Obscura and other summaries].

Who runs it. A foundation (onlus) formed on the initiative of the council. The Il Post article names only its organisational director, Natalia Cangi, and gives no staff numbers [fetched].

What happened. Il Post (December 2023) reports about 10,000 items in the collection, of which just over 2,600 are true diaries, with about 350 new items a year. The collection is kept in two apartments and a storage room; the plan to move to a former kindergarten was approved by the Ministry of Culture in 2021, with a tender and about two years of works still to come, and a hoped-for 2026 move [fetched]. Copyright for most texts remains with the authors, so the archive asks permission for each excerpt it publishes [fetched].

What worked. A durable public-institution link (council, ministry, national recognition) and a prize that brings in new material [search].

What failed or is strained. Space and physical custody, and slow public works [fetched].

Lesson for the Guestbook. A long-lived testimony archive needs a place and a custodian beyond the founder. Permission for each excerpt is the copyright lesson for the plan's section 14 (quoting and sharing). Text-only testimonies are small, but media will not be.

Sources: <https://www.ilpost.it/2023/12/27/archivio-diari-pieve-santo-stefano/> (fetched), <https://www.atlasobscura.com/articles/italy-tuscany-city-diaries-memories-history> (search).

### 3.16 French COVID-19 testimony collection and the BnF web deposit

What it is. In 2020 French archives and the national library collected pandemic testimony and web content.

Who runs it. The BnF (digital legal deposit team), and the departmental and municipal archives.

What happened. The BnF's digital legal deposit team began archiving COVID-related web content on 17 March 2020, including websites, blogs, lockdown diaries, social-media posts and YouTube videos; by mid-April it covered nearly 2,000 sources, with an expected 8 to 10 terabytes [fetched]. The Archives départementales des Vosges launched #memoiredeconfinement on 18 March 2020, promising to keep testimonies "pour l'éternité", and the Archives municipales de Beaune launched a call the same day; about twenty other services joined [fetched]. One search summary says the Loiret archives gathered fewer than fifty testimonies [search, unverified].

What worked. Institutions with an existing mandate took on the work quickly [fetched]. The BnF's legal deposit covers French web sites including personal sites; the only site-owner obligation described is not blocking the crawler [search, BnF help page, not opened].

What failed or is unclear. Some calls gathered little material [search]. I did not find the current BnF opt-out policy: a 2011 IFLA paper describes an opt-out, but current pages were not confirmed [search].

Lesson for the Guestbook. In France, a public archive is a realistic custodian for the annual editions and may already run a call. The plan's section 29 should list the departmental archives and the BnF as candidates, with a written deposit agreement that settles withdrawal rules before anything is deposited.

Sources: <https://labo.societenumerique.gouv.fr/fr/articles/comment-les-mus%C3%A9es-services-des-archives-et-la-bnf-archivent-et-documentent-la-crise-sanitaire/> (fetched), <https://www.bnf.fr/en/help-center/web-legal-deposit-instructions> (search), <https://www.archimag.com/archives-patrimoine/2020/03/23/memoires-confinement-projets-archivent-quotidien-coronavirus-covid-19> (search).

### 3.17 Mass Observation Archive (COVID-19 collection)

What it is. The Mass Observation Archive, a long-running UK panel and archive of everyday life, now at the University of Sussex [search].

Who runs it. The Mass Observation Archive, based at the University of Sussex, with an annual report [search].

What happened. The archive's COVID-19 collection includes directive responses and personal diaries, with a searchable database funded by a Wellcome Trust grant [search]. A peer-reviewed article on archiving the pandemic reports about 5,000 day diaries from 12 May 2020, about 3,000 in 2021 and about 300 in 2022 [search]. In 2025 the archive asked its panel to reflect on the pandemic five years later [search].

What worked. A standing panel and a repeat-collection format produced a longitudinal set, and an institutional host carries the custody [search].

What failed or is unknown. The end date of the contribution window is reported differently across sources [search].

Lesson for the Guestbook. A standing annual call (the plan's annual editions) can build a longitudinal series, and an institutional host is what keeps the custody going. The plan's 12 May style one-day call is also a method to consider.

Sources: <https://massobs.org.uk/research/covid19/> (search), <https://journals.sagepub.com/doi/10.1177/09526951231152139> (search).

### 3.18 A Journal of the Plague Year (Arizona State University)

What it is. An archive of Covid-19 testimony and material, hosted at covid-19archive.org, named after Defoe's novel [fetched].

Who runs it. Founded by Catherine O'Donnell, Richard Amesbury and Mark Tebeau at Arizona State University; now a curatorial consortium of faculty and graduate students [fetched]. Seeded by a public history endowment at ASU [fetched].

What happened. It accepts text, images, audio, video, links and files through a "Share Your Story" form [fetched]. The homepage does not state consent, minors, personal-information, or removal rules; its terms page was not read [fetched].

What worked. Institutional seeding and a student-facing submission route [fetched].

What is unknown. Its consent and removal policy, which is the item most relevant to the Guestbook; I did not read the terms page.

Lesson for the Guestbook. A closely comparable project, and a useful comparison for the consent wording. The terms page should be read before the plan's consent language (section 10) is finalised.

Sources: <https://covid-19archive.org/> (fetched).

### 3.19 Zenodo takedown procedure

What it is. Zenodo is a CERN-operated open repository for research outputs with DOIs. It is not indie, but its procedure is a clear public model.

Who runs it. CERN.

What happened. Zenodo's take-down FAQ says it first checks the validity of a request, "usually restrict[s] access to the files and/or full record while we investigate", informs the uploader and asks for comments, then decides [fetched]. It says it does not share personal information of the requester or uploader with each other without consent, though non-personal case details are shared [fetched]. Its privacy policy refers to CERN's operational circular on data protection, described as comparable to the GDPR [search].

What worked. A clear order of steps: restrict, verify, inform, decide, and keep the requester and uploader apart [fetched].

Lesson for the Guestbook. Copy this order for withdrawal and removal requests (plan section 22), and record each step in the internal moderation log.

Sources: <https://support.zenodo.org/help/en-gb/13-policies/140-what-is-your-take-down-procedure> (fetched), <https://about.zenodo.org/privacy-policy/> (search).

### 3.20 Right to Be (formerly Hollaback!)

What it is. Right To Be is a non-profit that began as Hollaback!, a crowdsourced map and storytelling project about street harassment.

Who runs it. A non-profit organisation.

What happened. Its current site describes itself as "Right To Be (formerly Hollaback!)", describes a storytelling platform, and cites "32,000+ stories" received [fetched]. The site does not say when the rename happened and does not mention the original map [fetched]. A Wikipedia summary says the name changed but does not give a date [search].

What worked. The project kept its storytelling platform running under a new name for years [fetched].

What is unknown. Whether older Hollaback-era stories and the map are still online and at the same URLs [not verified].

Lesson for the Guestbook. A rename or rebrand can break the stable URLs that the plan requires (section 12). Decide the naming and redirect policy before launch, and avoid any product name that might later change.

Sources: <https://righttobe.org/> (fetched), <https://en.wikipedia.org/wiki/Right_to_Be> (search).

### 3.21 Everyday Sexism Project (unresolved lead)

What it is. A crowdsourced collection of reports of everyday sexism, started by Laura Bates in the UK in 2012 [search].

Who runs it. Founded by Laura Bates; current operators not confirmed [search].

What happened. Search summaries report tens of thousands of entries, including a Globe and Mail piece about "20,000 submissions" and a figure above 80,000 testimonies in a later lecture listing [search]. An academic study used the entries as research data [search]. I found no source on moderation, takedown, closure, or current hosting [search].

Lesson for the Guestbook. This is a close analogue for a testimony collection, but its custodial history is not documented in what I found. Treat it as an open question, not a case study.

Sources: <https://www.theglobeandmail.com/life/the-hot-button/20000-submissions-have-you-heard-of-the-everyday-sexism-project/article8483409/> (search), <https://time.com/2882850/everyday-sexism/> (search).

### 3.22 September 11 Digital Archive

What it is. A digital collection of personal September 11 materials, begun in 2002 at George Mason University's Center for History and New Media with the American Social History Project, funded by the Alfred P. Sloan Foundation [search].

Who runs it. The Center for History and New Media (George Mason University) and partners [search].

What happened. The project deliberately collected material that was not already on the public web, such as personal narratives, emails and photos, directly from their owners [search]. Early submissions skewed white and middle-class, which prompted a Spanish-language site and community interviews [search]. The Library of Congress acquired a copy in September 2003 [search].

What worked. Direct collection and deliberate outreach to underrepresented groups [search].

Lesson for the Guestbook. Representation is a custodial concern as well as an editorial one. The plan's section 8 (languages) and the outreach element of the MVP should plan for this from the start.

Sources: <https://www.historians.org/perspectives-article/digital-archive-collects-and-preserves-memories-of-9-11-april-2002/> (search), <https://en.wikipedia.org/wiki/September_11_Digital_Archive> (search).

### 3.23 French regulatory references used in this report

What it is. Not a project case, but two regulatory facts that bear on the plan.

Minors: CNIL Recommendation 4 says that for a child under 15, online-service consent requires that the child and a holder of parental authority consent together; one holder is enough and the other is presumed to agree, but must be able to object [fetched]. Other CNIL material leaves unresolved which services fall under the 15-year rule [search]. I did not verify the current text of the statute itself.

Enforcement: a 2025 search summary says the CNIL received 6,167 breach notifications and imposed 83 sanctions totalling about 486.8 million euros, mostly against large firms [search, unverified]. An anecdotal case of a small association fined for an unsecured member database was not verifiable [search]. Sanctions reviewed by one analysis were mostly about passwords and unauthenticated data [search].

Lesson for the Guestbook. Age handling (plan section 11) can be specified at 15 for France as a starting point, with a legal check on scope. Security failures, not content, are where small operators are most often sanctioned, which supports the plan's security section.

Sources: <https://www.cnil.fr/fr/recommandation-4-rechercher-le-consentement-dun-parent-pour-les-mineurs-de-moins-de-15-ans> (fetched), <https://www.weka.fr/actualite/administration/article/face-a-un-nombre-record-de-violations-de-donnees-en-2025-la-cnil-va-renforcer-ses-controles-214486/> (search), <https://own2pwn.fr/articles/appsec/fuite-de-donnees> (search).

## 4. Open questions and leads not pursued

1. CNIL guidance on definitive archiving (guide_durees_de_conservation.pdf) could not be read; the tool returned a binary PDF. A search summary says private organisations should agree arrangements for definitive archiving with the competent departmental archives service [search]. If true, this is a plan-changing point for sections 20 and 21, because it could give the archive a legal anchor. Priority: read the CNIL PDF or its HTML equivalent.
2. Which French legal basis applies to a private operator archiving testimony in the public interest under Art. 9(2)(j) and Art. 89, and whether a deposit agreement with a public archive would qualify. Not verified.
3. Whether a testimony archive falls within the French under-15 consent rule (Art. 45 of the French data-protection act, cited by secondary sources [search]).
4. Whether the DSA and the French LCEN hosting rules apply to a small non-commercial operator. The French lawyer article (<https://kohenavocats.com/mastodon-france-instance-moderation-compte-suspendu-serveur-ferme-donnees-obligations-administrateurs-2026/>) says it is unsettled and recommends treating it as if it applies; it also states reporting duties for certain offences. Not verified against Legifrance.
5. Mandatory reporting of illegal content, including child sexual abuse material, and the French reporting channel. Refern's case (case 3.8) makes this concrete. Not researched further.
6. The Everyday Sexism Project's current status and moderation practice (case 3.21).
7. The terms page of A Journal of the Plague Year (case 3.18).
8. Whether Right to Be's Hollaback-era stories and map remain online at stable URLs (case 3.20).
9. The Pinboard "bus" post date (2016 or 2019 are both quoted) and its exact wording (case 3.4). The "we're not going anywhere" essay was not found.
10. Current Internet Archive removal policy; the official page was not found, only vendor guides (case 3.12).
11. Current BnF opt-out policy for personal sites (case 3.16).
12. Write.as status; no announcement found (not a case).
13. AFAS (Association française des archives sonores, orales et audio): founded 1979 [search]; no GDPR guidance from it was found. Other French oral-history bodies were not searched in depth.
14. Digital-estate and domain-after-death practice: sources found were commercial blogs and estate-service firms, not authoritative. Not used as a case.
15. Mass Observation's 2024 annual report and the peer-reviewed article were not opened.
16. The Framasoft 2021 and 2022 closure dates (Framasite, Framaslides) and the 2025 state of its services are reported inconsistently [search]; not verified.
17. The September 11 Digital Archive and Mass Observation figures come from search summaries; primary pages were not opened.

## 5. Sources

Primary or fetched sources (opened and read):

- <https://next.ink/6608/108225-deframatisons-internet-framasoft-fermera-progressivement-30-services/> (Framasoft plan, 2019)
- <https://sebsauvage.net/wiki/doku.php?id=php%3Azerobin> (ZeroBin wiki)
- <https://github.com/sebsauvage/ZeroBin> (ZeroBin README)
- <https://joinmastodon.org/covenant> (Mastodon Covenant)
- <https://kohenavocats.com/mastodon-france-instance-moderation-compte-suspendu-serveur-ferme-donnees-obligations-administrateurs-2026/> (French lawyer article, 25 October 2026; secondary, unverified)
- <https://mataroa.blog/> (Mataroa homepage)
- <https://hey.mataroa.blog/p/closing-registrations/> (Mataroa, 30 September 2022)
- <https://indieweb.org/site_deaths> (IndieWeb site-deaths list; secondary compilation)
- <https://mjtsai.com/blog/2024/09/23/cohost-to-shut-down> (Cohost, quoting the staff post)
- <https://www.theregister.com/software/2026/11/13/mozilla-leaves-solo-website-owners-to-go-it-alone-as-hosting-shuts-down/5309632> (Mozilla Solo)
- <https://wiki.archiveteam.org/index.php/GeoCities> (Archive Team GeoCities page)
- <https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/> (Pew, 17 May 2024)
- <https://blog.archive.org/2026/04/23/gone-but-not-forgotten-recovering-the-dead-web/> (Internet Archive, 23 April 2026; self-reported analysis)
- <https://ohs.org.uk/gdpr-2/> (Oral History Society GDPR guidance, version 5.0 August 2019)
- <https://gdpr-info.eu/art-9-gdpr/> (GDPR Art. 9)
- <https://gdpr-info.eu/art-17-gdpr/> (GDPR Art. 17, partly read)
- <https://gdpr-info.eu/art-33-gdpr/> (GDPR Art. 33, partly read)
- <https://gdpr-info.eu/art-89-gdpr/> (GDPR Art. 89, paraphrased)
- <https://www.cnil.fr/fr/recommandation-4-rechercher-le-consentement-dun-parent-pour-les-mineurs-de-moins-de-15-ans> (CNIL Recommendation 4)
- <https://www.ilpost.it/2023/12/27/archivio-diari-pieve-santo-stefano/> (Il Post on the Archivio Diaristico Nazionale)
- <https://labo.societenumerique.gouv.fr/fr/articles/comment-les-mus%C3%A9es-services-des-archives-et-la-bnf-archivent-et-documentent-la-crise-sanitaire/> (French state digital lab article on COVID archiving)
- <https://covid-19archive.org/> (A Journal of the Plague Year)
- <https://support.zenodo.org/help/en-gb/13-policies/140-what-is-your-take-down-procedure> (Zenodo take-down procedure)
- <https://righttobe.org/> (Right To Be)

Search-result sources (not opened; lower confidence):

- <https://framablog.org/2019/09/24/deframasoftisons-internet/> (Framablog 2019; fetch timed out)
- <https://framablog.org/2025/12/23/framasoft-in-numbers-2025-edition/>
- <https://news.ycombinator.com/item?id=34817612> (mastodon.au)
- <https://wedistribute.org/2024/09/mozilla-social-shutting-down/>
- <https://techcrunch.com/2024/09/17/mozilla-exits-the-fediverse-and-will-shutter-its-mastodon-server-in-december>
- <https://news.ycombinator.com/item?id=20397745> (Pinboard quote)
- <https://mjtsai.com/blog/2024/09/20/the-end-of-pinboard/>
- <https://finance.yahoo.com/news/cohost-x-rival-founded-anti-200951160.html>
- <https://www.computerworld.com/article/1333713/yahoo-geocities-closes-on-oct-26.html>
- <https://www.infodocket.com/2024/09/04/appellate-court-affirms-district-court-ruling-in-hachette-v-internet-archive/>
- <https://www.bleepingcomputer.com/news/security/internet-archive-hacked-data-breach-impacts-31-million-users/>
- <https://news.ycombinator.com/item?id=16965575> (2018 comment on Wayback removal)
- <https://neocities.org/legal>
- <https://neocities.org/terms>
- <https://herman.bearblog.dev/the-frustration-loop/>
- <https://docs.bearblog.dev/code-of-conduct/>
- <https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0115253> (Klein et al. 2014)
- <https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0167475> (Klein et al. 2016)
- <https://www.bnf.fr/en/help-center/web-legal-deposit-instructions>
- <https://www.archimag.com/archives-patrimoine/2020/03/23/memoires-confinement-projets-archivent-quotidien-coronavirus-covid-19>
- <https://massobs.org.uk/research/covid19/>
- <https://journals.sagepub.com/doi/10.1177/09526951231152139> (Mass Observation COVID article)
- <https://www.atlasobscura.com/articles/italy-tuscany-city-diaries-memories-history>
- <https://www.historians.org/perspectives-article/digital-archive-collects-and-preserves-memories-of-9-11-april-2002/>
- <https://en.wikipedia.org/wiki/September_11_Digital_Archive>
- <https://en.wikipedia.org/wiki/Right_to_Be>
- <https://www.theglobeandmail.com/life/the-hot-button/20000-submissions-have-you-heard-of-the-everyday-sexism-project/article8483409/>
- <https://time.com/2882850/everyday-sexism/>
- <https://about.zenodo.org/privacy-policy/>
- <https://www.weka.fr/actualite/administration/article/face-a-un-nombre-record-de-violations-de-donnees-en-2025-la-cnil-va-renforcer-ses-controles-214486/>
- <https://own2pwn.fr/articles/appsec/fuite-de-donnees>
- <https://www.i6doc.com/fr/publisher/?publisher_id=413> (AFAS)

Local files:

- C:\Users\DJ6664\Repos\the-artificial-intelligence-guestbook\docs\plans\main.md (plan read; sections 9 to 11, 20 to 22, 28 to 31)
