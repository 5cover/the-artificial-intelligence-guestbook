# The Artificial Intelligence Guestbook

## Concrete need

The Artificial Intelligence Guestbook provides a durable public place where anybody can record what it is like to live through the AI era.

A person should be able to arrive at the site, understand why the project exists, submit a testimony in their own words, optionally describe who they are, disclose whether and how AI helped produce their response, and later share a permanent link to that testimony.

Other visitors should be able to browse and search these testimonies directly rather than through an algorithmic recommendation system, including by fields such as profession, location, language, relationship to AI, and other voluntarily supplied metadata.

The project must preserve these testimonies over time, periodically package them into dated archival editions, and maintain enough contextual material that future readers can understand the world the contributors were describing.

The project is not intended to become a comprehensive encyclopedia of artificial intelligence. Where other projects already preserve models, technical development, benchmarks, source code, incidents, or other specialized material well, The Artificial Intelligence Guestbook should identify and reference them rather than duplicating their work.

The project is nevertheless not "build a website and finish." By its nature it creates an ongoing custodial responsibility. Someone must continue to moderate submissions, maintain the service, honor privacy requests, preserve the data, produce archival releases, keep essential references intelligible, and ensure the archive does not silently decay. This requirement is defined explicitly under Continuity.

## Status of this plan

This document defines what the MVP should accomplish and the important constraints under which it should operate.

It is not a complete implementation specification.

It deliberately does not choose an exact programming language, framework, database, hosting provider, search engine, repository layout, authentication provider, translation system, moderation architecture, or deployment topology.

The implementer may and should ask questions when implementation reveals an ambiguity, tradeoff, missing requirement, legal concern, security issue, or decision whose consequences are not adequately determined here.

Implementation choices should follow the purpose and constraints in this document rather than treating incidental examples as mandatory architecture.

## 1. Project purpose

The Artificial Intelligence Guestbook is a historical archive of the AI era centered on human experience.

Its primary subject is not artificial intelligence as a collection of technologies. Its primary subject is people living alongside those technologies.

The project should preserve:

- what people use AI for;
- what they refuse to use it for;
- what has changed in their work, education, creativity, relationships, habits, expectations, and culture;
- what they find useful, exciting, frightening, irritating, boring, absurd, overhyped, or underestimated;
- what they believe AI is becoming;
- what they expect their own future to look like;
- what they think contemporary society misunderstands;
- what ordinary details they suspect history might otherwise forget;
- predictions made before their outcome is known;
- disagreement between people occupying different places in the same historical period.

The project should preserve enthusiasm, hostility, indifference, uncertainty and contradiction without trying to reconcile them into a single account.

A testimony does not need to be insightful, representative, technically correct, or historically important according to the editors in order to have archival value.

"I barely use AI and don't care very much" can be as meaningful a record as an expert's long analysis.

## 2. The three layers

The project consists conceptually of three layers.

### 2.1 Testimonies

This is the primary layer.

It contains first-person contributions from people describing their relationship to AI and the world around it.

The MVP must make creating, publishing, finding and preserving these contributions possible.

### 2.2 Context

Context explains the world in which those testimonies were produced.

It may cover subjects such as:

- major AI products and companies;
- how ordinary people accessed AI;
- prevailing capabilities and limitations;
- employment and workplace use;
- education;
- creative industries;
- coding agents;
- companionship;
- misinformation and generated media;
- law and regulation;
- business adoption;
- social controversies;
- terminology and cultural phenomena;
- important public debates;
- public opinion;
- major events affecting how people understood AI.

This layer should be selective rather than encyclopedic.

Its test is:

> Does a future reader need this to understand the testimonies and the historical environment in which they were written?

The MVP does not require comprehensive coverage of these subjects.

### 2.3 References and evidence

The project should point readers toward specialist projects and primary sources that document technical or historical areas better than The Artificial Intelligence Guestbook reasonably could.

Examples may include model databases, model-preservation projects, benchmark archives, software archives, incident databases, annual AI reports, museums, research repositories, contemporary journalism and relevant public datasets.

Important external resources should be recorded deliberately rather than appearing only as fragile hyperlinks.

Where legally and practically appropriate, The Artificial Intelligence Guestbook may preserve snapshots, metadata or copies of especially important external material.

