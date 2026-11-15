# Reference shelf: format, selection and first records

Status: Proposal - awaiting owner review (2026-11-15)

Issue: #37

Research date: 2026-11-15. Source tags: [fetched] means the page was opened with WebFetch on 2026-11-15 and the cited statement was read there. [search] means only a search-result snippet or a secondary summary was available; treat it as lower confidence. [inference] means my reasoning from the cited sources. Repository documents are cited with relative links and tagged [fetched] because they were read directly. A record marked "partly read" was only partly readable. Pages that returned HTTP 403, a connection reset or an unreadable body are not used to support any record; they are listed in section 5.

## 1. Summary

1. The record format follows the constitution's list of required fields and data model section 2.14, with five additions: operator, category, last known status, licence source and snapshot eligibility (section 2).
2. Twenty-two records are proposed, each verified with WebFetch on 2026-11-15. Three are only partly read (Eurobarometer, Reuters Institute, Internet Archive).
3. Weak coverage: model databases (no verified record; Epoch AI could not be read), labour studies (one), education studies (one), generated-media and misinformation trackers (one), and oral-history projects about technology (one AI-specific, one general).
4. Only four records have a licence that clearly allows a local snapshot of their content: the State of AI Report (CC BY 4.0), the EU legal texts on EUR-Lex (reuse policy), the licensed collections of the AI Incident Database (CC BY-SA 4.0), and arXiv metadata (CC0). Most other resources are all rights reserved, or have terms that bar republication. For those, the shelf keeps metadata and dated capture links, not copies.
5. Decisions needed from the owner are listed in section 7.

## 2. Record format

The fields below are the ones proposed for each reference record. Core fields come from the [constitution](../constitution/external-archives.md) (principle 3) and [data model section 2.14](../specs/data-model.md). Field names follow the data model and [identifiers section 5](../specs/identifiers.md).

| Field | Meaning | Basis |
| --- | --- | --- |
| `slug` | Lowercase ASCII identifier, matching `[a-z0-9]+(-[a-z0-9]+)*`, permanent once published. | Identifiers section 5. Plan section 18 calls it `id`; see question 1. |
| `name` | The resource's name as it appears on its own pages. | Constitution principle 3. |
| `role` | What the resource is for, in one phrase. | Plan section 18. |
| `category` | One of the categories in section 4. Used to group the shelf and to show gaps. | Added. |
| `operator` | The organisation or person that runs the resource, with the page that says so. | Added, as the brief asks. Operators change, and a record needs to show who ran the resource when it was verified. |
| `homepage` | The landing page of the resource or its project. | Constitution principle 3. |
| `resource_url` | The URL of the specific resource described. | Constitution principle 3. |
| `description` | Two or three sentences on what the resource contains, with facts taken from the page. | Constitution principle 3. |
| `verified_on` | Date of the last successful read of `resource_url`. | Data model section 2.14 and constitution principle 3 ("date verified"). |
| `last_known_status` | `live`, `live, partly read` or `unverified`, plus any fact a later reader needs, such as a closing date. | Added, as the brief asks. |
| `licence` | The licence or terms that govern the content, quoted or closely paraphrased, or "not stated". | Data model section 2.14. |
| `licence_source` | The URL where the licence statement was read. | Added. A licence without its source cannot be checked again. |
| `snapshot_eligible` | `yes`, `no` or `unknown`: whether a local copy would be lawful under the stated licence. `unknown` means no licence was read. | Added, as the brief asks. |
| `local_snapshot` | Path and checksum in an edition, or `null`. | Data model section 2.14. This proposal makes no snapshots, so every record is `null`. |
| `notes` | Caveats, access limits, conflicts between sources and what was not read. | Constitution principle 3. |

## 3. Selection criteria

Numbered test, applied in this order:

1. Does a future reader need this to understand the testimonies and their world? Plan sections [16](../plans/main.md) and [17](../plans/main.md) set this test: the shelf points to specialist work and keeps the social record. Plan section 37 gives a higher bar to anything that would make the project a "comprehensive AI database" [fetched](../plans/main.md).
2. Is it specialist work the Guestbook should not duplicate? Model databases, incident databases, software archives and web archives fall in this class. Plan section 2.3 and constitution principle 1 say to record them, not to build rivals [fetched](../constitution/external-archives.md).
3. Is it run by an institution with a track record? Institutions are preferred. An individual-led or beta project is allowed when it is the best available, and the record flags it.
4. Is it likely to last? Signs are a named operator, an archive mandate or a funder, and a funding term that runs beyond the next year. Beta projects, funded phases that end soon and temporary exhibitions count against a resource.
5. Is the licence open? An open licence is preferred because it allows snapshots (constitution principle 4). A closed licence does not exclude a resource, because the metadata record is still kept (constitution principle 4).
6. Can it be read and checked now? A resource that cannot be read is not presented as verified. It appears in section 5 as unverified.

