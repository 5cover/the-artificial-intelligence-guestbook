# Stack RFP: choosing the application framework for The Artificial Intelligence Guestbook

Status: Proposal - awaiting owner decision (criteria revised 2026-11-15, section 4.3)

Date: 2026-11-15

Issues: #6 (stack RFP) and #7 (application stack decision)

Related: [plan](../plans/main.md), [ADR 0002](../decisions/0002-single-eu-vps.md), [ADR 0003](../decisions/0003-email-magic-link-auth.md), [ADR 0006](../decisions/0006-archive-first-replaceable-application.md), [ADR 0007](../decisions/0007-privacy-review-path.md)

Source tags such as [S12] refer to the numbered list in the Sources section. Anything not verified in this pass is labelled "not verified". Scores are judgements, not measurements.

## 1. Summary

The owner asked for a comparison of application stacks, not a build. Fourteen options are scored on the same scale:

- eleven real candidates, plus a minimal TypeScript assembly evaluated on the owner's request;
- the bare-runtime extreme (Node.js with no framework);
- a deliberately terrible reference stack that marks the floor of the scale.

The criteria were revised on 2026-11-15 after owner review (section 4.3): pass/fail gates were added, the upgrade criterion was redefined as the cost of staying supported, a type-system criterion was added, and the weights were rebalanced. The short version:

- **Gates come first** (section 4.1): erasure, lossless export, EU processing, a no-JavaScript core and a supported release line. Vercel fails the EU-processing gate, so Next.js is scored self-hosted only.
- **Django** (Python, with PostgreSQL 18) leads with 86.4. Its strengths are a first-party admin, gettext-based i18n, PostgreSQL full-text search with French and English configurations, foundation governance and a verified security policy. Its gaps: no first-party magic-link flow, no production worker for its new Tasks framework, no first-party rate limiter, and the weakest static typing of the leading group.
- **Symfony 7.4 LTS** (PHP) is second with 77.4. It has the longest verified LTS window, a first-party login-link feature, XLIFF and ICU translations and a database-backed job transport, but no first-party admin.
- **ASP.NET Core** (70.0), **Go** (69.0) and **minimal TypeScript** (68.8) are in a near-tie for third place. Minimal TypeScript means Node.js with TypeScript source and maintained libraries for every security or standards concern (section 6.13). It is the best typed and the best archive fit, but hand-builds its admin and depends on several single-maintainer libraries.
- **Bare Node.js** (65.6) is sixth, above every TypeScript framework. But it would hand-write all its security plumbing, so it is not recommended in its pure form (section 6.12). Minimal TypeScript is its practical form.
- **SvelteKit** (62.4) is the strongest TypeScript framework. **WordPress** (54.8) and **Next.js self-hosted** (52.8) are at the bottom of the real candidates. Each excels at jobs this project does not have: content editing for WordPress, interactive client applications for Next.js.
- **Churn does not decide the ranking.** Setting the cost-of-staying-supported weight to zero leaves the top three unchanged (section 7.2). Low scores for popular frameworks come from how little they provide first-party for a single custodian, not from their release cadence (section 7.3).
- **Architecture is largely independent of the winner.** ADR 0006 makes the archive format the primary artefact, so the framework choice is less consequential than usual. This document recommends writing the archive specification (issue #13) before the application scaffold.

## 2. Context and decided constraints

These are owner decisions already recorded in the repository or stated for this RFP. They are not reopened here.

- The archive is the primary deliverable. The web application is replaceable. The canonical archive format (structured records, plain text, manifests, checksums, schema documentation) is specified independently of the app. The app database is an operational store that exports to that format ([ADR 0006](../decisions/0006-archive-first-replaceable-application.md), [plan section 23](../plans/main.md)).
- Lessons from a "static public site plus small API" design may be borrowed (for example cacheable, pre-rendered HTML for published testimonies and static HTML in editions) without adopting that architecture ([ADR 0006](../decisions/0006-archive-first-replaceable-application.md)).
- Hosting: one self-managed EU VPS (Hetzner, OVHcloud, Scaleway class). The stack must run comfortably on a small VPS with modest memory ([ADR 0002](../decisions/0002-single-eu-vps.md)).
- Authentication: email magic links only, no passwords and no OAuth for now. Defences in layers: disposable-email blocklist, MX check, per-account pending caps, global intake throttling, a self-hosted proof-of-work challenge, rate limits, and rel="ugc nofollow" on outbound links ([ADR 0003](../decisions/0003-email-magic-link-auth.md)).
- Database: PostgreSQL is the presumptive choice for full-text search in French and English. A challenge to it is required (section 6).
- One operator, for decades. Successor-friendliness, low dependency churn and low supply-chain surface matter ([plan section 28 and 29](../plans/main.md)).
- Server-rendered, accessible HTML that works without JavaScript is preferred. French and English are first-class interface languages, and testimonies may be in any language ([plan sections 8 and 27](../plans/main.md)).
- The owner is comfortable with TypeScript and values its type system for expressing complex data models (criterion 15). Local tooling is not a constraint: the owner can install whatever is needed and can develop on other machines, so missing tools are an immediate setup step, not a risk (owner clarification, 2026-11-15).

## 3. Requirements derived from the plan

Each requirement is a condition the stack must satisfy or make practical. "Must" items are used for the scoring; the list is not exhaustive.

- R1. Canonical archive export that is lossless and independent of the app, including a round-trip validation test ([ADR 0006](../decisions/0006-archive-first-replaceable-application.md); plan sections 19, 23; [archival model](../constitution/archival-model.md)).
- R2. Stable testimony identifiers independent of state, URL and database keys; identifiers never reused (plan sections 12, 33; [domain research](../research/domain-and-persistence.md)).
- R3. Testimony states draft, submitted, under_review, published, rejected, withdrawn, with a content-free tombstone after withdrawal (plan sections 22, 33).
- R4. Pre-publication moderation queue; nothing auto-publishes; original submission kept separately from any moderated public representation (plan section 9; ADR 0003 point 2).
- R5. Authorship disclosure fields stored and shown with the testimony (plan section 7).
- R6. Optional public identity separated from the private account; no automatic publication of account data (plan sections 4, 5).
- R7. Magic-link sign-in with single-use, short-lived tokens; sessions; CSRF protection; rate limiting (plan section 25; ADR 0003).
- R8. Disposable-domain blocklist, MX validation, per-account pending caps, global throttling and bulk rejection in the admin (ADR 0003).
- R9. Self-hosted proof-of-work challenge at sign-up and submission, without third-party tracking (ADR 0003; plan section 25).
- R10. One-person admin: queue, moderation notes, redaction, privacy requests, translations, context pages, account suspension, export, operational health (plan section 24).
- R11. Deletion propagates to database, search index, caches, generated translations, generated files, and downloadable releases under project control; backups follow a defined expiry (plan sections 21, 22).
- R12. Chronological browsing, basic full-text search in French and English, filters by language, country, profession, relationship to AI and similar fields (plan section 13).
- R13. Full UI in French and English, including emails and consent text; testimonies in any language with the original canonical; machine translations labelled (plan sections 8, 10).
- R14. Server-rendered pages that work without JavaScript; semantic HTML, lang attributes, accessible forms and validation (plan section 27).
- R15. Permanent, short, opaque testimony URLs; published pages renderable as static HTML for cache and editions (plan section 12; ADR 0006).
- R16. Separate guardian-consent flow for minors (plan section 11).
- R17. Scheduled jobs for email sending, exports, backups, expiry of tokens and rate-limit data, without extra infrastructure beyond the VPS (plan sections 19, 30).
- R18. Real, tested backups and recovery; restore drills runnable by a successor (plan sections 29, 30).
- R19. Observability without behavioural tracking: submission failures, backlog, abuse rates, search failures, export failures (plan section 31).
- R20. Security: minimal collection, secrets never in exports, protected admin access, dependency updates feasible for one person (plan sections 26, 28).
- R21. Editable context and reference-shelf records with translations, exportable with the archive (plan sections 16, 18, 24).
- R22. Documentation a competent successor can follow: where data lives, how editions are built, how deletion works, how to restore (plan section 29).

## 4. Gates, criteria and weights

### 4.1 Gates

A weighted sum is compensatory: strength on one criterion pays for weakness on another. Some failures cannot be paid for. A stack scoring 5 everywhere except erasure would score about 95 while being unlawful to operate. The requirements below are therefore pass/fail and are checked before scoring. They apply to every candidate, and to anything added around the application later, such as a CDN, a translation service or a search engine.

| Gate | Requirement | Source |
| --- | --- | --- |
| G1 Erasure | Any personal data held anywhere in the system can be deleted within the defined lifecycle, backups and storage-level remnants included. | [Deletion philosophy](../constitution/deletion-philosophy.md); plan sections 21, 22 |
| G2 Lossless export | All archival data can be exported to the open, documented archive format without the vendor's cooperation. | ADR 0006; plan section 23 |
| G3 EU processing | Personal data is processed and stored by EU-controlled infrastructure under processor agreements. | ADR 0002; [privacy assumption](../constitution/privacy-assumptions.md) 11; [legal research](../research/legal-landscape.md), section 9 |
| G4 No-JS core | Reading testimonies and contributing work without client-side JavaScript. | Plan section 27; editorial principles |
| G5 Supported line | A released, supported version line with a published security process and a known end-of-support date. Abandoned software fails here. | Plan sections 26, 28 |

Results (judgement, not verified per candidate):

- The framework candidates in section 6 pass, including Next.js when self-hosted.
- Next.js on Vercel fails G3 (section 6.11).
- WordPress passes G1 to G3 with care: erasure must reach post revisions, metadata and plugin tables. It is conditional on G4, because contributors must use a custom no-JavaScript front-end form, never the block editor. It is also conditional on G5, because only the latest release is supported and plugins carry no support commitment.
- Bare Node.js is conditional on G5, because `node:sqlite` is still a release candidate (section 6.12).
- Minimal TypeScript is conditional on G5, because five of its key libraries publish no security policy (section 6.13).
- The reference anti-stack fails all five (section 6.14). It is scored only to mark the floor.

### 4.2 Criteria and weights

Weights sum to 100. Each criterion is scored 1 to 5 (5 is best) in section 7. A score of 1 on every criterion gives 20, the floor of the scale.

| # | Criterion | Weight | Original | Why this weight |
| --- | --- | --- | --- | --- |
| 1 | Longevity and governance: who controls the project, how it is funded, whether it is actively maintained and improving, and whether it will plausibly exist and be supported in 10 to 20 years | 10 | 11 | The plan is for decades, and a successor must inherit the stack ([plan 28, 29](../plans/main.md)). Active improvement is credited here. Support-window length moved to criterion 2. |
| 2 | Cost of staying supported: expected effort per year to remain on a supported, patched version. This covers the length of support windows, the size and frequency of breaking changes, the deprecation policy and migration tooling. It measures cost, not activity. | 7 | 9 | Redefined (section 4.3). Breaking change consumes custodial attention ([plan 28](../plans/main.md)). Updates themselves are not penalized. |
| 3 | Built-in or first-party admin for one-person moderation | 8 | 8 | Moderation, redaction, privacy requests and translations are routine duties ([plan 24](../plans/main.md)). |
| 4 | i18n and l10n maturity | 8 | 8 | FR and EN are first-class and testimonies may be in any language ([plan 8](../plans/main.md)). |
| 5 | Magic-link auth ecosystem: library maintenance, sessions, CSRF, rate limits | 6 | 7 | Owner decision ([ADR 0003](../decisions/0003-email-magic-link-auth.md)), but libraries can be swapped. |
| 6 | Forms, server-side validation, accessible rendering without JavaScript | 6 | 7 | Accessibility is explicit ([plan 27](../plans/main.md)). G4 now carries the veto; this criterion measures ergonomics. |
| 7 | Database and search: PostgreSQL integration, ORM, migrations, French and English full-text search | 6 | 6 | Search quality matters ([plan 13](../plans/main.md)). |
| 8 | Security defaults and security-release process | 10 | 9 | Unpublished testimony, auth identifiers and privacy requests are held ([plan 26](../plans/main.md)). Raised because a weighted sum compensates, and real security failures do not. |
| 9 | Background jobs and scheduled tasks without extra infrastructure | 4 | 5 | Real, but cheap to change later (ADR 0002). |
| 10 | Deployment and operations on one VPS: runtime upgrades, memory, process model | 5 | 6 | ADR 0002. Real, but cheaper to change than the framework. |
| 11 | Successor-friendliness: talent pool and documentation | 6 | 6 | Explicit in plan section 29. |
| 12 | Dependency footprint and supply-chain exposure | 5 | 5 | Supply-chain surface is an owner requirement. |
| 13 | Testing | 3 | 3 | Important, but nearly every candidate has a mature test story. |
| 14 | Fit with the archive-first principle: domain model and export kept clean | 10 | 10 | ADR 0006 makes the export the primary product. |
| 15 | Type system and data-model expressiveness | 6 | - | New, on owner input. See below. |

Criterion 15. The archive's core is a data model with real structure. A testimony moves through states, each with different valid fields. Authorship disclosure is a closed set of codes with conditional details. Translations carry provenance that differs by producer. Public identity is optional field by field, some fields are forbidden for minors, and some must never be exported. A type system that makes invalid states unrepresentable, and flags every place a new state must be handled, lowers the risk of the failures the plan fears most, such as a private field leaking into an export. Judgement, from general knowledge rather than sourced in this pass:

- TypeScript has structural typing, discriminated unions with exhaustiveness checking, literal and template literal types, and mapped and conditional types, all checked on every build. Types are erased at runtime, so external data still needs runtime validation. Schema-first libraries derive static types from runtime validators.
- Python has optional type hints (`Literal`, unions, `TypedDict`, `Protocol`, dataclasses, `match`, `assert_never`), checked by external tools such as mypy or pyright. The checkers are good in strict mode, but library adoption is uneven. Django's ORM is dynamic, and its static typing depends on third-party stubs and a checker plugin.

The weight is 6 rather than higher because the canonical schema is specified independently of the application (ADR 0006, #13), for example as JSON Schema. Types can be generated from it in any language, and the export test validates against it whatever the stack.

### 4.3 Revision of 2026-11-15

The first version had 14 criteria, with "upgrade burden over 10+ years" at weight 9. On review, the owner pointed out two problems:

- A framework that is never updated would have scored 5 on that criterion, although updates normally bring security fixes and improvements.
- Popular frameworks scored surprisingly low, while pure Node.js was not catastrophic.

Changes made:

1. **Gates added** (section 4.1). Abandoned software now fails G5, so no criterion needs to reward or punish activity as such.
2. **Upgrade burden redefined** as the cost of staying supported (criterion 2). It measures breaking change and support-window length, not the number of releases. The scores did not need to change under the new definition, because the original judgements were already about breaking changes. What changed is the reasoning and the weight.
3. **Double counting removed.** Churn appeared under longevity (support windows), upgrade burden, and partly under dependency footprint: 25 of 100 points. It now accounts for 22 points, and support windows are counted only in criterion 2.
4. **Security raised** from 9 to 10, because compensation is most dangerous there.
5. **Criterion 15 added** at weight 6.
6. **Minor weights trimmed** to keep the sum at 100: magic links, forms, jobs and operations.

The effect of each change is shown in section 7: the matrix keeps the original totals for comparison, and section 7.2 tests the weight of churn directly.

## 5. Database choice: PostgreSQL, and the challenge to it

PostgreSQL is presumed. The challenge was asked for, so the tradeoff is stated here.

- The case for SQLite: one file, no database server, simple backup with its online backup mechanism, no extra service to patch, and enough capacity for a small archive. Its operational simplicity is real and would suit a successor.
- The case against SQLite for this project is specific. SQLite's FTS5 ships the unicode61 tokenizer (the default), an ascii tokenizer, a porter tokenizer and a trigram tokenizer. The porter stemmer is documented as designed for English only, and the document does not describe a French stemmer [S43]. French search would therefore be accent-folded and unstemmed, which is a real loss for a bilingual archive.
- The case for PostgreSQL: Snowball stemmers are documented for many languages [S42]; Django's own documentation uses config="french" in its search examples [S7], so PostgreSQL search configurations per testimony language are a practical option. PostgreSQL also gives row-level concurrency, LISTEN/NOTIFY and SKIP LOCKED for a job table. Rails' Solid Queue uses PostgreSQL's SKIP LOCKED [S13], and River runs on PostgreSQL [S40].
- Costs of PostgreSQL: one more service to install, patch and back up on the VPS. Local development needs a PostgreSQL install, which is a one-time setup step.
- Version: PostgreSQL 18 is the current major (18.7 on the versioning page). PostgreSQL 14's final release is 12 November 2026, three days before this document's date, so a new deployment should not start on 14 [S41]. PostgreSQL 19 is at release-candidate stage and is not supported yet [S41].
- Verified locally on Node 26 (section 6.12): its bundled SQLite has FTS5 with accent folding but no French stemming, which confirms the point above.

Recommendation for this section: keep PostgreSQL 18. Keep SQLite as a documented fallback only if the owner decides that the one-server simplicity outweighs French stemming. No candidate argued for SQLite in this pass.

## 6. Candidates: verified facts, strengths and weaknesses

Each candidate section lists facts that were checked in this pass with source tags, then strengths, then weaknesses. Items marked "not verified" were not checked and must be checked before any commitment.

### 6.1 Django (Python)

Verified facts:

- Supported series on the download page: 5.2 LTS (mainstream support ended 3 December 2025, extended support to April 2028); 6.0 (mainstream to 4 August 2026, extended to April 2027); 6.1 (mainstream to April 2027, extended to December 2027). Django 6.2 is listed as the next LTS with a planned release in April 2027 [S1].
- Release dates from the endoflife cross-check: 6.0 on 3 December 2025, 6.1 on 5 August 2026, latest 6.1.3 on 3 November 2026; 5.2 LTS EOL 30 April 2028 [S2] [S3].
- Django 6.0 ships a built-in Tasks framework and built-in Content Security Policy support [S3].
- The Tasks framework has no worker. Its built-in backends (ImmediateBackend and DummyBackend) are for development and testing only. Production needs a third-party backend with a worker process [S4].
- Admin: documented as recommended for an organization's internal management tool. Provides list filters, search, bulk actions, list_editable, and per-model permission hooks (has_view, has_change, has_delete and so on) [S6].
- i18n: gettext PO and MO files, makemessages and compilemessages, ngettext for plurals, i18n_patterns for locale-prefixed URLs, LocaleMiddleware and the LANGUAGES setting [S5]. The page does not describe the html lang attribute; it is normally set in the base template (not verified in docs).
- PostgreSQL search: SearchVector, SearchQuery, SearchRank, SearchHeadline, a config parameter per field (for example 'french'), GeneratedField maintained by PostgreSQL, and trigram similarity via pg_trgm [S7].
- Security policy: the two most recent release series and LTS releases receive security support. Reports go to <security@djangoproject.com>, acknowledgement within 3 working days, target resolution 90 days. Distributors get advance notice under embargo [S8].
- Foundation: the Django Software Foundation is a nonprofit with an elected board [S9].
- Magic-link packages (search results only, maintenance not verified): django-magiclink (PyPI shows 1.3.0) [S10]; django-magicauth from betagouv, version 1.0.2, which adds a second check via django-otp [S10]; django-magic-link appears to be unmaintained (metadata suggests about ten years old) [S10].
- Not verified: Django's deprecation policy and typical upgrade effort; Python minimum for Django 6.x; a first-party rate limiter (none was found in the pages read); the admin's change-history storage details.

Strengths:

- The strongest first-party admin of all candidates for one-person moderation work (R10).
- Mature gettext workflow with plurals and locale-prefixed URLs (R13). Translators can use standard PO tooling.
- PostgreSQL-native search with per-language configurations and maintained search columns, which makes deletion propagate to the search index automatically if the index is a generated column (R11).
- Server-rendered forms and templates by default, with no JavaScript needed for the core flow (R14).
- Foundation governance and a published, specific security process (R20).
- Large talent pool and documentation quality. Python 3.12 is supported until 31 October 2028 [S45].

Weaknesses:

- No first-party magic-link flow. A library must be chosen and its maintenance checked, or a minimal token flow built on Django's signing tools with the library's tests (ADR 0003, R7).
- The Tasks framework has no worker. Jobs need either a third-party database-backed backend, or systemd timers calling management commands (section 8 recommends the latter for the MVP as the simplest working solution).
- Rate limiting and some anti-abuse pieces are not first-party as far as checked; they are either third-party or done at the reverse proxy.
- The Python packaging supply chain (PyPI) needs lock files with hashes and regular updates; this is standard practice but is ongoing work.
- The admin is explicitly for internal use. That fits moderation, but the public site must be built separately, which is normal.
- Admin change history stores object representations; the deletion design must cover it (section 9).

### 6.2 Symfony (PHP)

Verified facts:

- Symfony 7.4 is LTS, released November 2025; bug fixes to November 2028, security fixes to November 2029 [S24].
- Symfony 6.4 is LTS; its bug-fix support ends November 2026 (this month) and its security support ends November 2027 [S24].
- Symfony 8.0 is unmaintained (support ended July 2026). Symfony 8.1 is the current stable line (May 2026) and 8.2 is scheduled for November 2026 [S24].
- Login links: built-in login-link authenticator with signed URLs, default lifetime 10 minutes, optional max_uses with a cache, and check_post_only recommended for single-use links because email scanners prefetch links. The docs warn that login links are less secure than password login and are not recommended for security-critical applications [S25].
- Translation: XLIFF and YAML files supported; ICU MessageFormat supported, but non-English ICU needs the PHP intl extension; locale in routes via the _locale parameter [S26].
- Messenger: a Doctrine transport stores messages in a database table; workers run via messenger:consume under a process manager [S27].
- Security: report to <security@symfony.com>; login throttling bypasses and similar hardening items are handled as regular bug fixes rather than security issues; patches go to all maintained versions [S28].
- Admin: EasyAdmin is an active third-party bundle (5.10.1 on 14 November) [S29]. There is no first-party admin.
- Governance: the 2018 Symfony blog post, found through search, describes Symfony SAS as the company managing the project, with SensioLabs sponsorship [S30]. This is an old source and must be refreshed.

Strengths:

- The clearest LTS model in the candidate list: 7.4 LTS to 2029 for security is the longest verified window here.
- Strong i18n tooling (XLIFF for translator workflows, ICU for plurals and select) and locale routing.
- Job handling without Redis or RabbitMQ through the Doctrine transport.
- First-party login links, which is closest to ADR 0003 among the candidates.
- Components can be used without the full framework, which helps keep the domain model clean (R1, R2).

Weaknesses:

- No first-party admin; EasyAdmin or a hand-built admin would be needed.
- The owner is comfortable with TypeScript, not PHP.
- Symfony's own docs advise caution about login links for security-critical use. A guestbook is not security-critical in that sense, but the owner should accept this on the record.
- The company-led governance model (Symfony SAS) needs a current check.
- Full-text search needs raw SQL or a Doctrine extension (not verified in this pass).

### 6.3 Laravel (PHP)

Verified facts:

- Laravel 13 was released 17 March 2026; it requires PHP 8.3 to 8.5. Bug fixes until Q3 2027; security fixes until 17 March 2028 [S17].
- Laravel 12 security fixes until 24 February 2027. Laravel 11 security fixes ended 12 March 2026 [S17].
- Policy: major releases annually; bug fixes for 18 months and security fixes for 2 years per release [S17].
- Localization: strings in PHP array files or JSON files; pluralization with pipe syntax, ranges and trans_choice; no XLIFF or gettext mention on the page read [S18].
- Queues: database driver, Redis, SQS and others; the worker is queue:work [S19].
- Security policy: <security@laravel.com>; no response timeline stated [S20].
- Magic links: several community packages (for example harrisonclewis/laravel-passwordless, SpykApp/passwordless-login, webteractive/laravel-passwordless) appear in search results; their maintenance was not verified [S22].
- Admin: Filament 5.11.3 is the active community admin panel (13 November) [S23]. Nova is listed as a Laravel product on the official site [S17]; its licence was not verified.
- License: MIT, copyright held by Taylor Otwell [S21]. The company that sells hosting and products is named differently in different sources (Laravel LLC or Laravel Holdings Inc.); the legal name was not verified.

Strengths:

- Large PHP community, strong documentation, a mature queue and scheduling story on the database driver.
- Filament gives an admin panel quickly, if the owner accepts Filament's dependency tree and upgrade cadence.

Weaknesses:

- Annual major releases, and each major gets only two years of security fixes [S17], so the upgrade cycle is a recurring duty.
- Company-led product (the legal entity is not verified, see above). Laravel 13 foregrounds AI features [S17]. That is not a technical reason to reject it, but the product direction is not aligned with an archive.
- The i18n model is weaker for translator workflows than gettext or XLIFF (not verified beyond the docs page read).
- Magic-link packages are numerous and of uneven maintenance; the owner would need to pick and audit one.

### 6.4 Ruby on Rails

Verified facts:

- Rails 8.1 was released 22 October 2025 [S11]. Bug fixes for 8.1.x ended 10 October 2026, and security fixes run to 10 October 2027 [S12]. Rails 8.0.x security fixes ended 7 November 2026, eight days before this document's date [S12]. Endoflife lists 8.1.4.1 and 8.0.5.2 as released 3 November 2026 [S11].
- Policy: each minor release gets one year of bug fixes and two years of security fixes [S12].
- Rails 8.0 was released 7 November 2024 [S13].
- Rails 8 ships a built-in authentication generator for password-based sign-in and password reset [S13] [S14]. Magic-link sign-in is not part of the generator (the security guide describes passwords only) [S14].
- Built-in rate limiting in controllers: rate_limit to: 10, within: 3.minutes is documented [S14]. CSRF protection is on by default [S14].
- Solid Queue (background jobs on PostgreSQL with SKIP LOCKED), Solid Cache and Kamal 2 deployment are part of Rails 8 [S13].
- Security: reports go privately through GitHub or HackerOne; acknowledgement "before or during our monthly security meeting depending on severity"; no fixed fix deadline [S15].
- Governance: the Rails Foundation with core member companies, including 37signals (search results only; not verified on the Foundation's own pages) [S59].
- Admin: no first-party admin. Administrate is a thoughtbot-maintained gem; its README says it is maintained and funded by thoughtbot, but no release date was visible on the page read [S58].

Strengths:

- Solid Queue removes the need for Redis for jobs and fits R17 well.
- Rails' authentication generator and rate_limit give a good password-free start that can be adapted.
- Strong conventions for forms and server rendering.

Weaknesses:

- Short per-minor support windows: each minor series gets security fixes for two years, so keeping up is a regular upgrade duty. Rails 8.0 security support has already ended, which is a concrete example of the burden.
- No first-party admin and no first-party magic-link flow.
- Large gem dependency tree (not verified in this pass).
- Less of the i18n and translator tooling is verified in this pass.

### 6.5 Phoenix (Elixir)

Verified facts:

- Phoenix documentation for v1.8.16 [S54] [S55].
- mix phx.gen.auth generates email-based (magic-link) authentication. The docs describe the assumption that the email owner controls the account. Password handling is described as something added if the developer wants it [S54].
- Requires Elixir 1.17 or later and Erlang 25 or later [S55].
- Phoenix is MIT licensed [S56].
- Gettext for Elixir (v1.0.2): PO files, ngettext for plurals, extract and merge workflow using mix gettext.extract and mix gettext.merge [S53].
- Not verified: Phoenix governance and release policy, the SECURITY.md content, Oban or any job library, Ecto full-text search, and the no-JavaScript behaviour of the generated forms.

Strengths:

- The most direct magic-link support among the candidates: the generator produces email-based authentication out of the box [S54].
- Gettext is a real PO-based i18n system.
- BEAM runtime is efficient for long-running processes on a small VPS (judgement).

Weaknesses:

- The generated UI leans on LiveView for interactive behaviour. The no-JavaScript requirement (R14) is achievable, but it needs deliberate work and was not verified here.
- Smallest talent pool among the candidates, and the owner would be the only Elixir person in the succession plan (judgement).
- No first-party admin.
- The documentation for security policy and long-term support was not found.

### 6.6 ASP.NET Core (C#)

Verified facts:

- .NET 10 is LTS, released November 2025, supported until November 2028 [S31] [S32].
- .NET 11 is STS, released November 2026, supported until November 2028 [S31].
- .NET 8 and .NET 9 reached end of support on 10 November 2026 [S32]. Microsoft's support page lists only .NET 10 and 11 as currently supported [S31].
- Servicing updates ship monthly; security fixes ship on patch Tuesday [S31].
- The ASP.NET Core Identity introduction page, as fetched, does not describe passwordless or magic-link sign-in [S33].
- Not verified in this pass: localization (resx and IStringLocalizer), admin tooling, durable background-job options (Hangfire or others), and Npgsql full-text search support. General knowledge says there is no first-party admin UI.

Strengths:

- Long LTS windows and monthly security servicing.
- Strong typing and tooling; a large enterprise talent pool.
- Runs on Linux on a VPS.

Weaknesses:

- No first-party magic-link flow found; a third-party library or custom code would be needed.
- No first-party admin.
- The .NET LTS cadence is a three-year window; the owner would need to track two-year STS releases if they wanted them, though LTS-only is an option.
- Ecosystem and dependency footprint are larger than Go (judgement).

### 6.7 Go (standard library plus minimal libraries)

Verified facts:

- Go 1.27 was released 19 August 2026, Go 1.26 on 10 February 2026, and Go 1.25 reaches end of life on 19 August 2026 [S34]. The policy is that each major release is supported until two newer major releases exist [S34].
- Security: report to <security@golang.org>; fixes go to the two most recent major releases and the head of the repository; the stated commitment is that issues are fixed or made public within 90 days of acknowledgement [S35].
- Go 1.25 adds net/http CrossOriginProtection, a CSRF protection based on Fetch metadata that does not need tokens or cookies [S36].
- Go 1.22 adds method and wildcard patterns to net/http.ServeMux [S37].
- golang.org/x/text/message (v0.44.0 as shown) provides localized formatting and message catalogs; plural and gender forms come from translator-supplied alternatives, with a gotext extraction tool [S38].
- alexedwards/scs: an MIT-licensed session manager that describes itself as stable and maintained; it does not accept new store backends except in cases of significant demand [S39].
- River: a background job system on PostgreSQL (and SQLite) that enqueues jobs transactionally; the vendor is River Software, LLC, and the site links to a Pro licence [S40]. Licence terms for the open-source core were not verified.
- Not verified: html/template behaviour, pgx, migration tools, and any Go magic-link library.

Strengths:

- Excellent upgrade story and low runtime footprint (a single binary).
- Smallest dependency surface if the owner builds the rest with the standard library (R20).
- Good security reporting process and a real support window.

Weaknesses:

- No first-party admin, no first-party magic-link flow, no first-party background jobs, no translator workflow beyond x/text tooling. Each is a substantial build, which counts directly against the one-person constraint (plan section 28).
- The "minimal libraries" approach shifts maintenance from a framework to the operator's own code.
- Talent pool is moderate and the code shape differs from most web-framework knowledge.

### 6.8 TypeScript: SvelteKit with Drizzle and Paraglide (strongest TypeScript contender)

Verified facts:

- SvelteKit: the latest release tag on the GitHub releases page is @sveltejs/kit 3.2.0 (10 November) [S47]. The release page does not state which Svelte major it requires; this was not verified.
- Form actions: they work without client-side JavaScript; use:enhance is a progressive enhancement that emulates the browser's native submission [S47]. This is the strongest verified fit for R14 among the TypeScript candidates.
- Paraglide JS: MIT-licensed compile-time i18n, v2 core package; typed message functions; plurals through Intl.PluralRules; ICU through a plugin; built-in locale URL mapping such as /en/about and /de/ueber [S48].
- Drizzle ORM: the latest stable tag on the releases page is 0.45.4 (8 October); 1.0.0-rc.5 is a pre-release (21 October) [S49]. A stable 1.0 has not shipped as of this check.
- Astro (considered, see 6.15): i18n routing verified, no message catalogs or pluralization on the routing page [S46].
- Not verified: magic-link libraries for SvelteKit, background job libraries for Node/PostgreSQL, the SvelteKit upgrade guide, and any admin framework.

Strengths:

- Best verified no-JavaScript form story among the TypeScript candidates.
- Clean TypeScript domain model and good testing tools (Vitest and Playwright are general knowledge, not verified here).
- Owner is comfortable with TypeScript.

Weaknesses:

- Most of the requirements that Django and Symfony provide first-party (admin, magic-link auth, background jobs, rate limits) are assembled from third-party packages. That is the main supply-chain and maintenance cost.
- Major-version churn: SvelteKit 3.x is the current line on the releases page [S47], and the official docs already document API changes between 2.x minor versions (for example PageProps was added in 2.16) [S47]. Upgrade effort between majors was not verified.
- Drizzle is still pre-1.0 on its stable line in this check [S49].

### 6.9 AdonisJS (TypeScript, full framework)

Verified facts:

- The GitHub releases page, as fetched, lists v7.6.0 as the latest release (dated 5 October). This was not cross-checked against the npm registry [S50].
- @adonisjs/i18n: translations in JSON or YAML under resources/lang; ICU message format by default, with plural, select and selectordinal; locale detection from Accept-Language and custom logic; no built-in locale URL prefix [S50].
- Authentication: three built-in guards (session cookies, access tokens, HTTP basic). The authentication introduction does not mention magic links or passwordless login [S50].
- Not verified: Node.js requirement, Lucid ORM and migrations, job support, security reporting policy, governance and the size of the maintainer team.

Strengths:

- The most complete first-party TypeScript full stack in the list, based on what was verified (sessions, i18n with ICU plurals).
- Single-framework approach reduces the number of libraries to track.

Weaknesses:

- No first-party magic-link flow found in the auth documentation. This is the main gap against ADR 0003.
- Governance and maintainer depth are unknown in this pass; a small maintainer base is a succession risk (judgement).
- Several important facts (Node requirement, ORM, jobs, security policy) were not verified.

Verdict: AdonisJS is a credible TypeScript option, but the verified gaps are on the critical path (magic link, background jobs) and the succession risk is not yet assessed. On verified evidence it is behind SvelteKit in the TypeScript comparison (section 7).

### 6.10 WordPress (PHP CMS)

Added 2026-11-15 at the owner's request, evaluated on the same criteria as the frameworks above. WordPress is a content management system rather than a framework: the question is whether the testimony lifecycle can be built on it as plugins and a theme.

Verified facts:

- Releases: WordPress 7.0 shipped on 20 May 2026 after a six-week delay; 7.1 on 19 August 2026; 7.1.4, a security release, on 28 October 2026; 7.2 reportedly planned for December 2026 [S60, secondary summaries].
- Requirements for 7.0: minimum PHP raised from 7.2.24 to 7.4. The hosting handbook recommends PHP 8.4 or 8.5 for new installs, and MySQL 8.4 or MariaDB 10.11 [S61, search summary].
- Security policy: "officially only the latest version of WordPress is supported". Fixes are backported to older branches "as a courtesy". Branches 4.1 to 4.6 stopped receiving updates in July 2025. There is no LTS line [S62, search summary].
- Ecosystem vulnerabilities, from Patchstack's yearly reports:
  - 2023: 97% in plugins, 3% in themes, 0.2% in core [S63].
  - 2024: 7,966 new vulnerabilities, 96% in plugins, 7 in core [S63].
  - 2025: 11,334 new vulnerabilities, 91% in plugins, 9% in themes, 6 in core [S64, secondary coverage of the 2026 report].
- Governance: WordPress.org is effectively controlled by Automattic's chief executive. The WP Engine v. Automattic litigation started in 2024. On 24 September 2026 a federal judge reinstated antitrust claims that Automattic used its control of WordPress.org to raise prices and force competitors to pay for previously free access. The case remains open. Automattic's own board briefly put its chief executive on leave in September 2026 [S65, secondary].
- Known from general knowledge, not verified in this pass:
  - Core supports only MySQL and MariaDB; SQLite only through a feature plugin, and no PostgreSQL.
  - Core search uses SQL pattern matching, with no stemming or relevance ranking.
  - Core has a "pending review" post status and a Contributor role that can write but not publish.
  - Core has had privacy tools for exporting and erasing personal data since 4.9.6.
  - Post revisions are stored, and WP-Cron runs on page visits unless replaced by system cron.
  - WP-CLI exists.
  - Interface translation uses gettext. Multilingual content and locale URLs need a plugin such as Polylang or WPML.
  - Comments, pingbacks and XML-RPC are enabled by default.

Strengths:

- Its moderation primitives map naturally onto the plan: a "pending" status and a role that can submit but not publish.
- The most polished editing interface of any candidate. It would make Context pages and the reference shelf easy to maintain (plan sections 16, 18).
- Core privacy tools for data-subject export and erasure exist, which no framework provides out of the box.
- The largest talent pool on the web. A successor who knows WordPress is the easiest to find of any candidate.
- Core itself has a good security record, automatic background updates, and strong backward compatibility.

Weaknesses:

- It is built for publishing posts, not for a privacy-separated archive. Testimonies, authorship disclosures, translation provenance and public identity would be forced into posts plus key-value metadata. Private and public fields would share tables. Redaction that preserves the original privately would be custom code fighting post revisions.
- Nearly every requirement beyond core is a plugin, and therefore a vendor and a vulnerability stream:
  - FR/EN content and locale URLs;
  - magic links and admin second factor;
  - search with French support;
  - a no-JavaScript front-end contribution form, since contributors must not land in the JavaScript block editor;
  - rate limiting and proof-of-work.
  
  That is where 91 to 97% of ecosystem vulnerabilities are.
- No PostgreSQL, and no real full-text search in core.
- The most attacked web software. Its default login and XML-RPC endpoints draw constant automated scanning (judgement).
- Social features are on by default and must be disabled, and kept disabled, against the "no social network" principle (plan section 15).
- No LTS. Only the latest release is supported, so updates are continuous. Automatic updates mitigate this for core, not for plugins.
- Governance is concentrated in one person, and that power is the subject of unresolved antitrust litigation. Every plugin and core update passes through WordPress.org.
- Archive-first fit is poor. Content is stored with editor block markup embedded in the post body, and the native export format is not the archive schema. A custom exporter and a custom data layer would carry the whole archive-first principle.

Verdict: WordPress is strongest where the plan asks least (editing context pages, finding a successor) and weakest where the plan asks most: the privacy-separated data model, the archive export, multilingual testimonies, passwordless authentication and a small attack surface. Not recommended as the application. Using it only for Context pages would add a second system holding an admin login and personal data, contrary to [privacy assumption](../constitution/privacy-assumptions.md) 10.

### 6.11 Next.js (TypeScript, React), and Vercel as a host

Added 2026-11-15 at the owner's request. Next.js, the framework, is scored self-hosted on the VPS like every other candidate. Vercel, the hosting platform it is designed around, is tested separately against the gates (section 4.1) and ADR 0002.

Verified facts (search summaries; the official support-policy page is cited by those summaries):

- Support policy: each major is in Active LTS until the next major ships, then in Maintenance LTS until two years after its initial release, receiving only critical and security fixes. 16.x was released on 21 October 2025 and is the only supported line since 15.x ended on 21 October 2026. 14.x and older get no patches. Next.js 17 had not shipped as of the sources found [S66].
- Releases: 16.2 (March 2026) made the Deployment Adapter API stable. 16.3 shipped in August 2026. 16.4.1, an out-of-band fix for two critical remote-code-execution vulnerabilities, followed in October 2026 [S66, S68].
- Requirements: Node.js 20.9 or later and TypeScript 5.1 or later [S68].
- Security history [S67]:
  - CVE-2025-29927 (March 2025, CVSS 9.1): middleware authorization bypass through a spoofable internal header, affecting self-hosted versions 11.1.4 to 15.2.2.
  - CVE-2025-55182, "React2Shell" (December 2025, CVSS 10.0): unauthenticated remote code execution through insecure deserialization in the React Server Components protocol, affecting Next.js 15 and 16 with the App Router. It was exploited within hours, added to CISA's Known Exploited Vulnerabilities catalog on 5 December 2025, and used in ransomware campaigns. Denial-of-service and source-exposure follow-ups came after it.
  - Another React Server Components remote-code-execution flaw was fixed on 14 October 2026.
- Self-hosting: supported as a Node server, in containers or as a static export. The Adapter API is meant to give other hosts parity with Vercel. Sources from spring 2026 say full parity is not there yet, and that some caching defaults behaved as intended only on Vercel [S68].
- Authentication: Auth.js (NextAuth) moved to the Better Auth team in September 2025 and receives security fixes only. Its v5 was still beta in September 2026. Better Auth has a magic-link plugin. One secondary source reports that Vercel acquired Better Auth on 7 July 2026 [S69, secondary].
- Not built in (general knowledge, not verified in this pass): admin, database access and migrations, background jobs, and i18n routing in the App Router. Each needs a separate library, for example next-intl, Drizzle or Prisma, and a job runner.

Vercel as a host [S70]:

- Vercel Inc. is a US company, certified under the EU-US Data Privacy Framework.
- Its DPA states that primary processing facilities are in the United States and that customer data may be processed wherever Vercel or its sub-processors operate. Its security FAQ says no data is stored permanently inside EU regions; EU regions such as `fra1` only cache responses ephemerally.
- The control plane, account data and support are in the US (secondary).
- Result: **fails gate G3** (EU-controlled processing) and contradicts ADR 0002. Vercel is excluded before scoring, whatever its convenience. The legal research (section 9) also recommends EU-controlled processors because of the CLOUD Act.

Strengths:

- TypeScript end to end, with the type-system advantage measured by criterion 15 (score 5).
- The largest React talent pool. Popular enough that it will not disappear.
- Server Components and Server Actions can render HTML on the server and accept form posts without client JavaScript when written carefully.
- A stable Adapter API and documented self-hosting.

Weaknesses:

- The highest upgrade churn of any candidate (judgement): a new routing model (Pages Router to App Router), caching semantics changed between majors, and yearly majors with two-year support windows. For a decades-long custodian this is a recurring rewrite tax.
- Its security surface is novel and complex. The React Server Components protocol produced a CVSS 10.0 remote-code-execution bug exploited in the wild, followed by more of the same class within a year. A middleware bypass hit self-hosters specifically.
- Governance and business model belong to a hosting company whose product is the platform the framework is optimized for. The authentication library most Next.js apps use reportedly now belongs to the same company.
- Nothing the plan needs beyond rendering is first-party: admin, database, jobs, i18n routing, rate limiting and magic links. Each is a separate dependency with its own churn.
- The largest dependency tree of the candidates (React, the framework, the bundler and the libraries above).
- Its centre of gravity is interactive client-side applications, while this archive is mostly documents and forms. The server and client boundary of Server Components makes it harder to see what runs where, which matters for G4 and for keeping private data out of client payloads.

Verdict: the lowest score among the real candidates. Next.js solves problems this project does not have (rich client interactivity, edge rendering at scale) and adds churn and security surface where the project is most sensitive. Vercel is excluded by G3. Among TypeScript options, SvelteKit, and better still the minimal TypeScript stack of section 6.13, are stronger.

### 6.12 Bare Node.js (no framework, no build step)

Added 2026-11-15 at the owner's request. The option: only Node.js. No framework, no runtime dependencies, nothing built in except what Node ships. No build step: plain JavaScript with types written as JSDoc comments.

Verified facts:

- Node.js 26 is the current LTS line, first released 2026-05-05. LTS lines typically receive critical fixes for 30 months in total. From Node.js 27 onwards, majors move to an annual cycle, each reaching LTS after six months as Current and six as Alpha [S71].
- `node:sqlite` is at stability 1.2, "Release candidate" (since v25.7.0), not yet Stable. It can load SQLite extensions when this is explicitly allowed at construction [S72].
- Tested locally on 2026-11-15 with Node v26.13.0, which bundles SQLite 3.54.0:
  - FTS5 is available with the `unicode61`, `porter` and `trigram` tokenizers. Some Node distributions reportedly ship without FTS5, so it must be probed at startup [S73].
  - With `remove_diacritics 2`, `eleve` matches "élève". `eleves` does not match "élève", and only the prefix query `elev*` finds both, so there is no French stemming (section 5).
  - `PRAGMA secure_delete` is 0 by default, so deleted content can remain readable in free pages of the database file until it is overwritten or vacuumed.
- Type stripping, which runs `.ts` files directly with no build step, is Stable since v25.2.0 and v24.12.0, and enabled by default. It accepts only erasable syntax and performs no type checking [S74].
- TypeScript 7, the native compiler (7.0 stable in July 2026 according to secondary sources), rewrote JavaScript and JSDoc checking. It dropped several legacy JSDoc behaviours, including special handling of `@enum` and `@constructor` and Closure-style function types [S75] [S76].
- Built into Node and usable directly:
  - an HTTP server;
  - `fetch`, enough to call a transactional email provider's HTTP API without an SMTP client;
  - `crypto`, `dns` (MX checks) and `Intl` (plural rules, dates, locales);
  - `URLSearchParams`, the `node:test` runner, `--watch` and `--env-file`.

What would have to be written by hand: everything a framework normally provides. This list is also a checklist of what any chosen stack must supply, or what must be audited if it does not.

| Concern | Risk if hand-written | Standard involved |
| --- | --- | --- |
| Routing, request and response helpers | Low | - |
| Cookie parsing and serialization | Medium | RFC 6265 |
| Sessions and their storage | High | - |
| CSRF protection | High | - |
| HTML templating with context-aware escaping | High: every escaping mistake is a stored XSS | HTML |
| Magic-link token issuance, confirmation POST and expiry | High | - |
| Admin second factor (WebAuthn) | Very high: unrealistic to hand-write correctly | WebAuthn |
| Security headers and CSP | Medium | CSP |
| Form validation and error re-rendering | Medium | - |
| Locale negotiation from `Accept-Language` | Low to medium | RFC 9110, RFC 4647 |
| Message catalogs and translator workflow | Medium: no PO or XLIFF tooling | - |
| Proof-of-work challenge (server and widget) | Medium | - |
| Rate limiting | Low | - |
| JSON Schema validation of exports | Medium | JSON Schema |
| Moderation console, redaction, privacy-request handling | Medium, but large | - |
| Migrations | Medium | - |

Several rows implement standards. Using libraries for standardized formats and protocols is an established practice of this project, and this option contradicts it in those rows.

Gates: G1 passes provided `secure_delete` is on, the database is vacuumed after deletions and the backup lifecycle is respected. G2, G3 and G4 pass. G5 is conditional on `node:sqlite` becoming Stable.

Strengths:

- The most transparent option: everything that runs is the project's own small code on a foundation-governed runtime with a predictable LTS.
- Zero runtime dependencies, one process, one SQLite file, low memory.
- The best archive fit. There is no ORM between the domain model and the export, the same code renders edition HTML, and with no build step the code that runs is the code that is preserved.
- Most of TypeScript's checking through JSDoc, or all of it through native type stripping.

Weaknesses:

- The custodian becomes the sole maintainer of a small security-critical framework, with no external security process, no advisories and no other users finding its bugs. The table above is that framework's backlog.
- SQLite only, with no French stemming, and its Node binding is still a release candidate. PostgreSQL would need a driver dependency.
- No admin, no translator workflow, and no auto-escaping templates.
- Types as comments depend on the checker's JSDoc dialect, which TypeScript 7 just tightened. The code ages well; its annotations may need maintenance.

Variants, under the weights of section 4.2:

- Native `.ts` type stripping instead of JSDoc: criterion 15 rises to 5, total 66.8.
- One audited dependency, a PostgreSQL driver: criterion 7 rises to 4, total 68.0. With both: 69.2.

What it teaches, for every candidate:

- Zero dependencies does not mean zero maintenance. It moves the maintenance into the custodian's code.
- A framework's real value here is its security plumbing and its admin. Whatever is chosen should be judged mostly on how well it provides those.
- Deletion is never immediate at the storage layer. SQLite keeps deleted content in free pages unless `secure_delete` is on, and PostgreSQL keeps dead row versions until vacuum and in its write-ahead log. The deletion lifecycle (#16) must cover storage-level remnants, not just rows.
- French search is a recurring gap for every SQLite-based option. With a few thousand testimonies, prefix and accent-folded matching may be acceptable, but that is a product decision.

Verdict: not recommended in its pure form, because one person would carry the whole security surface. Its defensible form is "Node plus a short allow-list of small, audited libraries": sessions or cookies, templating with auto-escaping, WebAuthn for admin, and optionally a PostgreSQL driver. That minimal TypeScript stack keeps most of this option's strengths and removes its worst weaknesses. It is evaluated in section 6.13.

### 6.13 Minimal TypeScript (Node.js, TypeScript and key libraries)

Added 2026-11-15 at the owner's request. This is the practical form of section 6.12. The base is Node.js LTS, with source code in TypeScript run through Node's native type stripping (no build step) and checked by `tsc`. Security-sensitive and standards-defined concerns get a library. Everything else stays in the project's own code.

Library set. Versions, licences and repository activity were read from the npm registry and GitHub on 2026-11-15 [S77].

| Concern | Library | Version | Licence | Maintained by | Notes |
| --- | --- | --- | --- | --- | --- |
| HTTP server, routing, request validation by JSON Schema, test injection | `fastify` | 5.12.8 | MIT | Fastify organization, an OpenJS Foundation At-Large project [S78] | 15 direct dependencies. Security updates for a major continue six months after the next major ships [S78]. Its main branch already targets v6. |
| Cookies | `@fastify/cookie` | 11.1.5 | MIT | Fastify organization | Covered by the organization-wide security policy |
| Server-side sessions | `@fastify/session` | 11.1.6 | MIT | Fastify organization | Sessions stored in PostgreSQL through a small in-project store adapter, so they can be revoked |
| CSRF protection | `@fastify/csrf-protection` | 8.0.2 | MIT | Fastify organization | |
| Security headers and CSP | `@fastify/helmet` | 13.2.0 | MIT | Fastify organization | |
| Rate limiting | `@fastify/rate-limit` | 11.2.2 | MIT | Fastify organization | |
| Form parsing | `@fastify/formbody` | 9.0.2 | MIT | Fastify organization | |
| HTML templates | `eta` | 4.6.0 | MIT | One maintainer | No dependencies. `autoEscape` defaults to true [S79]. |
| Admin second factor (WebAuthn) | `@simplewebauthn/server` | 14.1.0 | MIT | One maintainer | 10 direct dependencies for ASN.1 and COSE parsing. Requires Node 22 or later. |
| Typed SQL query builder and migrations | `kysely` | 0.29.9 | MIT | kysely-org | No dependencies; still 0.x |
| PostgreSQL driver | `pg` | 8.23.1 | MIT | One long-standing maintainer | 6 direct dependencies; Kysely's built-in PostgreSQL dialect uses it |
| Schemas producing both JSON Schema and static types | `typebox` | 1.4.7 | MIT | One maintainer | No dependencies. Its schemas are JSON Schema, the same artefact family as the archive specification. |
| Message formatting (ICU plurals and select) | `intl-messageformat` | 12.1.5 | BSD-3-Clause | FormatJS organization | |
| Locale negotiation (BCP 47 lookup) | `@formatjs/intl-localematcher` | 0.10.1 | MIT | FormatJS organization | |
| Proof-of-work challenge, server side | `altcha-lib` | 2.8.0 | MIT | ALTCHA organization | No dependencies |
| Type checking, development only | `typescript` | 7.0.2 | Apache-2.0 | Microsoft | |

Not taken from npm:

- The disposable-domain blocklist is vendored from the maintained, CC0-licensed GitHub list (ADR 0003, [S52]) and refreshed by a script. The `disposable-email-domains` npm package was last published in 2022.
- Static files are served by the reverse proxy, which makes `@fastify/static` unnecessary.
- From the runtime itself: `node:crypto` (random tokens, hashing, constant-time comparison), `fetch` (the email provider's HTTP API), and `node:test`, used with Fastify's request injection for testing.

Measured footprint: a scratch install of the runtime libraries above, plus `@fastify/static` for an upper bound, resolved to 126 packages. Licences in the tree are MIT, ISC, BSD-3-Clause, Apache-2.0, 0BSD and BlueOak-1.0.0. By direct dependency, Fastify brings 45 packages, `@fastify/static` 25, `@simplewebauthn/server` 24, `pg` 14, and the others 0 to 4 each. Without `@fastify/static`, expect roughly 100. The install ran with lifecycle scripts disabled [S77].

Security policies: Node.js, TypeScript, the Fastify organization (one policy covering all its repositories), Kysely and ALTCHA publish a `SECURITY.md`. node-postgres, SimpleWebAuthn, Eta, TypeBox and FormatJS do not publish one in their repositories [S77].

Still hand-written, but on library primitives:

- the magic-link flow: token issuance and expiry on `node:crypto`, a confirmation POST, and the session;
- the session store adapter;
- locale-prefixed routing;
- the moderation console screens;
- job scripts run by systemd timers;
- the deletion procedures.

None of these implements a standard or a cryptographic primitive itself.

Gates: G1 to G4 pass, with the same storage-level deletion care as any PostgreSQL candidate. G5 is conditional: the runtime, compiler, framework, query builder and proof-of-work library publish security processes, but five key libraries do not.

Scores (judgement):

| # | Criterion | Score | Reason |
| --- | --- | --- | --- |
| 1 | Longevity and governance | 3 | Foundation-governed runtime and framework, but several essential libraries have one maintainer each. Each is small and replaceable. |
| 2 | Cost of staying supported | 3 | Many independent release streams: a yearly Node major, Fastify majors with a six-month overlap and v6 near, Kysely still 0.x, and the TypeScript 7 transition. |
| 3 | Admin | 2 | Sessions, forms, templates and validation exist, but the moderation console is built screen by screen. |
| 4 | i18n | 3 | ICU message formatting and standards-based locale matching, but no catalog extraction or translator workflow, and hand-written locale routing |
| 5 | Magic-link ecosystem | 3 | Thin in-project flow on audited primitives; library sessions, CSRF and rate limits; WebAuthn for admin |
| 6 | Forms and no-JS | 4 | Server-rendered with auto-escaping templates, schema-validated form bodies with typed results |
| 7 | Database and search | 4 | PostgreSQL with typed queries and migrations; full-text search in SQL with French and English configurations |
| 8 | Security defaults and process | 3 | Every security concern has a maintained library, but composing them correctly is the project's job, and no framework-level secure defaults tie them together. Clears the optional security floor of section 7.3. |
| 9 | Jobs | 3 | systemd timers running TypeScript scripts |
| 10 | Operations | 4 | One light Node process plus PostgreSQL |
| 11 | Successor-friendliness | 3 | TypeScript and Fastify are widely known, but the assembly is project-specific and must be documented |
| 12 | Dependency footprint | 3 | About 100 packages, all permissively licensed: more than Django or Go, far fewer than the TypeScript frameworks |
| 13 | Testing | 4 | `node:test` plus Fastify request injection |
| 14 | Archive-first fit | 5 | One TypeBox schema can be the JSON Schema of the archive specification, the request validator and the TypeScript type. There is no ORM, and the exporter shares the domain types. |
| 15 | Type system | 5 | TypeScript throughout, including typed SQL and typed schemas. Templates are the exception: Eta templates are strings and are not type-checked. |

Weighted total: **68.8**, or 66.8 under the original criteria.

Variants (judgement, not scored):

- A compile step would allow TSX templates rendered on the server, typed by the compiler and escaped by default. That closes the template typing gap, at the cost of the no-build-step property.
- Hono instead of Fastify: zero dependencies, with built-in cookie, CSRF and secure-header helpers, but no first-party session or rate-limit plugins, and no foundation governance.

Strengths:

- The best-typed option in the matrix, with the strongest archive fit: one schema can serve the archive specification, the validation and the types.
- Every security-sensitive or standards-defined concern is handled by a maintained library. This removes the main objection to bare Node.js and follows the project's own practice of using libraries for standards.
- Light to operate, transparent, and a moderate dependency tree with permissive licences.

Weaknesses:

- No admin. The moderation console, which is a daily tool, is hand-built.
- Many independent maintainers and release streams. Five essential libraries publish no security policy, and several have one maintainer.
- Security comes from composing libraries correctly, not from a framework's defaults. The threat model and tests must carry that.
- A successor inherits a project-specific assembly rather than a framework with its own documentation.

Verdict: the strongest TypeScript-family option, and in a near-tie with ASP.NET Core and Go for third place. It trades Django's first-party admin, i18n workflow and single governance for full TypeScript and the best archive fit. It is the credible alternative if TypeScript matters to the owner as much as the custodial evidence suggests it might (section 10).

### 6.14 Reference anti-stack (scale floor)

Added 2026-11-15 at the owner's request: the criteria applied in reverse, to design the worst possible stack. It is a deliberate composite of real categories, not a review of any particular product. It fails all five gates and is scored only to mark the floor of the scale (20).

The stack:

- A client-rendered single-page app on a 0.x meta-framework maintained by one venture-funded developer, shipping breaking changes weekly.
- A dozen microservices on Kubernetes spread across three US clouds.
- Testimonies in a proprietary schemaless serverless document store. "For permanence", each one is also written in full to a public blockchain and pinned on IPFS.
- Sign-in through a social network whose profile photo and name appear next to the testimony by default.
- An interface machine-translated at runtime by a third-party AI API, which also receives drafts "to suggest improvements".
- Moderation in the database vendor's web console. Jobs on a queue SaaS triggered by a cron SaaS.
- Session-replay analytics recording every keystroke in the contribution form "for UX insights".
- A lockfile resolving to 2,000 packages, and no tests.

| # | Criterion | Anti-stack choice |
| --- | --- | --- |
| 1 | Longevity and governance | 0.x framework, one maintainer, dependent on funding |
| 2 | Cost of staying supported | Weekly breaking changes across a dozen services |
| 3 | Admin | The database vendor's console: no redaction, no audit, no privacy workflow |
| 4 | i18n | Runtime machine translation; no catalogs, no review, no plural rules |
| 5 | Auth | Social login that publishes the account identity, the opposite of plan section 4 |
| 6 | Forms and no-JS | Nothing renders without JavaScript; validation only on the client |
| 7 | Database and search | Schemaless proprietary store, no French search, personal data duplicated across documents |
| 8 | Security | Keystroke recording, drafts sent to a third party, unpatched 0.x dependencies |
| 9 | Jobs | Two extra SaaS dependencies for what a timer could do |
| 10 | Operations | Kubernetes across three clouds, for one person |
| 11 | Successor | Nobody can understand it, including its author six months later |
| 12 | Dependency footprint | 2,000 packages plus a dozen external services |
| 13 | Testing | None |
| 14 | Archive-first fit | Data locked in a vendor format; the only "permanent" copy can never be corrected or erased |
| 15 | Type system | Untyped JavaScript |

What it teaches:

1. **Permanence is not immutability.** The blockchain is the most instructive mistake because it maximizes the property people naively associate with archives. It makes erasure impossible, which turns every withdrawal request into an unresolvable GDPR violation and contradicts the [deletion philosophy](../constitution/deletion-philosophy.md) at its root. The archive needs stable identity with revisable content: identifiers that never change, and editions that can be revised for privacy.
2. **The export is the product.** A platform that cannot be left losslessly fails ADR 0006, whatever else it does well. Vendor lock-in is a preservation failure, not just a cost.
3. **Jurisdiction is part of the stack.** US clouds, a US identity provider and a US AI API make the CLOUD Act and transfer questions ([legal research](../research/legal-landscape.md), section 9) unavoidable.
4. **Server-rendered HTML is an archival format in itself.** A page that needs a JavaScript runtime to show its text is inaccessible to some people, invisible to some search engines, and poorly captured by the BnF and Wayback crawlers.
5. **Every system holding personal data multiplies the cost of deletion.** Each extra service is one more place deletion must reach, one more processor agreement and one more breach surface ([privacy assumption](../constitution/privacy-assumptions.md) 10).
6. **Breaking change is a tax paid in custodial attention.** Over ten years, a framework that breaks weekly costs more than any feature it offers (plan section 37).
7. **"Helpful" AI integrations leak unpublished testimony.** The [threat model](../specs/threat-model.md) (section 3.6) forbids sending unpublished content to third parties.

These lessons are the origin of the gates in section 4.1.

### 6.15 Astro (considered, not a primary candidate)

- Astro's current major is 7 (astro@7.4.12 on 13 November in the GitHub releases page) [S46].
- Built-in i18n routing: locale folders, prefixDefaultLocale, fallback and domain mapping [S46]. No message catalogs or pluralization are covered on that page [S46].
- Astro is an excellent static-HTML generator. It fits the "static HTML for published testimonies and editions" idea (ADR 0006) well, but a dynamic app (magic links, admin, moderation queue) is not its centre of gravity. It is noted as a possible companion for Context and editions, not as the application.

### 6.16 CMS-on-framework options for Context pages (optional, not mandatory)

- Wagtail (on Django): Wagtail 7.4 is LTS (released 4 May 2026) with security support until 2 November 2027; Wagtail 8.1 was released 2 November 2026 [S57]. A page-tree CMS would add an editor UI for Context pages. The cost is another dependency stream and another upgrade stream. Judgement: markdown files in the repository, rendered by the app, are simpler and more archive-friendly. Not required.
- Filament (on Laravel): 5.11.3 active (13 November) [S23]. Relevant only if Laravel were chosen.
- EasyAdmin (on Symfony): 5.10.1 active (14 November) [S29]. Relevant only if Symfony were chosen.
- Statamic: not evaluated.

## 7. Scoring matrix

Scores are 1 to 5 (5 best). They are judgements based on the verified facts in section 6, and on general experience where marked "not verified". Weighted total = sum of (score times weight) divided by 5, so the maximum is 100 and the floor, a score of 1 everywhere, is 20. Columns are ordered by weighted total. The last row keeps the totals of the first version (14 criteria, original weights; section 4.3) for comparison.

| # | Criterion | Weight | Django | Symfony 7.4 | ASP.NET Core | Go | Minimal TypeScript | Bare Node.js | Laravel 13 | Rails 8.1 | Phoenix | SvelteKit | AdonisJS | WordPress | Next.js (self-hosted) | Anti-stack |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Longevity and governance | 10 | 5 | 4 | 4 | 4 | 3 | 4 | 3 | 3 | 3 | 3 | 2 | 3 | 3 | 1 |
| 2 | Cost of staying supported | 7 | 4 | 4 | 3 | 5 | 3 | 4 | 3 | 2 | 3 | 2 | 3 | 4 | 1 | 1 |
| 3 | Admin | 8 | 5 | 3 | 2 | 1 | 2 | 1 | 3 | 2 | 2 | 1 | 2 | 4 | 1 | 1 |
| 4 | i18n | 8 | 5 | 5 | 4 | 3 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 3 | 3 | 1 |
| 5 | Magic-link ecosystem | 6 | 3 | 4 | 2 | 2 | 3 | 2 | 3 | 3 | 4 | 2 | 2 | 2 | 3 | 1 |
| 6 | Forms and no-JS | 6 | 5 | 4 | 4 | 4 | 4 | 3 | 4 | 4 | 3 | 5 | 3 | 3 | 3 | 1 |
| 7 | Database and search | 6 | 5 | 3 | 4 | 3 | 4 | 2 | 3 | 4 | 4 | 3 | 3 | 1 | 3 | 1 |
| 8 | Security defaults and process | 10 | 5 | 4 | 4 | 4 | 3 | 2 | 3 | 4 | 3 | 3 | 3 | 2 | 2 | 1 |
| 9 | Jobs without extra infrastructure | 4 | 3 | 5 | 3 | 3 | 3 | 3 | 4 | 5 | 3 | 2 | 2 | 3 | 2 | 1 |
| 10 | Operations on one VPS | 5 | 4 | 4 | 4 | 5 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 1 |
| 11 | Successor-friendliness | 6 | 5 | 4 | 3 | 3 | 3 | 3 | 4 | 4 | 2 | 3 | 3 | 5 | 4 | 1 |
| 12 | Dependency footprint | 5 | 4 | 3 | 3 | 5 | 3 | 5 | 3 | 3 | 4 | 2 | 2 | 2 | 1 | 1 |
| 13 | Testing | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 2 | 3 | 1 |
| 14 | Archive-first fit | 10 | 4 | 4 | 4 | 4 | 5 | 5 | 3 | 3 | 3 | 4 | 3 | 2 | 3 | 1 |
| 15 | Type system and data-model expressiveness | 6 | 2 | 3 | 4 | 2 | 5 | 4 | 2 | 1 | 2 | 5 | 5 | 1 | 5 | 1 |
| | **Weighted total** | 100 | **86.4** | **77.4** | **70.0** | **69.0** | **68.8** | **65.6** | **63.6** | **63.4** | **62.6** | **62.4** | **58.4** | **54.8** | **52.8** | **20.0** |
| | Total with the original 14 criteria and weights | | 88.6 | 78.8 | 69.0 | 71.4 | 66.8 | 65.4 | 65.4 | 66.0 | 64.2 | 59.8 | 55.6 | 57.8 | 49.6 | 20.0 |

Ranking:

1. Django 86.4
2. Symfony 77.4
3. ASP.NET Core 70.0
4. Go 69.0
5. Minimal TypeScript 68.8
6. Bare Node.js 65.6
7. Laravel 63.6
8. Rails 63.4
9. Phoenix 62.6
10. SvelteKit 62.4
11. AdonisJS 58.4
12. WordPress 54.8
13. Next.js self-hosted 52.8

Next.js on Vercel is excluded by G3. The anti-stack fails every gate and appears only as the floor.

### 7.1 Reading the matrix

- Django's lead over Symfony comes mainly from admin (+2 points at weight 8), database and search, security process, longevity and successor-friendliness. Symfony leads on jobs, magic links and types.
- Third to fifth place is a near-tie: ASP.NET Core 70.0, Go 69.0 and minimal TypeScript 68.8, within 1.2 points, which is less than the uncertainty of the judgements.
  - ASP.NET Core is the most balanced.
  - Go is the most frugal.
  - Minimal TypeScript is the best typed and the best archive fit, and pays for it with a hand-built admin and many independent maintainers.
- ASP.NET Core and Go swapped places compared with the first version. The type criterion favours ASP.NET Core, and the lower weight of criterion 2 costs Go some of its compatibility advantage. A reasonable owner who values minimal dependencies more than first-party features could still put Go higher.
- Minimal TypeScript gains 3.2 points over bare Node.js. Through its libraries, admin, magic links, forms, security and types each go up one step, and database and search up two. The same libraries cost one step each on longevity, cost of staying supported and operations, and two on dependency footprint.
- Bare Node.js scores 5 on operations, dependencies and archive fit, and 4 on longevity, cost of staying supported, testing and types. It scores 1 or 2 on admin, magic links, database and security. Section 7.3 explains why that profile does not collapse.
- WordPress has the most uneven profile of the real candidates: 4 on admin and 5 on successor-friendliness, but 1 on database and 2 on security, archive fit and dependencies. Its strengths are in content editing, which the plan needs least.
- Next.js loses on cost of staying supported (1), security history (2), first-party completeness (admin 1, jobs 2) and dependency footprint (1). Its benefits, interactive client rendering and edge delivery, are not requirements here.
- The scores are judgements. A 3 means "adequate with known gaps". Differences of about 2 points or less are within the range that different reasonable judgements could move. Django and Symfony are clearly separated from the rest; the order from third place down is not.

### 7.2 Sensitivity: does churn decide the ranking?

Totals with criterion 2 (cost of staying supported) at weight 0, at the adopted 7, and doubled to 14, with all other weights unchanged and totals renormalized to 100:

| Candidate | Criterion 2 at weight 0 | At 7 (adopted) | At 14 |
| --- | --- | --- | --- |
| Django | 86.9 | 86.4 | 86.0 |
| Symfony 7.4 | 77.2 | 77.4 | 77.6 |
| ASP.NET Core | 70.8 | 70.0 | 69.3 |
| Go | 66.7 | 69.0 | 71.0 |
| Minimal TypeScript | 69.5 | 68.8 | 68.2 |
| Bare Node.js | 64.5 | 65.6 | 66.5 |
| Laravel 13 | 63.9 | 63.6 | 63.4 |
| Rails 8.1 | 65.2 | 63.4 | 61.9 |
| Phoenix | 62.8 | 62.6 | 62.4 |
| SvelteKit | 64.1 | 62.4 | 60.9 |
| AdonisJS | 58.3 | 58.4 | 58.5 |
| WordPress | 52.9 | 54.8 | 56.4 |
| Next.js (self-hosted) | 55.3 | 52.8 | 50.7 |
| Anti-stack | 20.0 | 20.0 | 20.0 |

Removing the criterion entirely leaves the top three unchanged. Minimal TypeScript moves ahead of Go for fourth place. Other movements:

- Go: down 2.3.
- SvelteKit: up 1.7.
- Next.js: up 2.5.

Even with churn ignored entirely, Next.js stays second to last and SvelteKit stays in the second half. Churn is not why these frameworks score low.

### 7.3 Why popular frameworks score low, and why bare Node.js does not collapse

- **The criteria measure fit, not quality.** They describe one custodian keeping a privacy-sensitive archive alive for decades. Popularity enters only through successor-friendliness (weight 6). A framework can be excellent and still be a poor fit.
- **About a third of the weight measures what the stack provides first-party for one person:** admin 8, i18n 8, magic links 6, database and search 6, jobs 4, which is 32 points. Next.js, SvelteKit and WordPress are popular for work where those pieces come from elsewhere: a team, hosted services or plugins. Here, every missing piece is assembled and maintained by one person.
- **A 55 is not a failure.** On a 20 to 100 scale the midpoint is 60, so the popular frameworks sit around the middle: adequate with significant gaps for this use.
- **Bare Node.js survives because the sum is compensatory.** Its fives on operations, dependencies and archive fit pay for its ones and twos on admin, magic links, database and security. The real cost of the second group is not linear. Hand-written sessions, CSRF protection, escaping and WebAuthn are a permanent security liability for one person, and a 2 out of 5 understates that. This is the limit of a weighted-sum method, and the reason for the gates.
- **Option, not applied by default (question 13):** a non-compensatory floor of 3 on security. It would exclude bare Node.js in its pure form, WordPress and Next.js, and leave the other ten candidates. Minimal TypeScript (section 6.13) scores 3 and clears it.

## 8. Architecture sketch (applies to any winner)

The architecture is the same whichever framework wins. Only the application container changes.

Components:

- Application process: the web application (Django with Gunicorn, or the equivalent for the chosen stack). Serves public pages, the contribution flow, the magic-link flow and the admin under a separate path. Admin access restricted at the proxy (IP allow-list or VPN) and protected by a second factor where the framework permits (not verified for each candidate).
- Reverse proxy: TLS termination, static files, caching for published testimony pages and edition HTML, and coarse rate limits. Caddy or nginx; choice not evaluated here.
- PostgreSQL 18: operational store for drafts, moderation, accounts (minimal), privacy requests, translations, context pages and search columns. Separate database user per role.
- Job runner: systemd timers calling idempotent management or CLI commands for email sending, token and rate-limit expiry, export builds and backups. Where a queue is needed for email, a Postgres-backed table with SKIP LOCKED (or the framework's database queue) is sufficient on one VPS. This keeps the infrastructure to the VPS plus Postgres.
- Mail: transactional provider with DNS authentication (SPF, DKIM, DMARC), per ADR 0003 and issue #10.
- Backups: PostgreSQL logical dumps in custom format plus optional continuous WAL archiving, encrypted, copied to storage operated by a different provider (ADR 0002). Restore drills run on a schedule and are documented in docs/operations/.
- Archive exporter: a separate command that reads the database through the same domain layer as the app, and writes an edition package. It is part of the core and runs continuously in tests (ADR 0006). Round-trip test: export, validate against the schema, re-import into a scratch database, compare identifiers and checksums.
- Archive format: specified in docs/specs/archive-format.md (issue #13), independent of the application. The research note (domain-and-persistence) proposes BagIt (RFC 8493) per edition for transfer and OCFL 1.1 objects for successive editions, with an explicit purge procedure for privacy revisions. These are proposals, not decisions; the specification decides.
- Testimony identifiers: opaque, assigned at publication, never reused, no year and no sequence in the public form; internal keys are separate (domain research, section 3.8).
- Deletion propagation: database rows with cascading foreign keys; search columns derived in the database (generated or trigger-maintained) so they go with the row; cache keys per testimony; generated translations and static renderings removed by a defined procedure; backup expiry on a documented schedule (retention to be set with legal review).
- Logs and analytics: minimal application logs with short retention; hashed IP for rate limits with short retention (ADR 0003); no third-party analytics.
- Secrets: environment files outside the repository, never in exports; .env stays ignored (AGENTS.md).
- Monitoring: a health endpoint, a daily check of backlog, failed mail sends, failed exports, and backup age. Notifications to the operator only (plan section 31).

Sketch:

```
visitors
   |
reverse proxy (TLS, static files, page cache, coarse rate limits)
   |
app process (public site, contribution flow, magic links, admin on a restricted path)
   |                         |
PostgreSQL 18               job runner (systemd timers -> management commands)
   |                         |
   +-- backups (encrypted, other provider) --- restore drills
   |
   +-- archive exporter (CLI, reads via domain layer)
            |
            v
     edition package (spec-defined, independent of app)
     + withdrawal index + checksums + schema docs
```

## 9. Operational and privacy notes that apply to all candidates

- Deletion must reach admin history, sessions, logs and backups. Django's admin keeps an object history view [S6]; the other candidates have comparable admin or audit logs (not verified per framework). The design must decide what they store and for how long (R11).
- Backups: a deleted testimony remains in backups until they expire. The plan requires a deletion lifecycle for backups (plan section 21, 30). The retention figure is a legal and operational decision, not a stack decision.
- The archive format must not depend on the application's serialization. Framework-native serialization (pickle, PHP serialize, Marshal) must never be used for exports.
- Outbound links are rel="ugc nofollow" by policy (ADR 0003). This is trivial in any stack.
- The admin must not expose the export of unpublished submissions. Export builds read published testimonies only.
- Deletion is never immediate at the storage layer. SQLite keeps deleted content in free pages unless `secure_delete` is on, and PostgreSQL keeps dead row versions until vacuum and in its write-ahead log. The deletion lifecycle (#16) must cover these remnants (section 6.12).

## 10. Owner context (noted, not scored)

- Local tooling is not a constraint (owner clarification, 2026-11-15). Any runtime, PostgreSQL or Docker can be installed, and development can happen on other machines. Missing tools are a setup step, not a risk, and do not favour any candidate.
- Python 3.12 is supported until 31 October 2028 [S45]. Node 26 is the current LTS line, released 5 May 2026, with active LTS support until 27 October 2027 and maintenance support until 30 April 2029 [S44].
- The owner values TypeScript for expressing complex data models, and finds Python more complicated. Criterion 15 measures the technical side of this. What the matrix cannot measure is the custodian: a project that lasts decades depends on its maintainer wanting to keep working in the code. If writing Python would make the owner less willing to tend the archive, that is a custodial risk the weights do not capture, and it is the owner's call to weigh it.
- A hybrid is possible but has a cost: archive tooling (schema, validator, edition renderer) in TypeScript, and the operational app in Django. It gives the strongest types where the archive lives, at the price of two runtimes and two ecosystems for one person.
- Because ADR 0006 makes the archive the primary deliverable, a later move between stacks is less costly than usual if the archive specification and exporter are done first. This is the strongest argument for making a provisional choice now, and recording it as an ADR that can be superseded.

## 11. Recommendation

Top recommendation: Django 6.x (or Django 5.2 LTS if the owner prefers the longer already-published LTS window to April 2028), with PostgreSQL 18. It scores 86.4, and was first under the original criteria as well.

Why:

- It scores highest on the criteria that matter most under this plan: longevity, archive fit, security, admin and i18n.
- Django's admin provides the one-person moderation surface with no extra product (R10).
- gettext plus i18n_patterns is a mature FR and EN workflow with a translator-friendly file format (R13).
- PostgreSQL search with per-language configurations can cover French and English (Django's documented examples use 'french' and 'english' [S7]; the full PostgreSQL configuration list was not verified [S42]). A generated search column follows the row on deletion (R11, R12).
- The DSF governance, the published security policy and the release cadence were verified (S1, S8, S9; R20).
- The gaps are known and bounded:
  - choose and audit a magic-link library;
  - build the job runner from management commands and systemd timers, or a database-backed package;
  - add rate limits at the proxy and in a small Postgres-backed counter;
  - treat admin second factor as a deliberate addition;
  - use strict type checking with stubs, and generate types from the archive schema, to narrow the typing gap.

Upgrade plan (judgement): target 6.2 LTS when it ships (planned for April 2027 per the download page [S1]); until then use 6.1 or 5.2 LTS. Verify the 6.2 support window when released.

Runner-up: Symfony 7.4 LTS (PHP), at 77.4.

A reasonable owner might pick Symfony instead of Django for these reasons:

- The LTS model is the most explicit in this list, and the 7.4 security window to November 2029 is the longest verified (S24).
- Symfony has a first-party login-link feature, strong translation tooling with XLIFF and ICU, and a database-backed job transport with no extra service (S25, S26, S27).
- Its typed component model may suit a long-lived codebase with a strict domain model.

Reasons not to pick it: no first-party admin, and the owner would be learning a stack without TypeScript in it. The Symfony login-link caution applies to magic links in any stack; see section 12.

Close behind: ASP.NET Core (70.0) and Go (69.0). Go suits an owner who values minimal dependencies and a single binary more than first-party features, and accepts building the admin, magic-link flow and job runner. That is a larger one-person build than the verified facts for Django and Symfony suggest.

If the owner decides that TypeScript should dominate, the strongest direction is not a TypeScript framework. It is minimal TypeScript (section 6.13, 68.8): Node.js LTS with TypeScript source, Fastify and its first-party plugins for cookies, sessions, CSRF, headers and rate limits, Eta for auto-escaped templates, SimpleWebAuthn for admin, Kysely and pg for PostgreSQL, TypeBox for schemas, and FormatJS for messages. One TypeBox schema can serve as the archive JSON Schema, the request validator and the TypeScript type. That is the strongest archive fit in the matrix. Its costs are a hand-built moderation console, about 100 packages across many independent maintainers, and security that depends on composing those libraries correctly. Among frameworks, SvelteKit with Drizzle and Paraglide (62.4) is the strongest TypeScript option.

## 12. Risks

- Single operator: the decision is a one-person bet on a framework. Mitigation: the archive specification and exporter come first (ADR 0006), and an ADR records the choice so it can be superseded.
- Magic-link library maintenance (Django and Laravel options): the community packages are of uneven and partly unverified maintenance. Mitigation: pick one only after checking its last release, open issues and tests; keep the token logic thin and tested.
- Django Tasks framework has no worker: adopting the new API without a backend gives no background execution. Mitigation: use management commands and systemd timers, or a verified third-party database backend, not the built-in backends in production.
- Rate limiting: no first-party rate limiter was found in the Django pages read; a proxy-level and database-counter approach is needed (ADR 0003 point 4).
- Security support windows: Rails 8.0 security support has already ended (7 November 2026), and Rails 8.1 is security-only until 10 October 2027 [S12]. Symfony 6.4 bug fixes end in November 2026 [S24]. Upgrade windows are short for some candidates; the owner must schedule these.
- Ended support already: .NET 8 and .NET 9 reached end of support on 10 November 2026 [S32]. PostgreSQL 14's final release is 12 November 2026 [S41]. These are not choices against the candidates, but they show how quickly versions expire.
- PostgreSQL operations: one more service to back up, patch and restore. Mitigation: documented runbook, tested restores (plan 30).
- Supply chain: all candidates depend on large package ecosystems (PyPI, Composer, npm, Hex, NuGet, Go modules). Mitigation: lock files, reviewed updates, minimal dependency set, and a dependency list in the runbook.
- ALTCHA: the widget is MIT [S51], but the server component is ALTCHA Sentinel or a custom server. The Sentinel licence was not stated on the pages read; server libraries exist for Python, Go, PHP, Elixir and .NET [S51]. The licence of each library was not verified. If the owner wants a Python-side verifier, its licence and maintenance must be checked.
- Disposable-email blocklist: CC0 [S52], community-maintained, with no guarantee of completeness. ADR 0003 already puts it on the recurring duties list.
- Symfony login-link caveat: the docs say login links are less secure than password login and not recommended for security-critical applications [S25]. This caveat applies to magic links in every stack, not to Symfony's implementation specifically; ADR 0003 accepts it for contributors, and the [threat model](../specs/threat-model.md) (sections 3.1, 3.2) mitigates it with a confirmation POST and a phishing-resistant second factor for admin. It should not count against Symfony relative to the others.
- Governance records are dated for some candidates. Symfony's company structure is from a 2018 source [S30]. Rails Foundation details come from search results [S59]. These need refreshing before any final decision.
- Verification gaps: several facts in sections 6.4 to 6.9 are marked not verified. They must be checked before a final decision.

## 13. Questions for the owner

1. Do you accept Python (Django) as the application language, given that you are comfortable with TypeScript?
2. Do you confirm PostgreSQL 18 (not 14, which reaches its final release on 12 November 2026) or do you want SQLite with the French-stemming loss?
3. Django 5.2 LTS (supported to April 2028) or wait for Django 6.2 LTS (planned April 2027)? Which should the first deployment target?
4. Should background work use systemd timers with management commands only, or a database-backed package for Django? The first option has no extra dependency.
5. Which magic-link library, if any, is acceptable? What maintenance threshold do you require (for example a release in the last 12 months, and an open security contact)?
6. Do you accept the admin being Django's own admin on a restricted path? It is designed for internal use, which matches moderation.
7. Context pages: markdown in the repository rendered by the app, or a CMS such as Wagtail? The default here is the former.
8. Which reverse proxy do you want (Caddy or nginx)? Not evaluated here.
9. ALTCHA: self-host the Sentinel component, or a custom verifier? Which licence is acceptable if Sentinel's licence is not MIT?
10. Testimonies in any language: is it acceptable that languages without a PostgreSQL search configuration use the "simple" configuration (no stemming)?
11. Do you want the archive specification (issue #13) to be written before the framework is scaffolded? This document recommends yes.
12. Is the Symfony login-link caveat acceptable if Symfony is chosen?
13. Should security be a non-compensatory floor, so that a candidate scoring below 3 is excluded however well it does elsewhere (section 7.3)?
14. Do you accept the revised criteria and weights of section 4.3?
15. If TypeScript should dominate, is minimal TypeScript (section 6.13) acceptable, given its hand-built admin and its reliance on several single-maintainer libraries without published security policies?

## 14. Sources

Numbered sources. "Fetched" means the page was read in this pass through a fetch tool, and the stated facts are the ones the summaries returned. "Search result" means only the search snippet or listing was read.

- [S1] <https://www.djangoproject.com/download/> - fetched. Django supported series and end-of-support dates; 6.2 LTS roadmap. Release dates not shown on this page.
- [S2] <https://endoflife.date/django> - fetched. Django release dates and EOL dates.
- [S3] <https://www.djangoproject.com/weblog/2025/dec/03/django-60-released/> - fetched. Django 6.0 release, built-in tasks framework, CSP support.
- [S4] <https://docs.djangoproject.com/en/6.0/topics/tasks/> - fetched. Tasks framework has no worker; development and testing backends only.
- [S5] <https://docs.djangoproject.com/en/6.0/topics/i18n/translation/> - fetched. gettext, makemessages, compilemessages, ngettext, i18n_patterns, LocaleMiddleware, LANGUAGES.
- [S6] <https://docs.djangoproject.com/en/6.0/ref/contrib/admin/> - fetched. Admin scope and features; page truncated, LogEntry details not read.
- [S7] <https://docs.djangoproject.com/en/6.0/ref/contrib/postgres/search/> - fetched. PostgreSQL full-text search, config parameter, GeneratedField, trigram.
- [S8] <https://docs.djangoproject.com/en/6.0/internals/security/> and <https://docs.djangoproject.com/en/dev/internals/security/> - fetched. Django security policy. The fetched page included text addressed to AI tools; it was ignored and is not relied on.
- [S9] <https://www.djangoproject.com/foundation/> - fetched. Django Software Foundation as a nonprofit with a board.
- [S10] <https://pypi.org/project/django-magiclink/> ; <https://github.com/betagouv/django-magicauth> ; <https://github.com/wejhink/django-magic-link> - search results only. Magic-link packages; maintenance not verified.
- [S11] <https://endoflife.date/rails> - fetched. Rails release dates, EOL, latest patches.
- [S12] <https://rubyonrails.org/maintenance> - fetched. Rails support table and policy (1 year bug fixes, 2 years security per minor).
- [S13] <https://rubyonrails.org/2024/11/7/rails-8-no-paas-required> - fetched. Rails 8.0 release, Solid Queue, Solid Cable, Kamal 2, authentication generator.
- [S14] <https://guides.rubyonrails.org/security.html> - fetched (first 100,000 characters). Authentication generator (password-based), rate_limit, CSRF default.
- [S15] <https://rubyonrails.org/security> - fetched. Rails security reporting and disclosure process.
- [S16] <https://endoflife.date/php> - fetched. PHP branch support dates.
- [S17] <https://laravel.com/docs/releases> - fetched. Laravel support table, Laravel 13 release, support policy, product list (Nova).
- [S18] <https://laravel.com/docs/13.x/localization> - fetched. Laravel translation files, pluralization.
- [S19] <https://laravel.com/docs/13.x/queues> - fetched (first 100,000 characters). Queue drivers and queue:work.
- [S20] <https://github.com/laravel/framework/security/policy> - fetched. Laravel security contact.
- [S21] <https://laravel.com/docs/13.x/license> - search result only. MIT licence and copyright holder.
- [S22] <https://packagist.org/packages/harrisonclewis/laravel-passwordless> ; <https://github.com/SpykApp/passwordless-login> - search results only. Laravel magic-link packages.
- [S23] <https://github.com/filamentphp/filament/releases> - fetched. Filament 5.11.3.
- [S24] <https://symfony.com/releases> - fetched. Symfony release and support table; "Today" on the page read as November 15, 2026.
- [S25] <https://symfony.com/doc/current/security/login_link.html> - fetched. Login links, expiry, max_uses, warnings.
- [S26] <https://symfony.com/doc/current/translation.html> - fetched. XLIFF, ICU MessageFormat, _locale routing.
- [S27] <https://symfony.com/doc/current/messenger.html> - fetched (first 100,000 characters). Doctrine transport and messenger:consume.
- [S28] <https://symfony.com/doc/current/contributing/code/security.html> - fetched. Symfony security reporting and classification.
- [S29] <https://github.com/EasyCorp/EasyAdminBundle/releases> - fetched. EasyAdmin 5.10.1.
- [S30] <https://symfony.com/blog/a-business-model-for-symfony> - search result only (2018 post). Symfony SAS and SensioLabs; dated.
- [S31] <https://learn.microsoft.com/en-us/dotnet/core/releases-and-support> - fetched. .NET supported versions, LTS and STS windows, servicing.
- [S32] <https://endoflife.date/dotnet> - fetched. .NET release and EOL table.
- [S33] <https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity> - fetched (first 100,000 characters). No passwordless or magic-link terms found in the fetched text.
- [S34] <https://endoflife.date/go> - fetched. Go release dates and support rule.
- [S35] <https://go.dev/security/policy> - fetched. Go security reporting, versions receiving fixes, 90-day commitment.
- [S36] <https://go.dev/doc/go1.25> - fetched. net/http CrossOriginProtection.
- [S37] <https://go.dev/doc/go1.22> - fetched. net/http.ServeMux patterns.
- [S38] <https://pkg.go.dev/golang.org/x/text/message> - fetched. Localized formatting and catalogs; v0.44.0 shown.
- [S39] <https://github.com/alexedwards/scs> - fetched. MIT, stability statement, backend policy.
- [S40] <https://riverqueue.com/> - fetched. River background jobs on PostgreSQL; vendor and Pro licence link.
- [S41] <https://www.postgresql.org/support/versioning/> - fetched. PostgreSQL major versions, final release dates, 19 RC.
- [S42] <https://www.postgresql.org/docs/current/textsearch-dictionaries.html#TEXTSEARCH-SNOWBALL-DICTIONARY> - fetched. Snowball stemmers for many languages; French not confirmed on the page.
- [S43] <https://sqlite.org/fts5.html> - fetched (first 100,000 characters). FTS5 tokenizers; porter English only.
- [S44] <https://endoflife.date/nodejs> - fetched. Node release lines.
- [S45] <https://endoflife.date/python> - fetched. Python 3.12 EOL.
- [S46] <https://github.com/withastro/astro/releases> ; <https://docs.astro.build/en/guides/internationalization/> - fetched. Astro version and i18n routing.
- [S47] <https://github.com/sveltejs/kit/releases> ; <https://svelte.dev/docs/kit/form-actions> - fetched. SvelteKit release; form actions and progressive enhancement.
- [S48] <https://paraglidejs.com/> - fetched. Paraglide JS v2, MIT, plurals and URL localization.
- [S49] <https://github.com/drizzle-team/drizzle-orm/releases> - fetched. Drizzle stable and pre-release tags.
- [S50] <https://docs.adonisjs.com/guides/digging-deeper/i18n> ; <https://docs.adonisjs.com/guides/auth/introduction> ; <https://github.com/adonisjs/core/releases> - fetched. AdonisJS i18n, auth guards, release listing.
- [S51] <https://github.com/altcha-org/altcha> ; <https://altcha.org/> - fetched. ALTCHA widget MIT; Sentinel and server libraries.
- [S52] <https://github.com/disposable-email-domains/disposable-email-domains> - fetched. CC0 licence and maintenance model.
- [S53] <https://gettext.hexdocs.pm/Gettext.html> - fetched. Gettext for Elixir v1.0.2.
- [S54] <https://phoenix.hexdocs.pm/Mix.Tasks.Phx.Gen.Auth.html> ; <https://phoenix.hexdocs.pm/overview.html> - fetched. Phoenix v1.8.16 docs; phx.gen.auth email-based authentication.
- [S55] <https://phoenix.hexdocs.pm/installation.html> - fetched. Elixir 1.17 and Erlang 25 requirement.
- [S56] <https://github.com/phoenixframework/phoenix> - fetched. MIT licence.
- [S57] <https://endoflife.date/wagtail> - fetched. Wagtail release and support table.
- [S58] <https://github.com/thoughtbot/administrate> - fetched. Maintenance statement; no release date visible.
- [S59] <https://rubyonrails.org/foundation> ; <https://rubyonrails.org/foundation/37signals> - search results only. Rails Foundation governance; not verified on the pages.
- [S60] <https://wp-umbrella.com/blog/wordpress-7-0-release-status-and-timeline/> and <https://atlasum.net/blog/wordpress-7-1-4-security-release> - search result summaries, 2026-11-15. WordPress 7.0, 7.1 and 7.1.4 release dates; 7.2 plan.
- [S61] <https://make.wordpress.org/hosting/handbook/compatibility/version/7-0/> - search result summary. PHP and database requirements for 7.0.
- [S62] <https://make.wordpress.org/security/> - search result summary. "Only the latest version" support policy, courtesy backports, end of 4.1-4.6 updates.
- [S63] <https://patchstack.com/whitepaper/state-of-wordpress-security-in-2024/> and <https://patchstack.com/whitepaper/state-of-wordpress-security-in-2025/> - search result summaries. Plugin, theme and core vulnerability shares.
- [S64] <https://wp-content.co/patchstack-wordpress-security-report-2026-vulnerabilities-rises-hosting-defenses-struggles/> - secondary coverage of Patchstack's 2026 report.
- [S65] <https://techcrunch.com/2026/02/12/automattic-planned-to-target-10-competitors-with-royalty-fees-wp-engine-claims-in-new-filing/> and <https://www.therepository.email/wp-engines-antitrust-claims-against-automattic-are-back-on-after-judge-reverses-earlier-dismissal> - secondary. WP Engine v. Automattic status and the September 2026 ruling.
- [S66] <https://nextjs.org/support-policy> - cited through search result summaries, 2026-11-15; release and end-of-support dates from third-party summaries (endoflife.ai, digitalapplied.com, creuto.com).
- [S67] <https://github.com/vercel/next.js/security/advisories/GHSA-9qr9-h5gf-34mp> ; <https://projectdiscovery.io/blog/nextjs-middleware-authorization-bypass> ; <https://threatdefence.com/article/react-server-components-rce-ghsa-xqc2-xf4c-x3h3-patching-hunting> - search result summaries. CVE-2025-29927, CVE-2025-55182 and the October 2026 Server Components fix.
- [S68] <https://www.reactsquad.io/blog/nextjs-16-2-adapter-api> ; <https://github.com/vercel/next.js/discussions/77740> - search result summaries. Adapter API, self-hosting parity, Node and TypeScript requirements.
- [S69] <https://www.better-auth.com/blog/authjs-joins-better-auth> ; <https://startwithidentity.com/vendors/open-source/authjs/> - search result summaries. Auth.js maintenance status; the Vercel acquisition of Better Auth is from secondary sources only.
- [S70] <https://vercel.com/security> ; <https://vercel.com/legal/dpa> ; <https://www.dataprivacyframework.gov/participant/6847> - search result summaries. DPF certification, DPA processing locations, EU regions caching only.
- [S71] <https://nodejs.org/en/about/previous-releases> - fetched 2026-11-15. Node.js release lines, LTS length, annual cycle from Node.js 27.
- [S72] <https://nodejs.org/api/sqlite.html> - fetched 2026-11-15 (documentation for v26.13.1). `node:sqlite` stability and extension loading.
- [S73] <https://github.com/nodejs/node/issues/56951> ; <https://github.com/openclaw/openclaw/issues/20987> - search results only. Reports of FTS5 missing in some Node builds.
- [S74] <https://nodejs.org/api/typescript.html> - fetched 2026-11-15. Type stripping stability and limits.
- [S75] <https://devblogs.microsoft.com/typescript/progress-on-typescript-7-december-2025/> - search result summary. JSDoc support rewritten; `@enum` and `@constructor` not recognized.
- [S76] <https://typescriptdocs.com/release-notes/TypeScript%207.0> - search result summary. TypeScript 7 release timeline and removed JSDoc behaviours.
- Local test, 2026-11-15: Node v26.13.0 with SQLite 3.54.0; FTS5 tokenizers, diacritics folding, absence of French stemming, `secure_delete` default.
- [S77] npm registry (<https://registry.npmjs.org/>) and GitHub REST API, queried 2026-11-15: latest versions, licences, direct dependency counts, repository activity and the presence of `SECURITY.md` (including the Fastify organization's default community-health repository). A scratch install of the section 6.13 library set with pnpm 12.18.0, lifecycle scripts disabled, gave the package count and licence list.
- [S78] <https://fastify.dev/docs/latest/Reference/LTS/> - fetched 2026-11-15. LTS policy and OpenJS Foundation At-Large status. <https://github.com/fastify/fastify> - search result: README notes that the main branch targets v6.
- [S79] <https://eta.js.org/docs/4.x.x/api/configuration> - fetched 2026-11-15. `autoEscape` default true.
- Repository documents: docs/plans/main.md; docs/decisions/0002-single-eu-vps.md; 0003-email-magic-link-auth.md; 0006-archive-first-replaceable-application.md; 0007-privacy-review-path.md; docs/research/domain-and-persistence.md; docs/constitution/archival-model.md; AGENTS.md.

Not verified in this pass (listed so they are not mistaken for facts): Django deprecation policy and upgrade history; Django rate limiting; Django admin change-history storage; Python minimum for Django 6.x; Phoenix governance and security policy; Oban and Ecto full-text search; Laravel scheduler; Laravel and Rails i18n URL handling; ASP.NET localization and jobs; Go html/template, pgx and migration tools; AdonisJS Node requirement, Lucid, jobs and governance; SvelteKit magic-link and job libraries; Drizzle full-text search; Symfony full-text search; the licences of altcha-lib packages and the Sentinel server; Rails Foundation structure; Symfony governance today.