## 3. Who can contribute

The intended principle is:

> Anybody can express themselves.

The system should not restrict testimony to experts, AI users, particular professions, particular political positions, particular countries, or people who have strong opinions about AI.

The project should actively accommodate people who:

- use AI constantly;
- use it occasionally;
- refuse to use it;
- have barely encountered it;
- work on AI systems;
- have had their work changed by AI;
- believe AI is transformative;
- believe AI is overhyped;
- are unsure what to think.

Participation requirements related to law, abuse prevention, security or parental consent are operational constraints, not a change to this principle.

## 4. Contributor accounts and public identity

The MVP may require authentication before submission, principally for anti-abuse purposes and to make trivial mass submission more difficult.

OAuth is a reasonable candidate, but the exact authentication system is not prescribed by this plan.

Authentication should not imply public identity.

The system should distinguish:

1. private account identity;
2. optional public contributor information;
3. the testimony itself.

A contributor may authenticate using an identifiable account while publishing completely anonymously.

The application should retain only authentication information actually necessary for the service.

It should not automatically make OAuth names, photographs, email addresses or similar account information public.

Authentication is an anti-abuse mechanism, not a claim that one account equals one human being. Additional spam and abuse protections may still be necessary.

## 5. Public identity fields

At the end of the contribution form, contributors should be able to provide optional information about themselves.

Possible fields include:

- display name;
- age or age range;
- country;
- region;
- language;
- profession or field;
- organization or type of organization;
- relationship to AI;
- personal website or other public link.

These fields should be optional unless a particular field is legally or operationally necessary.

A contributor should be able to publish:

- with a real identity;
- with a pseudonym;
- anonymously.

Public identity should be clearly separated from private account information.

The MVP need not support an elaborate profile system.

The testimony is the primary object, not the contributor profile.

## 6. Submission format

The form should combine free expression with optional structure.

The application should not feel primarily like a survey.

A contributor should be given a large free-text area with an invitation similar in spirit to:

> What is it like to live with AI right now?

The contributor may write a few sentences or a long response.

The interface may offer optional prompts such as:

- What role does AI currently have in your life?
- What do you use it for?
- What do you avoid using it for?
- Has it affected your work or studies?
- Has it affected your hobbies or creative work?
- What excites you about it?
- What worries or frustrates you?
- What seems overhyped?
- What seems underestimated?
- What do people around you think?
- What do you expect in the next few years?
- What do you expect in the longer term?
- What prediction would you like to leave on record?
- What ordinary detail about this period might future historians overlook?
- What would you like somebody reading this many decades from now to understand?

These prompts are aids, not mandatory questions.

The system may also collect structured fields useful for later browsing and research, such as frequency of AI use, occupation category, broad sentiment, technologies used, and predictions.

The structured fields should not replace the contributor's own words.

## 7. AI authorship disclosure

The project does not require testimony to be written without AI.

Fully AI-generated testimony is permitted if its provenance is disclosed.

The project is interested in how people choose to communicate during the AI era, including their use of AI to communicate about AI.

Each submission should therefore record an authorship declaration.

At minimum, contributors should be able to indicate something equivalent to:

- no AI used;
- AI used for proofreading or translation;
- AI used to organize or develop the response;
- AI substantially generated the response;
- response fully generated by AI;
- prefer not to characterize it.

Where AI was used, contributors should be able to optionally provide:

- model or product;
- model version when known;
- mode or reasoning/effort setting when relevant;
- prompts or workflow;
- what the person changed afterward;
- any other comments about AI involvement.

These declarations should be visible with the published testimony.

The archive should not silently classify or guess whether a response was AI-generated.

## 8. Languages and localization

Multilingual support is a first-class property of the project, not a later enhancement.

The MVP interface must support at least:

- English;
- French.

All major contributor-facing flows should be localized, including:

- project explanation;
- submission form;
- consent information;
- moderation status;
- privacy controls;
- browsing and filtering;
- deletion or withdrawal requests;
- relevant emails or notifications.

Contributors should be allowed to submit testimony in other languages as well.

The original language version is canonical.

A translation must never silently replace the original.

Machine-generated translations may eventually be provided, but they should be clearly labeled as such.