Excluded: link hubs with no records of their own, such as the EU DisinfoLab AI disinfo hub, which collects links to news, events and research and does not record incidents or data [fetched](https://www.disinfo.eu/ai-disinfo-hub/); exhibitions that close and have no lasting archive, which are recorded only through their institution; and resources whose main purpose is product marketing.

## 4. Candidate records

Each record below was verified on 2026-11-15. Claims about the operator, description and status come from the record's `resource_url` or `homepage`. Licence claims come from `licence_source`, unless a field gives another URL. Tags sit next to the claims they support.

### 4.1 Model databases

No verified record. Epoch AI's notable AI models dataset is the obvious candidate. A search result reports it as CC BY 4.0 [search](https://epoch.ai/data/ai-models), but every fetch of the site returned HTTP 403 (section 5). Plan section 37 means the Guestbook should point to such a database, not build one, so this gap should be filled by a pointer once the page can be read.

### 4.2 Incident databases

#### ai-incident-database

```yaml
slug: "ai-incident-database"
name: "AI Incident Database"
role: "Database of reported incidents in which AI systems caused or nearly caused harm"
category: "incident database"
operator: "Responsible AI Collaborative, described on the site as an organisation chartered to advance the database [fetched] https://incidentdatabase.ai/"
homepage: "https://incidentdatabase.ai/"
resource_url: "https://incidentdatabase.ai/"
description: "Public database of AI incident reports with summaries and sources, and a complete-database download under the Research menu; the page shows incident IDs up to 1828 and no total count [fetched]"
verified_on: 2026-11-15
last_known_status: "live; no total count or update date shown [fetched]"
licence: "CC BY-SA 4.0 for the incidents, quickadd, duplicates, taxa, classifications, entities and entity_relationships collections. Not licensed: submissions, the report text field, and the sources of images and videos. [fetched] https://incidentdatabase.ai/terms-of-use/"
licence_source: "https://incidentdatabase.ai/terms-of-use/"
snapshot_eligible: "yes, for the licensed collections only, from the published download, with attribution and share-alike"
local_snapshot: null
notes: "The terms also state that the site must not be commercially exploited without permission, which sits uneasily with CC BY-SA; the terms name a contact address for licensing questions. Terms effective 7 August 2025 [fetched]. High-volume access by bots and spiders is prohibited, so use the download, not a crawl. User submissions fall under a separate agreement that was not read."
```

A dated record of reported AI harms lets a reader check the incidents that testimonies describe, and it is the only verified incident database here with an open licence.

#### oecd-ai-incidents-monitor

```yaml
slug: "oecd-ai-incidents-monitor"
name: "OECD AI Incidents and Hazards Monitor (AIM)"
role: "Monitor of AI incidents and hazards drawn from press coverage, for policy use"
category: "incident database"
operator: "OECD, within the OECD.AI Policy Observatory; the page says its content does not represent official OECD views [fetched] https://oecd.ai/en/incidents"
homepage: "https://oecd.ai/en/"
resource_url: "https://oecd.ai/en/incidents"
description: "Beta monitor. Each record is built from one or more news articles, and classifications and summaries are marked as AI generated. The search counter on the page shows about 19,051 incidents and hazards [fetched]"
verified_on: 2026-11-15
last_known_status: "live, Beta; the newest visible items are dated 14 November 2026 [fetched]"
licence: "Not open. The page footer carries a copyright line reading 2026 OECD, All rights reserved. The linked Terms and conditions page was not read. [fetched] https://oecd.ai/en/"
licence_source: "https://oecd.ai/en/"
snapshot_eligible: "no"
local_snapshot: null
notes: "Labels are machine-generated, so cite the underlying press articles rather than the monitor's classification. The methodology page linked from the site was not read."
```

Testimonies that describe a reported AI harm can be checked against a dated, press-based monitor, provided readers treat its labels as automated.

### 4.3 Annual reports

#### stanford-ai-index

```yaml
slug: "stanford-ai-index"
name: "Artificial Intelligence Index Report (Stanford AI Index)"
role: "Report of data and analysis on the state of AI; 2026 edition read"
category: "annual report"
operator: "Stanford Institute for Human-Centered AI (Stanford HAI), which describes the AI Index as an independent initiative at the institute [fetched] https://hai.stanford.edu/ai-index"
homepage: "https://hai.stanford.edu/ai-index"
resource_url: "https://hai.stanford.edu/ai-index/2026-ai-index-report"
description: "The 2026 report is offered as a PDF, with a Chinese translation also linked. The page shows no publication date [fetched]"
verified_on: 2026-11-15
last_known_status: "live; no publication date shown [fetched]"
licence: "Not stated on the page. The footer reads Stanford University with a link to general copyright and terms pages [fetched]. A search summary reports either CC BY or CC BY-ND [search] https://casrai.org/guides/stanford-ai-index"
licence_source: "https://hai.stanford.edu/ai-index/2026-ai-index-report"
snapshot_eligible: "unknown"
local_snapshot: null
notes: "Read the licence statement inside the PDF before any copy. CC BY-ND would bar adapted versions. A search copy of the report also gives Attribution-NoDerivatives 4.0 [search] https://studylib.net/doc/28612293/ai-index-report-2026, which is not an authoritative source."
```

An annual report gives dated baseline figures against which testimonies about adoption, work and trust can be read.

#### state-of-ai-report

```yaml
slug: "state-of-ai-report"
name: "State of AI Report"
role: "Annual report on the state of AI, produced by a named individual with a firm"
category: "annual report"
operator: "Nathan Benaich, with Air Street Capital; an individual-led project, not an institution [fetched] https://www.stateof.ai/about"
homepage: "https://www.stateof.ai/about"
resource_url: "https://www.stateof.ai/about"
description: "Report published annually since 2018, edited and produced by Nathan Benaich with researchers, investors and practitioners [fetched] https://www.stateof.ai/about"
verified_on: 2026-11-15
last_known_status: "live; the about page is readable; individual edition pages were not opened"
licence: "CC BY 4.0: 'This work is licensed under a Creative Commons Attribution 4.0 International License.' [fetched] https://www.stateof.ai/about"
licence_source: "https://www.stateof.ai/about"
snapshot_eligible: "yes, with attribution under CC BY 4.0"
local_snapshot: null
notes: "This is the only verified annual report with an open licence. It is individual-led, which is an exception to the institutional preference (question 2). The site asks for citation with attribution."
```

It is the openly licensed annual report in the set, so it is the first candidate for a full snapshot of each edition.

### 4.4 Policy and law trackers

#### eur-lex-ai-act

```yaml
slug: "eur-lex-ai-act"
name: "Regulation (EU) 2024/1689 (Artificial Intelligence Act) on EUR-Lex"
role: "Official text of the EU Artificial Intelligence Act"
category: "policy and law tracker"
operator: "Publications Office of the European Union, which operates EUR-Lex; the legal notice names its copyright contact [fetched] https://eur-lex.europa.eu/content/legal-notice/legal-notice.html. The AI Act page does not name its publisher [fetched] https://eur-lex.europa.eu/eli/reg/2024/1689/oj"
homepage: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"
resource_url: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"
description: "Regulation of 13 June 2024 laying down harmonised rules on artificial intelligence. Published in the Official Journal as OJ L, 2024/1689, 12.7.2024, with ELI identifier http://data.europa.eu/eli/reg/2024/1689/oj [fetched]"
verified_on: 2026-11-15
last_known_status: "live; the page is about 442,000 characters and the first 100,000 were read [fetched]"
licence: "Legal documents may be reused for commercial and non-commercial purposes unless stated otherwise, under Commission Decision 2011/833/EU. Editorial content, summaries and consolidated texts are CC BY 4.0. Third-party content may need the rights holder's permission. Metadata is CC0 1.0. [fetched] https://eur-lex.europa.eu/content/legal-notice/legal-notice.html"
licence_source: "https://eur-lex.europa.eu/content/legal-notice/legal-notice.html"
snapshot_eligible: "yes, for the legal text under the reuse policy, with source acknowledgement"
local_snapshot: null
notes: "The copyright notice at the end of the AI Act page was not reached, so confirm it before a copy. Use the ELI as the canonical reference. Consolidated texts change with amendments, so a snapshot should carry the Official Journal reference and its date."
```

Testimonies about being screened, scored or refused by AI systems in the EU can be read against the official legal text that sets the rules.

#### oecd-ai-policy-observatory

```yaml
slug: "oecd-ai-policy-observatory"
name: "OECD.AI Policy Observatory"
role: "Policy observatory on trustworthy AI: national policies, tools and metrics, incidents and reporting"
category: "policy and law tracker"
operator: "OECD [fetched] https://oecd.ai/en/"
homepage: "https://oecd.ai/en/"
resource_url: "https://oecd.ai/en/"
description: "Platform with a policy toolkit for mapping national AI policy, an OECD.AI Index of progress on the OECD AI Recommendation, a catalogue of tools and metrics, the Hiroshima AI Reporting Framework, and themed areas including generative AI and the future of work [fetched]"
verified_on: 2026-11-15
last_known_status: "live; 2026 copyright line; the update dates of individual pages are not shown [fetched]"
licence: "Not open. Footer copyright line 2026 OECD, All rights reserved; the linked Terms and conditions page was not read [fetched] https://oecd.ai/en/"
licence_source: "https://oecd.ai/en/"
snapshot_eligible: "no"
local_snapshot: null
notes: "Policy pages change often, so this record needs the yearly check in section 6. The Index and the policy toolkit are the parts most likely to change."
```

Policy disputes and national AI rules recur in testimonies, and this observatory is a comparative map of national policy that readers can link to, though not copy.

### 4.5 Public-opinion surveys

#### pew-research-center-ai

```yaml
slug: "pew-research-center-ai"
name: "Pew Research Center, artificial intelligence topic"
role: "Survey research on public attitudes to AI, with reports and datasets"
category: "public-opinion survey"
operator: "Pew Research Center, described as a nonpartisan, nonadvocacy fact tank and a subsidiary of The Pew Charitable Trusts [fetched] https://www.pewresearch.org/topic/internet-technology/emerging-technology/artificial-intelligence/"
homepage: "https://www.pewresearch.org/topic/internet-technology/emerging-technology/artificial-intelligence/"
resource_url: "https://www.pewresearch.org/topic/internet-technology/emerging-technology/artificial-intelligence/"
description: "Topic page listing AI reports. The most recent shown is 'Americans Are Open to AI in Healthcare, but Want Humans Making Final Calls', published 29 October 2026 [fetched]"
verified_on: 2026-11-15
last_known_status: "live; topic page readable; report pages not opened"
licence: "Pew Terms of Use, effective 05/25/2018. Use is permitted subject to attribution. Republication in whole or in principal part needs Pew's express written permission. Survey datasets are limited to excerpts. American Trends Panel datasets are governed by separate terms. [fetched] https://www.pewresearch.org/about/terms-and-conditions/"
licence_source: "https://www.pewresearch.org/about/terms-and-conditions/"
snapshot_eligible: "no; metadata and citation only"
local_snapshot: null
notes: "The Terms give a citation format: 'Report Title.' Pew Research Center, Washington, D.C. (Publication date) URL [fetched] https://www.pewresearch.org/about/terms-and-conditions/. Use short excerpts with attribution."
```

Pew's dated survey reports give readers a record of American attitudes to AI, against which individual testimonies can be placed.

#### ipsos-ai-monitor

```yaml
slug: "ipsos-ai-monitor"
name: "Ipsos AI Monitor"
role: "Multi-country survey of public attitudes to AI"
category: "public-opinion survey"
operator: "Ipsos [fetched] https://www.ipsos.com/en/global-attitudes-ai-2026-wonder-vs-worry-divide-deepens"
homepage: "https://www.ipsos.com/en/global-attitudes-ai-2026-wonder-vs-worry-divide-deepens"
resource_url: "https://www.ipsos.com/en/global-attitudes-ai-2026-wonder-vs-worry-divide-deepens"
description: "2026 edition, the fifth annual edition, covering 32 countries and published 2 June 2026. The page says excitement and nervousness about AI are now nearly equal worldwide. The report is a download; respondent numbers are not on the page [fetched]"
verified_on: 2026-11-15
last_known_status: "live; the report PDF was not opened [fetched]"
licence: "Not open. The page carries an Ipsos All Rights Reserved line, dated 2016 to 2026. Legal Mentions were not read. [fetched] https://www.ipsos.com/en/global-attitudes-ai-2026-wonder-vs-worry-divide-deepens"
licence_source: "https://www.ipsos.com/en/global-attitudes-ai-2026-wonder-vs-worry-divide-deepens"
snapshot_eligible: "no"
local_snapshot: null
notes: "Country figures in secondary coverage were not checked against the report and are not used here [search] https://www.ipsos.com/en/global-attitudes-ai-2026-wonder-vs-worry-divide-deepens. Cite the Ipsos page until the PDF is read."
```

Cross-national survey data on excitement and worry about AI gives testimonies from different countries a shared reference point.

#### eurobarometer-ai

```yaml
slug: "eurobarometer-ai"
name: "Eurobarometer surveys on artificial intelligence"
role: "European Commission opinion surveys on AI, including the 2025 survey on AI and the future of work"
category: "public-opinion survey"
operator: "European Commission; its digital strategy site published the news item [fetched] https://digital-strategy.ec.europa.eu/en/news/commission-survey-shows-most-europeans-support-use-artificial-intelligence-workplace"
homepage: "https://europa.eu/eurobarometer/screen/home"
resource_url: "https://digital-strategy.ec.europa.eu/en/news/commission-survey-shows-most-europeans-support-use-artificial-intelligence-workplace"
description: "News item of 13 February 2025. It reports that more than 60 percent of Europeans view robots and AI at work positively, over 70 percent think AI improves productivity, and 84 percent think AI needs careful management for privacy and transparency. It links survey detail 3222 [fetched]"
verified_on: 2026-11-15
last_known_status: "live, partly read; the Eurobarometer portal returned only its title, and survey 3222 was not opened [fetched] https://europa.eu/eurobarometer/screen/home"
licence: "Not read. The page has a copyright notice link whose text was not retrieved [fetched]"
licence_source: "none read"
snapshot_eligible: "unknown"
local_snapshot: null
notes: "Partly verified. Before publication, open the survey detail page and its copyright notice. A search result gives Special Eurobarometer 554 for this survey [search] https://www.cec-managers.org/wp-content/uploads/2025/02/Artificial-Intelligence-and-the-future-of-work_SP554__report_en.pdf, which was not confirmed."
```

EU-wide survey data on how people view AI at work gives testimonies about work a reference beyond one country.

### 4.6 Labour and education studies

#### ilo-generative-ai-jobs

```yaml
slug: "ilo-generative-ai-jobs"
name: "Generative AI and Jobs: A Refined Global Index of Occupational Exposure (ILO Working Paper 140)"
role: "Index of how exposed occupations are to generative AI"
category: "labour study"
operator: "International Labour Organization [fetched] https://www.ilo.org/publications/generative-ai-and-jobs-refined-global-index-occupational-exposure"
homepage: "https://www.ilo.org/publications/generative-ai-and-jobs-refined-global-index-occupational-exposure"
resource_url: "https://www.ilo.org/publications/generative-ai-and-jobs-refined-global-index-occupational-exposure"
description: "Working paper published 20 May 2025 by eight ILO authors, listed as ILO Working Paper 140, with DOI 10.54394/HETP0387 [fetched]"
verified_on: 2026-11-15
last_known_status: "live; page readable; PDF not opened [fetched]"
licence: "Not stated in the page text; no copyright or Creative Commons line was found on the page [fetched]"
licence_source: "https://www.ilo.org/publications/generative-ai-and-jobs-refined-global-index-occupational-exposure"
snapshot_eligible: "unknown"
local_snapshot: null
notes: "The PDF or the ILO terms may state a licence; check before any copy. Check for later ILO updates to the index. Only one verified labour study is on the shelf, so this category is thin."
```

Occupational exposure estimates let a reader check testimonies about specific jobs against a published figure.

#### unesco-genai-education-guidance

```yaml
slug: "unesco-genai-education-guidance"
name: "Guidance for Generative AI in Education and Research"
role: "UNESCO guidance on the use of generative AI in education and research"
category: "education study"
operator: "UNESCO, per the library record [fetched] https://connect.unevoc.unesco.org/home/UNEVOC+Publications/lang=en/akt=detail/qs=6696"
homepage: "https://connect.unevoc.unesco.org/home/UNEVOC+Publications/lang=en/akt=detail/qs=6696"
resource_url: "https://connect.unevoc.unesco.org/home/UNEVOC+Publications/lang=en/akt=detail/qs=6696"
description: "Title, publisher and year 2023 from the library record [fetched]. Authors Fengchun Miao and Wayne Holmes from a search result [search] https://discovery.ucl.ac.uk/id/eprint/10176438/1/Miao%20and%20Holmes%20-%202023%20-%20Guidance%20for%20Generative%20AI%20in%20Education%20and%20Resear.pdf"
verified_on: 2026-11-15
last_known_status: "live library record; the UNESDOC record was not read"
licence: "CC BY-SA according to the UNEVOC library record [fetched]. A search summary says the PDF carries a UNESCO 2023 copyright notice [search], which conflicts with that licence."
licence_source: "https://connect.unevoc.unesco.org/home/UNEVOC+Publications/lang=en/akt=detail/qs=6696"
snapshot_eligible: "unknown"
local_snapshot: null
notes: "Resolve the licence on the official UNESDOC record before any copy. Education testimonies that react to classroom AI rules can be read against this public-authority statement."
```

Public-authority guidance on generative AI in schools is a reference point for testimonies about teaching and learning.

### 4.7 Generated-media and misinformation trackers

#### political-deepfakes-incidents-database

```yaml
slug: "political-deepfakes-incidents-database"
name: "Political Deepfakes Incidents Database (PDID)"
role: "Beta database of political deepfakes and cheapfakes, with a codebook for media type, disclosure, framing and harm"
category: "generated-media and misinformation tracker"
operator: "GRAIL, the Governance and Responsible AI Lab [fetched] https://www.grail-lab.org/pdid/. The Purdue University researchers behind it are named in a search result [search] https://cla.purdue.edu/news/college/2024/itn-tracking-political-deepfakes.html"
homepage: "https://www.grail-lab.org/pdid/"
resource_url: "https://www.grail-lab.org/pdid/"
description: "Codebook covers media type and authenticity, sources and targets, disclosure and verification, framing, circulation and harms. Charts show 420 subject-matter posts dated October 2026 [fetched]"
verified_on: 2026-11-15
last_known_status: "live; labelled Beta; no total count shown [fetched]"
licence: "Not stated. The footer reads 2026 GRAIL with an accessibility link [fetched] https://www.grail-lab.org/pdid/"
licence_source: "https://www.grail-lab.org/pdid/"
snapshot_eligible: "no"
local_snapshot: null
notes: "Beta and lab-run, so it carries a custodial risk. The page does not say whether the data can be downloaded; check before any snapshot. This is the only verified tracker in the category, so coverage is thin."
```

Political deepfakes shape what people in testimonies say they can trust, and this database records those cases in a structured form.

### 4.8 Web and software archives

#### internet-archive

```yaml
slug: "internet-archive"
name: "Internet Archive and Wayback Machine"
role: "Public web archive that stores dated captures of web pages and other digital material"
category: "web archive"
operator: "Internet Archive. The Wayback help page is from the Archive [fetched] https://help.archive.org/help/using-the-wayback-machine/; the terms page returned only its title, so the name comes from that title [fetched] https://archive.org/about/terms.php"
homepage: "https://archive.org/about/terms.php"
resource_url: "https://help.archive.org/help/using-the-wayback-machine/"
description: "Help page for the Wayback Machine. It explains that site owners can ask for exclusion by email and that the Archive makes no guarantee of the outcome [fetched]"
verified_on: 2026-11-15
last_known_status: "live, partly read; the terms page returned only its title"
licence: "No licence for archived content is named in the pages read. The help page says 'Our terms of use do not cover backups for the general public.' [fetched] https://help.archive.org/help/using-the-wayback-machine/"
licence_source: "https://help.archive.org/help/using-the-wayback-machine/"
snapshot_eligible: "no; cite capture URLs and timestamps instead"
local_snapshot: null
notes: "Do not copy captures into an edition. Owners can request exclusion, and the Archive does not guarantee the outcome, so keep the capture URL and its timestamp in the context material that cites the page."
```

A dated capture gives a fallback when a page that testimonies or context material cite disappears.

#### common-crawl

```yaml
slug: "common-crawl"
name: "Common Crawl"
role: "Open repository of web crawl data for research"
category: "web archive (dataset)"
operator: "The Common Crawl Foundation, a 501(c)(3) non-profit founded in 2007 [fetched] https://commoncrawl.org/"
homepage: "https://commoncrawl.org/"
resource_url: "https://commoncrawl.org/"
description: "Repository of over 300 billion pages spanning 15 years, adding 3 to 5 billion pages a month. The homepage says it has been cited in over 10,000 research papers [fetched]"
verified_on: 2026-11-15
last_known_status: "live; latest crawl date not shown [fetched]"
licence: "Limited licence under the Terms of Use, last updated 7 March 2024. Crawled content may be subject to its owners' terms, and users must respect third-party rights. No open dataset licence is named. [fetched] https://commoncrawl.org/terms-of-use"
licence_source: "https://commoncrawl.org/terms-of-use"
snapshot_eligible: "no; the terms do not license the crawled pages"
local_snapshot: null
notes: "The homepage says the repository 'can be used by anyone', which is not a licence. Metadata and index references only."
```

Testimonies about web content and training data can be traced to a public crawl that research cites widely.

#### software-heritage

```yaml
slug: "software-heritage"
name: "Software Heritage"
role: "Archive of publicly available source code, described by its operator as the universal software archive"
category: "web and software archive"
operator: "Inria initiated the archive, in collaboration with UNESCO [fetched] https://www.softwareheritage.org/. Inria owns the trademark [fetched] https://www.softwareheritage.org/legal/"
homepage: "https://www.softwareheritage.org/"
resource_url: "https://www.softwareheritage.org/"
description: "Describes itself as building the universal software archive. Sponsors listed include Microsoft, CEA, CNRS, Amazon Web Services, Google and GitHub. Archive size counters did not load [fetched]"
verified_on: 2026-11-15
last_known_status: "live; size counters did not load [fetched]"
licence: "Not stated on the pages read. The linked Bulk Access and API Terms of Use were not read. [fetched] https://www.softwareheritage.org/legal/"
licence_source: "https://www.softwareheritage.org/legal/"
snapshot_eligible: "unknown; do not snapshot the archive"
local_snapshot: null
notes: "Read the linked Bulk Access and API terms before citing or reusing archived code."
```

Source code for the models and tools that testimonies discuss is kept here, so the shelf can point to it rather than hold a copy.

#### arxiv

```yaml
slug: "arxiv"
name: "arXiv"
role: "Preprint repository for scholarly material; much AI research is posted there [inference]"
category: "research repository (outside the listed categories)"
operator: "Not named on the licence page read [fetched] https://info.arxiv.org/help/license/index.html"
homepage: "https://info.arxiv.org/help/license/index.html"
resource_url: "https://info.arxiv.org/help/license/index.html"
description: "The licence page describes arXiv as 'a repository for scholarly material' and acknowledges major funders and member institutions without naming them [fetched]"
verified_on: 2026-11-15
last_known_status: "live; the licence page was read; the main site was not opened"
licence: "Metadata under CC0 1.0. Each paper carries the author's choice of one of seven licences: CC BY 4.0, CC BY-SA 4.0, CC BY-NC-SA 4.0, CC BY-NC-ND 4.0, the arXiv non-exclusive licence 1.0, or CC0. The choice is irrevocable. [fetched] https://info.arxiv.org/help/license/index.html"
licence_source: "https://info.arxiv.org/help/license/index.html"
snapshot_eligible: "metadata: yes (CC0). Papers: only under CC BY 4.0, CC BY-SA 4.0 or CC0 [inference]"
local_snapshot: null
notes: "The operator is not named on the page read, so confirm it on the arXiv site before publication. Papers under the non-exclusive licence or a non-commercial licence are not open for copying [inference]."
```

Research papers are the primary sources for many AI claims that testimonies repeat, and the shelf needs a stable pointer to them rather than copies.

#### bnf-web-archive

```yaml
slug: "bnf-web-archive"
name: "Bibliothèque nationale de France web archive (legal deposit)"
role: "National archive of French websites collected under web legal deposit"
category: "web archive"
operator: "Bibliothèque nationale de France [fetched] https://www.bnf.fr/en/conducting-research-web-archives"
homepage: "https://www.bnf.fr/en/conducting-research-web-archives"
resource_url: "https://www.bnf.fr/en/conducting-research-web-archives"
description: "Web collections consultable from BnF research rooms and a network of partner libraries, through the 'Archives de l'internet' and 'Archives de l'internet Labs' applications. Radio and TV sites under the INA are excluded [fetched]"
verified_on: 2026-11-15
last_known_status: "live; remote online access not confirmed on the page [fetched]"
licence: "No reuse or copyright statement on the page read. A linked page on access and reuse was not read. [fetched] https://www.bnf.fr/en/conducting-research-web-archives"
licence_source: "https://www.bnf.fr/en/conducting-research-web-archives"
snapshot_eligible: "no; access is limited to research rooms and partner libraries"
local_snapshot: null
notes: "Access is restricted on site, as the page states. Whether any part of the collection is online remotely is not confirmed on the page read."
```

It is the national record of French websites, and the place to look when a French web source cited in a testimony has disappeared.

### 4.9 Museums and exhibitions

#### ars-electronica-archive

```yaml
slug: "ars-electronica-archive"
name: "Ars Electronica Archive"
role: "Digital archive of Ars Electronica's media-art projects, including its AI-related material"
category: "museum and exhibition"
operator: "Ars Electronica Linz GmbH & Co KG, per the page footer [fetched] https://ars.electronica.art/archive/en/projects/"
homepage: "https://ars.electronica.art/archive/en/projects/"
resource_url: "https://ars.electronica.art/archive/en/projects/"
description: "Lists 15 projects. The AI Lab showcase documents the European ARTificial Intelligence Lab's activities, partners and juries from 2018 to 2021 [fetched]. A search summary notes a permanent AI exhibition at the Ars Electronica Center since 2019 [search] https://ars.electronica.art/aeblog/en/2024/08/23/how-the-ars-electronica-archive-reflects-the-development-of-artificial-intelligence/"
verified_on: 2026-11-15
last_known_status: "live; project pages not opened [fetched]"
licence: "Not open. The footer reads All Rights Reserved; the imprint page was not read. [fetched] https://ars.electronica.art/archive/en/projects/"
licence_source: "https://ars.electronica.art/archive/en/projects/"
snapshot_eligible: "no"
local_snapshot: null
notes: "AI material is a small part of this archive, so the record is for the institution's AI-related projects only."
```

A media-art institution's documentation of AI projects can be read alongside testimonies about creative work.

#### zkm-exhibitions

```yaml
slug: "zkm-exhibitions"
name: "ZKM | Center for Art and Media Karlsruhe, exhibitions"
role: "Art and media museum; its exhibitions page lists a current AI-focused exhibition"
category: "museum and exhibition"
operator: "ZKM | Center for Art and Media Karlsruhe [fetched] https://zkm.de/en/exhibitions"
homepage: "https://zkm.de/en/exhibitions"
resource_url: "https://zkm.de/en/exhibitions"
description: "Lists 'Agentic Constellations. Cartography of the Hidden', about autonomous AI agents exploring internet data and visualising it, closing 7 February 2027 [fetched]. The opening date is not on the page; a search summary gives 23 October 2026 [search] https://zkm.de/en/exhibitions"
verified_on: 2026-11-15
last_known_status: "live; the exhibition is temporary and closes 7 February 2027, so this record needs a check after that date"
licence: "Not read; no licence was seen on the page [fetched]"
licence_source: "none read"
snapshot_eligible: "no; not checked, assume all rights reserved"
local_snapshot: null
notes: "Exhibitions are temporary, so the record should point to the museum's AI programme and collection rather than to the show alone. Online collection terms were not checked."
```

A media-art museum's AI programme shows how the art world frames AI, which helps readers place testimonies about creative work.

### 4.10 Oral-history and testimony projects

#### computer-history-museum-oral-histories

```yaml
slug: "computer-history-museum-oral-histories"
name: "Computer History Museum oral history catalogue"
role: "Catalogue of recorded oral-history interviews with people who built computing, several on AI"
category: "oral history"
operator: "Computer History Museum [fetched] https://www.computerhistory.org/collections/catalog/oral-history"
homepage: "https://www.computerhistory.org/collections/catalog/oral-history"
resource_url: "https://www.computerhistory.org/collections/catalog/oral-history"
description: "Lists 18 oral histories with short summaries and catalogue links. AI-related interviews named on the page include John McCarthy, Edward Feigenbaum (interviewed by Donald Knuth) and Judea Pearl. The page gives no interview dates [fetched]"
verified_on: 2026-11-15
last_known_status: "live; individual catalogue records not opened [fetched]"
licence: "No reuse, licence or copyright terms on the listing page [fetched]"
licence_source: "https://www.computerhistory.org/collections/catalog/oral-history"
snapshot_eligible: "unknown; no snapshot"
local_snapshot: null
notes: "Check each catalogue record and the museum's terms before quoting transcripts or video."
```

First-hand accounts from people who built early AI show where the systems that testimonies now describe came from.

#### oral-history-digital

```yaml
slug: "oral-history-digital"
name: "Oral-History.Digital"
role: "Platform for scholarly collections of audio-visual narrative interviews"
category: "oral history"
operator: "Not named on the page read. Five partner institutions are listed, including the University Library of Freie Universität Berlin; the continuation of the platform under that university is an inference [fetched] https://www.oral-history.digital/en/projekt/index.html"
homepage: "https://www.oral-history.digital/en/projekt/index.html"
resource_url: "https://www.oral-history.digital/en/projekt/index.html"
description: "Lists 42 archives, 202 collections and 4113 interviews from 46 institutions. Registered users can view files with subtitles and annotate them. Funded by the DFG under e-Research Technologies since 2020, second phase 2023 to 2026 [fetched]"
verified_on: 2026-11-15
last_known_status: "live; the funded second phase ends in 2026, so continuity is unconfirmed [fetched]"
licence: "No licence stated for the interviews or metadata. The software is described as available as Open Source, with no licence named. The legal notice was not read. [fetched] https://www.oral-history.digital/en/projekt/index.html"
licence_source: "https://www.oral-history.digital/en/projekt/index.html"
snapshot_eligible: "no; access depends on registration and rights management"
local_snapshot: null
notes: "This is a general oral-history platform, not AI-specific. Continuity after 2026 is the main risk."
```

It shows how other projects hold first-person interviews under rights management, which is the nearest existing model for the Guestbook's own consent and access rules [inference].

## 5. Unverified candidates and excluded resources

These are not counted in the 22 records.

- Epoch AI, notable AI models dataset and models database, <https://epoch.ai/data/ai-models>. The models page and the data hub returned HTTP 403, the llms.txt file returned a connection reset, and the CSV returned HTTP 403. A search result reports the notable models dataset as CC BY 4.0 [search] <https://epoch.ai/data/ai-models>, and an Epoch post says its work is under CC BY [search] <https://x.com/EpochAIResearch/status/1976668882162372986>. Excluded until a fetch succeeds.
- OECD Digital Education Outlook 2026, <https://www.oecd.org/en/publications/oecd-digital-education-outlook-2026_062a7394-en.html>. HTTP 403. A search result gives the title and a publication date of 19 January 2026 [search]. The DOI route redirected to a third-party blog and was not followed.
- Eurofound, algorithmic management in European workplaces, <https://www.eurofound.europa.eu/en/publications/all/algorithmic-management-in-european-workplaces>. Connection reset. Search only [search].
- Charles Babbage Institute oral histories, <https://conservancy.umn.edu/handle/11299/107544>. HTTP 403. Search results list interviews with Saul Amarel, Allen Newell, George Heilmeier and Lawrence Roberts on ARPA and AI [search]. This would be the strongest early-AI testimony candidate, once readable.
- Smithsonian Computer Oral History Collection, <https://sova.si.edu/record/nmah.ac.0196>. HTTP 403. A search summary says some transcripts are online and the collection is open for research [search].
- OECD terms and conditions. Linked from the OECD footer and not read, so OECD licence statements rest on the footer copyright line alone.
- Council of Europe Framework Convention on AI. Search only. Not proposed, because policy coverage is already provided by EUR-Lex and OECD.AI [inference].
- EU DisinfoLab AI disinfo hub, <https://www.disinfo.eu/ai-disinfo-hub/>. Read, but it is a curated link hub, not a tracker. It fails the selection test in section 3 [fetched].
- Computer History Museum Extended Reality exhibition, read on <https://computerhistory.org/blog/ai-guided-tour-project/>. Open from 1 October 2026 to 28 March 2027 [fetched]. Not proposed, because it is about extended reality, including AI glasses, rather than AI.

## 6. Risks, verification cadence and snapshots

Risks:

1. Link rot. The repository research note records a Pew finding that about a quarter of pages that existed between 2013 and 2023 were no longer accessible in October 2023 [search] ([custodial research](../research/custodial-indie-projects.md)). The figure was not re-checked here.
2. Change of operator. Papers With Code was shut down in July 2025 and its domain redirected to Hugging Face [search] <https://hyper.ai/en/news/42900>. The `operator` field exists to catch this kind of change.
3. Change of licence. The AI Incident Database terms are dated 7 August 2025 [fetched] <https://incidentdatabase.ai/terms-of-use/>, so the licence can change, and the record must carry its date.
4. Funding and beta status. The second funded phase of Oral-History.Digital ends in 2026 [fetched] <https://www.oral-history.digital/en/projekt/index.html>. The OECD monitor and the PDID are labelled Beta [fetched] <https://oecd.ai/en/incidents> and <https://www.grail-lab.org/pdid/>.
5. Temporary exhibitions. The ZKM AI exhibition closes on 7 February 2027 [fetched] <https://zkm.de/en/exhibitions>.

Verification cadence, proposed:

1. Full check of every record once a year, in November, with the `verified_on` date updated for each record read.
2. An extra check of the relevant annual report within a month of each new edition (Stanford AI Index, State of AI Report, Ipsos AI Monitor).
3. Each check reads `resource_url` and `licence_source`. Any change to the licence text, a redirect, or a 403 or 404 response is logged in `notes` and reviewed before the record is changed.
4. A script to do this check is proposed, for example a PowerShell or Node script under `scripts/` that reads the shelf files, requests each URL, records the status and a hash of the licence text, and reports changes. AGENTS.md asks for repeated operations to be scripted; this is not written here.

What to snapshot first, if the owner approves:

1. The State of AI Report PDF of each edition, which is CC BY 4.0, with its checksum and date.
2. The AI Incident Database licensed collections, from the published download, under CC BY-SA 4.0, with attribution and share-alike.
3. The Official Journal text of the AI Act on EUR-Lex, with its ELI and date.
4. arXiv metadata for papers on the shelf (CC0), and the paper itself only where its per-paper licence is open.
5. Nothing else. For all-rights-reserved resources, keep the metadata and a dated capture link, and decide any private preservation copy only after the legal review under [project licensing](project-licensing.md) (issue #43).

## 7. Open questions for the owner

1. Field names. Plan section 18 uses `id`, `accessed_or_verified` and `license`. Data model section 2.14 and the identifier specification use `slug`, `verified_on` and `licence`. This proposal follows the data model. Should the plan's example be amended to match? That is a plan change.
2. Institutional preference. The State of AI Report is produced by an individual with a firm. Is an individual-led source acceptable as an exception?
3. Metadata-only records. May all-rights-reserved resources be kept as metadata-only records? Should a private preservation copy be permitted, subject to the legal review under issue #43?
4. Exhibitions. Are temporary exhibitions in scope, or only an institution's AI programme and archive?
5. Model databases. Should Epoch AI be added on search evidence, or wait until a fetch succeeds? If the owner can open it from another network, a check would take minutes.
6. Scope. Are arXiv and Common Crawl in scope, although they sit outside the listed categories?
7. Language. The public shelf must be in French and English (AGENTS.md). The descriptions here are in English only. Who writes and checks the French?
8. Cadence and script. Is a yearly check acceptable, and should the script in section 6 be written?
9. Index. Should this proposal be indexed in docs/README.md once the owner has reviewed it? It has not been added there in this pass.

## 8. Sources

Fetched on 2026-11-15:

- [S1] <https://incidentdatabase.ai/> - fetched. Operator description, incident IDs, absence of total count and update date.
- [S2] <https://incidentdatabase.ai/terms-of-use/> - fetched. Licence terms, effective 7 August 2025.
- [S3] <https://oecd.ai/en/incidents> - fetched. AIM description, count, AI-generated labels, footer copyright line.
- [S4] <https://oecd.ai/en/> - fetched. OECD.AI scope and footer copyright line.
- [S5] <https://hai.stanford.edu/ai-index> - fetched. AI Index programme description; no licence stated.
- [S6] <https://hai.stanford.edu/ai-index/2026-ai-index-report> - fetched. PDF and translation links; footer copyright line.
- [S7] <https://www.stateof.ai/about> - fetched. Producer, annual publication since 2018, CC BY 4.0.
- [S8] <https://eur-lex.europa.eu/eli/reg/2024/1689/oj> - fetched. Title, OJ reference and ELI identifier.
- [S9] <https://eur-lex.europa.eu/content/legal-notice/legal-notice.html> - fetched. Reuse policy, CC BY 4.0 for editorial content, CC0 metadata.
- [S10] <https://www.pewresearch.org/topic/internet-technology/emerging-technology/artificial-intelligence/> - fetched. Operator description and latest listed report.
- [S11] <https://www.pewresearch.org/about/terms-and-conditions/> - fetched. Terms of Use effective 05/25/2018.
- [S12] <https://www.ipsos.com/en/global-attitudes-ai-2026-wonder-vs-worry-divide-deepens> - fetched. Publication date, 32 countries, copyright line.
- [S13] <https://digital-strategy.ec.europa.eu/en/news/commission-survey-shows-most-europeans-support-use-artificial-intelligence-workplace> - fetched. Commission news item of 13 February 2025 and headline figures.
- [S14] <https://europa.eu/eurobarometer/screen/home> - fetched, title only.
- [S15] <https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2025> - fetched, teasers only.
- [S16] <https://www.ilo.org/publications/generative-ai-and-jobs-refined-global-index-occupational-exposure> - fetched. Title, date, authors count, DOI.
- [S17] <https://connect.unevoc.unesco.org/home/UNEVOC+Publications/lang=en/akt=detail/qs=6696> - fetched. Title, publisher, year and CC BY-SA licence.
- [S18] <https://www.grail-lab.org/pdid/> - fetched. Codebook, charts, Beta label, footer.
- [S19] <https://help.archive.org/help/using-the-wayback-machine/> - fetched. Exclusion requests and terms wording.
- [S20] <https://archive.org/about/terms.php> - fetched, title only.
- [S21] <https://commoncrawl.org/> - fetched. Operator, scale, citation count.
- [S22] <https://commoncrawl.org/terms-of-use> - fetched. Terms of Use last updated 7 March 2024.
- [S23] <https://www.softwareheritage.org/> - fetched. Operator, partners, counters that did not load.
- [S24] <https://www.softwareheritage.org/legal/> - fetched. Trademark owner, linked terms not read.
- [S25] <https://info.arxiv.org/help/license/index.html> - fetched. Metadata CC0 and the seven per-paper licences.
- [S26] <https://www.bnf.fr/en/conducting-research-web-archives> - fetched. Access routes and exclusions.
- [S27] <https://ars.electronica.art/archive/en/projects/> - fetched. Operator, 15 projects, AI Lab showcase, All Rights Reserved.
- [S28] <https://zkm.de/en/exhibitions> - fetched. AI exhibition and closing date.
- [S29] <https://www.computerhistory.org/collections/catalog/oral-history> - fetched. 18 oral histories and AI-related names.
- [S30] <https://www.oral-history.digital/en/projekt/index.html> - fetched. Counts, funding, software licence statement.
- [S31] <https://computerhistory.org/blog/ai-guided-tour-project/> - fetched. Exhibition dates; excluded.
- [S32] <https://www.disinfo.eu/ai-disinfo-hub/> - fetched. Hub description; excluded.

Search results, not opened (lower confidence):

- [S33] <https://epoch.ai/data/ai-models> - search. CC BY 4.0 for the notable models dataset. The page itself returned HTTP 403.
- [S34] <https://x.com/EpochAIResearch/status/1976668882162372986> - search. Epoch statement that its work is under CC BY.
- [S35] <https://casrai.org/guides/stanford-ai-index> - search. Reports CC BY or CC BY-ND for the AI Index.
- [S36] <https://studylib.net/doc/28612293/ai-index-report-2026> - search. Copy of the report stating Attribution-NoDerivatives 4.0.
- [S37] <https://cla.purdue.edu/news/college/2024/itn-tracking-political-deepfakes.html> - search. Purdue researchers behind the PDID.
- [S38] <https://ars.electronica.art/aeblog/en/2024/08/23/how-the-ars-electronica-archive-reflects-the-development-of-artificial-intelligence/> - search. Permanent AI exhibition at the Ars Electronica Center since 2019.
- [S39] <https://hyper.ai/en/news/42900> - search. Papers With Code shutdown and redirect to Hugging Face.
- [S40] <https://www.oecd.org/en/publications/oecd-digital-education-outlook-2026_062a7394-en.html> - search. Title and date; the page returned HTTP 403.
- [S41] <https://www.eurofound.europa.eu/en/publications/all/algorithmic-management-in-european-workplaces> - search. The page returned a connection reset.
- [S42] <https://conservancy.umn.edu/handle/11299/107544> - search. CBI interview listings; the page returned HTTP 403.
- [S43] <https://sova.si.edu/record/nmah.ac.0196> - search. Smithsonian collection; the page returned HTTP 403.
- [S44] <https://europa.eu/eurobarometer/surveys/detail/3222> - search. Survey detail identifier; not opened.
- [S45] <https://www.cec-managers.org/wp-content/uploads/2025/02/Artificial-Intelligence-and-the-future-of-work_SP554__report_en.pdf> - search. Special Eurobarometer 554 report on AI and the future of work; not opened.
- [S46] <https://discovery.ucl.ac.uk/id/eprint/10176438/1/Miao%20and%20Holmes%20-%202023%20-%20Guidance%20for%20Generative%20AI%20in%20Education%20and%20Resear.pdf> - search. Title and authors of the UNESCO guidance; not opened.

Repository documents read directly (fetched):

- [S47] [Plan](../plans/main.md), sections 2.3, 16, 17, 18 and 37.
- [S48] [Constitution: relationship to external archives](../constitution/external-archives.md).
- [S49] [Data model, section 2.14](../specs/data-model.md).
- [S50] [Identifiers, section 5](../specs/identifiers.md).
- [S51] [AGENTS.md](../../AGENTS.md), documentation and Markdown conventions.
- [S52] [Custodial independent projects research](../research/custodial-indie-projects.md), lesson 7 and case 3.13 (the Pew link-rot figure, [search] as cited there).
- [S53] [Legal landscape research](../research/legal-landscape.md), section 11 on licences, including the view that CC BY-NC is not an open licence [inference].
- [S54] [Project licensing proposal](project-licensing.md), issue #43.