Because translation can materially alter testimony, the project should not assume an AI translation is authoritative merely because it is fluent.

English and French translations can initially receive greater editorial attention because their quality can be independently evaluated by the maintainer.

Crowdsourced or contributor-supplied translations may be considered later.

## 9. Publication and moderation

User-generated content is real public content.

Submissions should not automatically become public.

The MVP should support a light pre-publication moderation workflow.

Moderation exists to address matters such as:

- spam;
- automated flooding;
- illegal material;
- threats;
- harassment;
- content that creates serious privacy problems for another person;
- accidental publication of secrets or credentials;
- obviously malicious use of the platform;
- content that violates the project's narrow publishing rules.

Moderation should not become ideological or editorial gatekeeping.

A testimony should not be rejected because the moderator disagrees with it, thinks it is poorly argued, considers its prediction foolish, or believes its view of AI is factually mistaken.

The archive is partly valuable because people disagree and are sometimes wrong.

The original submitted content should be distinguished internally from any moderated public representation if moderation ever requires redaction.

The exact moderation policy and tooling require further design.

For the MVP, the project may be moderated entirely by its founder.

## 10. Sensitive and personal information

The platform should behave like a deliberate public publishing system.

Before submission, contributors must be clearly informed that their testimony is intended for public access and historical preservation.

They should be warned:

- not to publish information about themselves that they do not want made public;
- not to reveal private or sensitive information about identifiable third parties;
- that their own voluntary self-disclosure may become part of a public historical archive.

The project should not attempt to prohibit every possible form of sensitive self-expression.

Someone discussing their own health, beliefs, disability, sexuality, employment difficulties or other personal experiences may be expressing something directly relevant to their testimony.

The consent and publication process must therefore be designed appropriately for voluntary public self-disclosure.

Disclosure of personal information about other people is a separate moderation concern.

The exact legal basis, consent language and treatment of special-category data must receive proper GDPR review before public launch.

## 11. Children and parental consent

The project's principle remains that young people should be able to contribute rather than being excluded solely because their perspective creates additional implementation work.

The MVP must therefore account for age and parental-consent requirements.

For contributors who can legally consent for themselves, the normal contribution flow applies.

Where parental or guardian authorization is legally required, the application should provide a separate flow for obtaining it.

The interface should not merely pretend this problem does not exist.

The exact age thresholds and verification mechanism should be determined according to applicable law and the contributor's circumstances.

For example, a French contributor who can independently consent under French rules should not unnecessarily be forced through the same process as somebody below that threshold.

The precise legal and technical mechanism remains an implementation question requiring validation.

## 12. Every testimony is independently addressable

Every published testimony must have a stable identifier and a permanent deep link.

Example conceptually:

```text
/testimonies/7q4km2xd
```

The exact URL convention is not prescribed.

A testimony page should show:

- testimony text;
- date of submission or publication as appropriate;
- original language;
- optional public identity information;
- relevant structured metadata;
- AI-authorship disclosure;
- translations, clearly identified;
- a stable way to quote or link to the testimony.

A person should be able to cite one contribution without linking to an unstable search page.

Stable internal IDs should survive redesigns of the website.

## 13. Browsing

Visitors should be able to deliberately explore the archive.

The MVP should support:

- chronological browsing;
- basic text search;
- filtering.

Useful filters may include:

- language;
- country;
- region where appropriate;
- profession or field;
- relationship to AI;
- frequency of AI use;
- AI tools used;
- broad self-described attitude;
- AI-authorship category;
- year or archival edition.

Only sufficiently populated and useful filters need to appear initially.

The system should avoid presenting very granular combinations that unnecessarily make anonymous contributors identifiable.

There is no recommendation algorithm.

There is no personalized feed.

There is no engagement ranking.

There is no "people like you also liked."

The user chooses what to look for.

## 14. Quoting and sharing

The MVP should make individual testimony easy to reference.

Users should be able to:

- link to an entire testimony;
- copy a canonical URL;
- quote text with attribution appropriate to the contributor's chosen public identity.

More elaborate quote-fragment deep linking may be implemented if useful but is not required for the earliest version.

Sharing features should not turn the archive into a social platform.

## 15. No social network

The MVP explicitly excludes:

- comments;
- replies;
- likes;
- follower systems;
- private messaging;
- engagement scores;
- reputation systems;
- personalized timelines;
- recommendation feeds;
- public argument threads.

The Artificial Intelligence Guestbook is an archive people contribute to, not a social network.

A testimony may respond intellectually to another testimony, but the platform does not need to build a conversational graph around that interaction.

## 16. Contextual material

The MVP should contain enough editorial content for a visitor to understand what the project is documenting.

It does not need a complete encyclopedia.

Initial contextual material could include:

- an explanation of what "AI" generally means in the archive;
- a concise overview of how people are encountering AI;
- important contemporary systems and interfaces;
- major societal controversies;
- effects on work, education and creative activity;
- important vocabulary;
- a concise chronology;
- links to specialist archives and research projects.

The contextual layer may grow substantially over time.

The key editorial rule is that The Artificial Intelligence Guestbook should not reproduce specialist work merely because it exists.

For example, if another project maintains a serious historical database of AI models, The Artificial Intelligence Guestbook can explain why it matters, record the relevant resource and direct readers to it rather than creating a competing model database.

## 17. Societal history remains in scope

Delegating technical preservation does not mean delegating the entire historical record.

Existing preservation projects tend to have strong coverage of areas such as:

- models;
- benchmarks;
- research papers;
- source code;
- technical artifacts;
- incidents;
- institutional reporting.

The Artificial Intelligence Guestbook should remain willing to document social dimensions where external preservation is weaker, especially when they contextualize testimony.

This can include:

- cultural discourse;
- labor conflict;
- educational changes;
- creative controversies;
- enterprise adoption;
- public expectations;
- AI companionship;
- attitudes toward automation;
- changing language;
- media narratives;
- policy disputes;
- hype and backlash;
- scams and generated content;
- ordinary uses;
- regional differences.

The archive should periodically reassess what other projects preserve well and where genuine gaps remain.

## 18. Reference shelf

The project should maintain a curated catalogue of external archives and resources that complement it.

For each important dependency, record enough information to establish what the resource was and why it mattered.

A reference record may contain:

```yaml
id: epoch-ai-models
name: Epoch AI Models
role: Database of historically significant AI models
homepage: ...
resource_url: ...
description: ...
accessed_or_verified: ...
local_snapshot: ...
license: ...
notes: ...
```

Not every referenced site needs to be copied.

Where preservation is legal, useful and proportionate, important static resources or datasets may be included in archival releases.

Where redistribution is inappropriate, sufficient metadata should still be retained so future readers can identify the external work.

## 19. Annual archival editions

The live website is a continuously growing collection.

Annual editions are snapshots of that living archive.

There is no annual submission deadline in the sense of closing participation.

Instead, an edition includes whatever eligible material has entered the archive by its cutoff.

The intended first major edition uses a cutoff of December 31, 2027.

A submission received afterward remains entirely valid and becomes part of a subsequent archival period.

Each edition should eventually package:

- testimonies;
- public metadata;
- translations intended for archival publication;
- contextual material;
- reference records;
- relevant primary artifacts;
- provenance information;
- documentation explaining the archive;
- the data structures necessary to interpret the collection.

An edition should be independently intelligible rather than requiring the future live website to continue functioning.

## 20. Archive downloads

A major long-term objective is to allow people and institutions to download and preserve copies of the archive.

This is desirable because a historical archive should not depend entirely on one server, company or maintainer.

However, testimony can contain personal data.

The archive therefore cannot treat an old release as absolutely immutable in the face of valid privacy obligations.

The archive model should support privacy revisions.

For example:

```text
2027.0
2027.1
2027.2
```

A later revision may expunge withdrawn testimony while preserving the fact that an archival object once existed through a non-personal tombstone where appropriate.

The project should maintain a machine-readable withdrawal or invalidation mechanism so operators of mirrors and existing archive copies can determine whether material has subsequently been withdrawn.

The exact format remains to be designed.

The project must not promise that it can remotely destroy independent copies previously downloaded by unrelated third parties.

It should instead make the limits of redistribution and later deletion clear to contributors and archive users, and implement the obligations that apply to copies under its control.

This entire mechanism requires legal validation before public downloadable personal-data archives are launched.

## 21. GDPR and privacy rights

Because the project is operated from France and intentionally handles public testimony, GDPR compliance is a core product requirement.

It is not a footer or a later legal task.

The system must be designed to support applicable rights, including mechanisms for contributors to request access, correction where appropriate, withdrawal and deletion.

Deletion needs to propagate through systems controlled by the project, which can include:

- live testimony pages;
- databases;
- search indexes;
- generated translations;
- cached representations;
- internal moderation interfaces;
- generated site files;
- downloadable releases controlled by the project;
- backups according to an appropriate deletion lifecycle.

The data model should make this possible without manual archaeology across unrelated systems.

Privacy requirements also affect:

- authentication;
- logs;
- analytics;
- backups;
- moderation;
- localization;
- archive generation;
- external mirrors;
- data exports;
- contributor communications.

A privacy and GDPR review is therefore a release requirement, not an optional future improvement.

## 22. Withdrawal and deletion

A contributor must have a practical way to request removal of their testimony.

The project should retain whatever minimum private linkage is necessary to authenticate or appropriately validate such requests.

When content is removed:

- the public testimony disappears;
- copies under project control are addressed through the defined deletion process;
- future archival packages exclude it;
- prior project-hosted packages are superseded or revised where required;
- the archive may retain a content-free tombstone or identifier if legally appropriate and useful for historical consistency.

A tombstone must not itself retain the personal information that was supposed to be deleted.

The exact retention of operational records related to deletion requests should follow legal requirements.

## 23. Portability of the archive

The project should not make the website database the only meaningful form of the collection.

Over time, the archive should be exportable into understandable, relatively simple formats.

Likely examples include:

- structured JSON or similar machine-readable records;
- plain text or Markdown;
- media files;
- manifests;
- static HTML;
- checksums;
- documentation describing the schema.

The exact formats are not fixed by the MVP plan.

The important requirement is that the archive can eventually survive the application.

A future custodian should not need to resurrect the original production stack merely to understand the testimonies.

## 24. Administration

The founder needs a small operational interface or equivalent tooling.

The MVP administration capability should make it possible to:

- review pending submissions;
- publish or reject submissions;
- record moderation notes;
- remove or redact content when legitimately necessary;
- process privacy requests;
- manage translations;
- manage contextual pages;
- inspect basic submission metadata;
- prevent or restrict abusive accounts;
- export archive data;
- identify operational failures requiring attention.

The admin system does not need to resemble a large commercial CMS.

It needs to make routine stewardship safe and manageable for one person.

## 25. Anti-abuse

Because anybody can contribute, abuse should be assumed.

The system should be able to defend against:

- mass spam;
- automated submissions;
- repeated reposting;
- account creation abuse;
- malicious links;
- attempts to overwhelm moderation;
- denial-of-service patterns;
- publication of secrets or credentials;
- attempts to use testimony pages primarily for SEO or advertising.

Authentication is one layer, not the entire solution.

Rate limiting, moderation queues, spam detection and other safeguards may be used.

Anti-abuse systems should not require invasive tracking where less intrusive methods suffice.

## 26. Security

Security is particularly important because the system holds:

- unpublished testimony;
- authentication identifiers;
- moderation records;
- privacy requests;
- possibly contributor contact information;
- potentially sensitive public writing prior to publication.

The implementation should minimize collection of private information and minimize the number of systems containing it.

Administrative access must be protected appropriately.

Secrets and authentication credentials must not enter archival exports.

Security decisions belong to implementation design, but the requirement to treat unpublished and private operational data carefully is part of the MVP.

## 27. Accessibility

People should not need specialized technical ability to contribute or read.

The MVP should follow ordinary web accessibility practices, including:

- keyboard usability;
- sensible semantic structure;
- readable typography;
- adequate contrast;
- screen-reader compatibility;
- accessible forms and validation;
- language metadata;
- usable interfaces without complex animations or interaction patterns.

Accessibility matters especially because the archive is explicitly intended to represent more than a narrow technical subculture.

## 28. Continuity

The Artificial Intelligence Guestbook creates an ongoing custodial obligation.

This must be acknowledged explicitly.

Launching the website means accepting responsibility for tending the archive.

At the beginning, that custodian is the founder.

Routine continuity work includes at least:

- reviewing the moderation queue;
- responding to legitimate privacy and deletion requests;
- dealing with spam and abuse;
- monitoring whether submissions are still functioning;
- maintaining authentication and security;
- keeping dependencies and hosting operational;
- maintaining backups;
- checking that archive exports remain recoverable;
- reviewing important external references for disappearance or material changes;
- maintaining English and French interface text;
- dealing with problematic translations;
- periodically updating contextual material;
- producing annual archival editions;
- documenting corrections and withdrawals;
- ensuring published archive formats remain understandable;
- keeping basic project documentation current.

The project should be designed so this work remains feasible for one person at modest scale.

Automation is encouraged where it reduces repetitive maintenance, but automation does not eliminate custody.

The MVP should avoid creating features that substantially increase permanent operational burden without advancing the archival mission.

This is another reason to exclude comments, private messaging, recommendation systems, elaborate profiles and social-network mechanics.

## 29. Continuity beyond the founder

The MVP does not require an organization, foundation, association or editorial team.

The founder may initially operate the entire project.

However, the project should be documented sufficiently that another technically competent person could understand:

- what the archive is;
- where its data lives;
- how archival editions are produced;
- how deletion works;
- what operational services it depends on;
- what recurring responsibilities exist;
- how to restore it from backups.

Important knowledge should not exist solely in the founder's memory.

If the project gains traction, later continuity mechanisms may include:

- additional maintainers;
- moderators;
- an association or other legal structure;
- institutional archival partners;
- library or university partnerships;
- independent mirrors;
- succession arrangements.

These are not MVP requirements.

Preparing the project so such transitions are possible is.

## 30. Backups and recovery

The MVP must have a real backup strategy.

"At least the hosting provider probably has backups" is insufficient for an archival project.

The system should maintain recoverable copies of important data separately enough that a single operational failure does not destroy the archive.

Recovery should eventually be tested rather than assumed.

Backups containing personal data remain subject to the project's privacy and deletion design.

The exact storage architecture is an implementation decision.

## 31. Observability without surveillance

The maintainer needs enough operational information to know whether the site works.

Useful measurements may include:

- submission failures;
- moderation backlog;
- abuse rates;
- search failures;
- server errors;
- archival export failures;
- localization problems.

The project does not require invasive behavioral analytics.

Metrics should be collected because they support operation of the archive, not because every visitor action can be monetized or optimized.

## 32. MVP public pages

At minimum, the public application should provide the equivalent of:

### Home

Explains the idea clearly and offers immediate paths to:

- leave a testimony;
- browse testimonies;
- understand the project;
- explore context.

### Contribute

The testimony form and publication/consent flow.

### Testimonies

Browsable and searchable collection.

### Individual testimony

Permanent deep-linked representation of one contribution.

### About

Mission, methodology, who operates the project, what gets preserved, why human testimony matters.

### Context

A modest collection of explanatory material and reference resources.

### Privacy

Clear explanation of data handling and contributor rights.

### Archive

Initially this may simply explain the annual archival model. Downloadable editions can appear when appropriate.

The exact information architecture may differ.

## 33. Internal objects the application should understand

The implementation does not need a complex research graph for the MVP.

It does need clear conceptual objects.

At minimum these probably include:

```text
Contributor account
Testimony
Public contributor metadata
Authorship disclosure
Translation
Moderation record
Withdrawal/deletion record
Context document
External reference
Archival edition
```

A testimony should have a stable internal ID independent of its current publication state or URL.

Likely testimony states include something like:

```text
draft
submitted
under_review
published
rejected
withdrawn
```

The exact schema is an implementation decision.

## 34. What is explicitly not required for the MVP

The MVP does not require:

- a comprehensive AI encyclopedia;
- a complete history of AI;
- a model database;
- benchmark tracking infrastructure;
- preservation of every AI model;
- a full research knowledge graph;
- autonomous research agents;
- sophisticated recommendation systems;
- comments;
- likes;
- messaging;
- profiles resembling social-network accounts;
- follower relationships;
- contributor reputation;
- mobile applications;
- elaborate visualization systems;
- perfect automated translation;
- every possible filter;
- an advanced editorial CMS;
- a finalized permanent technical architecture;
- large-scale organizational governance.

Some of these may eventually become useful.

They are not prerequisites for proving the project.

## 35. MVP success condition

The MVP is successful when a stranger can:

1. arrive without prior knowledge of the project;
2. understand what The Artificial Intelligence Guestbook is trying to preserve;
3. submit a testimony in a supported, understandable flow;
4. choose how much or how little public identity to attach;
5. disclose how AI was involved in producing the testimony;
6. understand that publication is public and archival;
7. have the submission pass through moderation;
8. receive a stable public deep link once published;
9. browse other people's testimonies;
10. search and filter them according to personally relevant dimensions;
11. read the site in English or French;
12. understand enough contextual information to orient themselves.

And the maintainer can:

 1. moderate submissions;
 2. handle spam and abuse;
 3. process privacy and deletion requests;
 4. administer translations and public content;
 5. export the archive in a usable form;
 6. back it up and recover it;
 7. understand what operational work must continue;
 8. eventually turn the living collection into a dated archival edition.

If those things work, The Artificial Intelligence Guestbook exists.

It does not need hundreds of contextual articles or thousands of testimonies before it is a real archive.

## 36. Suggested implementation sequence

### Phase A: Constitution

Before substantial application development, establish short authoritative documents defining:

- mission;
- editorial principles;
- moderation principles;
- privacy assumptions;
- authorship disclosure;
- annual archival model;
- deletion philosophy;
- multilingual principles;
- relationship to external archives;
- continuity expectations.

These documents prevent implementation decisions from quietly redefining the project.

### Phase B: Data and privacy design

Define:

- testimony representation;
- public versus private identity;
- authorship metadata;
- translation relationship;
- moderation states;
- deletion and withdrawal lifecycle;
- age/parental-consent handling;
- archive export requirements;
- minimum authentication data;
- backup/deletion interaction.

Obtain appropriate privacy/GDPR review before launching public collection.

### Phase C: Small end-to-end application

Build the smallest complete path:

```text
Visitor
  ↓
Understands project
  ↓
Authenticates
  ↓
Writes testimony
  ↓
Chooses public metadata
  ↓
Declares AI involvement
  ↓
Accepts publication terms
  ↓
Submission enters moderation
  ↓
Maintainer reviews
  ↓
Published
  ↓
Permanent testimony URL
```

At this stage, correctness of the complete lifecycle matters more than visual sophistication.

### Phase D: Browsing and localization

Add:

- testimony index;
- search;
- filters;
- English interface;
- French interface;
- language handling;
- canonical/original-language presentation.

### Phase E: Operational completeness

Before meaningful promotion, ensure:

- deletion works;
- moderation is manageable;
- abuse controls exist;
- backups exist;
- recovery is possible;
- privacy documentation exists;
- important operational actions are documented.

### Phase F: Context and reference shelf

Add enough contextual material for the archive to make sense and establish the project's curated links to complementary preservation initiatives.

Do not wait for this section to become encyclopedic before accepting testimony.

### Phase G: First archival pipeline

Before the first annual cutoff, prove that the live collection can actually be transformed into a self-contained archival package.

Do at least one rehearsal archive before the real annual edition.

The first major edition should package eligible material through December 31, 2027.

## 37. Product principle for future decisions

When considering a new feature, ask:

> Does this make it easier to preserve, understand, discover or responsibly maintain human testimony about living through the AI era?

If yes, it may belong.

If its main effect is to make The Artificial Intelligence Guestbook behave more like a social network, general-purpose encyclopedia, technology-news site, engagement platform or comprehensive AI database, it should face a much higher bar.

The project's scarce resource is not storage.

It is custodial attention.

Features should be judged partly by the permanent maintenance obligation they create.

## 38. Naming

The project should be publicly named:

> The Artificial Intelligence Guestbook

The name is intentionally somewhat playful without making the project unserious.

"Artificial Intelligence" states the subject explicitly. This is preferable to relying solely on the abbreviation "AI": it is unambiguous, descriptive outside the immediate context of the project, and sufficiently specific to help the project be identifiable and discoverable through search.

"The AI Guestbook" may be used for concision in technical identifiers and documentation. That shortened should also eventually appear on the site for searchability. SEO is an explicit goal to prepare early rather than retrofit later

"Guestbook" describes the relationship the project wants to establish with contributors.

A guestbook does not demand expertise, completeness or representativeness. It asks people who were present to leave something behind.

The implicit invitation is:

> You were here. Leave a record.

This closely matches the purpose of the project. Contributors are not primarily research subjects, survey respondents or commentators expected to produce authoritative analyses. They are people living through a historical period and leaving accounts of what that period looks like from where they stand.

The guestbook metaphor also accommodates differences in the scale and character of contributions. A short observation, a detailed essay, uncertainty, indifference, enthusiasm, fear and an incorrect prediction can all legitimately be entries in the same guestbook.

### Public terminology

The naming should influence the language of the interface.

Prefer ordinary terms such as:

- sign the guestbook;
- write an entry;
- read the guestbook;
- browse entries;
- your entry;
- anonymous entry;
- previous entries.

The project may use more precise terms such as "testimony," "contemporary testimony," "contributor," "archival record," and "corpus" in its methodology, documentation and internal implementation.

These terms should not unnecessarily make the public interface feel academic or bureaucratic.

An individual public contribution is therefore normally an "entry" in the interface, even when the same object is understood as testimony for archival and research purposes.

### Subtitle

The title does not need to communicate the complete philosophy of the project by itself.

A subtitle should explain its human and archival purpose.

The preferred working subtitle is:

> A human time capsule of the AI era.

Together:

> The Artificial Intelligence Guestbook  
> A human time capsule of the AI era.

Alternative explanatory phrases may be used in particular contexts, such as:

> What it was like to live through AI.

or:

> Tell the future what it's like from where you are.

The title should remain stable even if explanatory copy changes.

### The guestbook and the time capsule

The two metaphors describe different aspects of the project and should coexist.

The guestbook is the living collection.

It remains open. People arrive, leave entries, and read what others have written.

A time capsule is a preserved historical edition of that guestbook and its surrounding context.

The relationship can be explained simply:

> The guestbook stays open. At the end of each year, we preserve a time capsule of what people had written and of the world they were writing about.

This gives the project a natural vocabulary:

```text
The Artificial Intelligence Guestbook
    |
    +-- Guestbook       living collection
    |
    +-- Entry           individual contribution
    |
    +-- Time Capsule    preserved annual edition
    |
    +-- Context         material explaining the period
    |
    +-- Reference Shelf external archives and resources
```

The terminology is conceptual rather than a required website navigation structure.

### Historical and methodological meaning

The more serious intellectual basis of the project should be explained on the About or methodology pages rather than forced into its name.

One useful concept is the German term "Zeitzeugnis": broadly, a testimony or document that bears witness to its own time. Related concepts such as "Zeitzeuge," a contemporary witness, help describe why these entries are historically interesting.

The important property of an entry is not simply that somebody remembers an event.

The contributor writes while the future is still unknown.

Their expectations have not yet been corrected by hindsight. Their fears may never materialize. Their confident predictions may prove absurd. Things they consider revolutionary may become mundane, while details they barely mention may later appear historically decisive.

The project deliberately preserves that epistemic position.

The About page should explain this idea in accessible language and may introduce terms such as Zeitzeugnis as useful conceptual precedents. Knowledge of those terms should never be necessary to understand or participate in the project.

### Naming should guide product design

"Guestbook" should function as more than branding.

When evaluating product decisions, the implementer can ask whether the resulting experience still behaves like a guestbook.

A guestbook naturally supports writing, reading, browsing, returning and leaving another entry.

It does not naturally require likes, followers, engagement rankings, recommendation feeds, reputation scores or discussion threads.

This reinforces the project's existing decision not to become a social network.

Likewise, the metaphor argues against making contribution feel like completing a research questionnaire. Structured metadata can support preservation and discovery, but the central interaction should remain:

> Leave an entry.

The name therefore acts as a useful product constraint as well as a public identity.

## 39. The MVP in one sentence

Build a multilingual, searchable, responsibly moderated public archive where anyone can leave a permanently addressable testimony about living through the AI era, with transparent authorship and optional identity, backed by enough context to make those testimonies understandable and by enough operational and archival infrastructure to ensure somebody can continue taking care of them.
