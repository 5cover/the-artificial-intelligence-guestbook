# Stack RFP: choosing the application framework for The Artificial Intelligence Guestbook

Status: Proposal - awaiting owner decision

Date: 2026-11-15

Issues: #6 (stack RFP) and #7 (application stack decision)

Related: [plan](../plans/main.md), [ADR 0002](../decisions/0002-single-eu-vps.md), [ADR 0003](../decisions/0003-email-magic-link-auth.md), [ADR 0006](../decisions/0006-archive-first-replaceable-application.md), [ADR 0007](../decisions/0007-privacy-review-path.md)

Source tags such as [S12] refer to the numbered list in the Sources section. Anything not verified in this pass is labelled "not verified". Scores are judgements, not measurements.

## 1. Summary

The owner asked for a comparison of application stacks, not a build. The short version:

- Django (Python, with PostgreSQL 18) scores highest on the weighted criteria, mainly because of its first-party admin, its gettext-based i18n, its PostgreSQL full-text search with French and English configurations, a clear foundation governance model and a security policy that was verified. Its weak points are the lack of a first-party magic-link flow, no production worker for its new Tasks framework, and no first-party rate limiter found in this pass.
- Symfony 7.4 LTS (PHP) is the runner-up. It has the longest verified LTS window of the candidates, a first-party login-link (magic link) feature, strong XLIFF and ICU translation support and a Doctrine-backed job transport. It has no first-party admin and it is a PHP stack the owner does not have installed.
- The strongest TypeScript option is SvelteKit with Drizzle and Paraglide. It is the best fit for no-JavaScript forms and for localized URLs, but it leaves admin, magic-link auth and background jobs to the operator. AdonisJS was evaluated but its first-party docs did not show magic-link auth and several details could not be verified.
- Architecture is largely independent of the winner. ADR 0006 makes the archive format the primary artefact, so the framework choice is less consequential than usual. This document recommends the archive specification (issue #13) be written before the application scaffold.

## 2. Context and decided constraints

These are owner decisions already recorded in the repository or stated for this RFP. They are not reopened here.

- The archive is the primary deliverable. The web application is replaceable. The canonical archive format (structured records, plain text, manifests, checksums, schema documentation) is specified independently of the app. The app database is an operational store that exports to that format ([ADR 0006](../decisions/0006-archive-first-replaceable-application.md), [plan section 23](../plans/main.md)).
- Lessons from a "static public site plus small API" design may be borrowed (for example cacheable, pre-rendered HTML for published testimonies and static HTML in editions) without adopting that architecture ([ADR 0006](../decisions/0006-archive-first-replaceable-application.md)).
- Hosting: one self-managed EU VPS (Hetzner, OVHcloud, Scaleway class). The stack must run comfortably on a small VPS with modest memory ([ADR 0002](../decisions/0002-single-eu-vps.md)).
- Authentication: email magic links only, no passwords and no OAuth for now. Defences in layers: disposable-email blocklist, MX check, per-account pending caps, global intake throttling, a self-hosted proof-of-work challenge, rate limits, and rel="ugc nofollow" on outbound links ([ADR 0003](../decisions/0003-email-magic-link-auth.md)).
- Database: PostgreSQL is the presumptive choice for full-text search in French and English. A challenge to it is required (section 6).
- One operator, for decades. Successor-friendliness, low dependency churn and low supply-chain surface matter ([plan section 28 and 29](../plans/main.md)).
- Server-rendered, accessible HTML that works without JavaScript is preferred. French and English are first-class interface languages, and testimonies may be in any language ([plan sections 8 and 27](../plans/main.md)).
- The operator's machine is Windows 11 with Node 26, pnpm and Python 3.12. Docker is not installed and PHP is not installed. The owner is comfortable with TypeScript. This is noted in section 10 and deliberately kept out of the scoring matrix.
- Git: this document is not committed. The owner asked for no commit in this pass.

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

## 4. Criteria and weights

Weights sum to 100. They reflect the plan and the ADRs. Each criterion is scored 1 to 5 (5 is best) in section 7.

| # | Criterion | Weight | Why this weight |
| --- | --- | --- | --- |
| 1 | Longevity: governance, release cadence, support windows | 11 | The plan is for decades and a successor must inherit the stack ([plan 28, 29](../plans/main.md)). |
| 2 | Upgrade burden over 10+ years | 9 | Every forced major or minor upgrade is recurring custodial work ([plan 28](../plans/main.md)). |
| 3 | Built-in or first-party admin for one-person moderation | 8 | Moderation, redaction, privacy requests and translations are routine duties ([plan 24](../plans/main.md)). |
| 4 | i18n and l10n maturity | 8 | FR and EN are first-class and testimonies may be in any language ([plan 8](../plans/main.md)). |
| 5 | Magic-link auth ecosystem (library maintenance, sessions, CSRF, rate limits) | 7 | Owner decision ([ADR 0003](../decisions/0003-email-magic-link-auth.md)), but libraries can be swapped. |
| 6 | Forms, server-side validation, accessible no-JS rendering | 7 | Accessibility and no-JS are explicit ([plan 27](../plans/main.md)). Important, but most stacks can do it. |
| 7 | PostgreSQL integration (ORM, migrations, full-text search) | 6 | PostgreSQL is presumptive; search quality matters ([plan 13](../plans/main.md)). |
| 8 | Security defaults and security-release process | 9 | Unpublished testimony, auth identifiers and privacy requests are held ([plan 26](../plans/main.md)). |
| 9 | Background jobs and scheduled tasks without extra infrastructure | 5 | Exports, email and backups run on one VPS ([ADR 0002](../decisions/0002-single-eu-vps.md)). |
| 10 | Deployment and operations on one VPS (runtime upgrades, memory, process model) | 6 | ADR 0002 requires a small VPS to run it comfortably. |
| 11 | Successor-friendliness: talent pool and documentation | 6 | Explicit in plan section 29. |
| 12 | Dependency footprint and supply-chain exposure | 5 | Low churn and low supply-chain surface are owner requirements. |
| 13 | Testing | 3 | Important, but every candidate has a mature test story. |
| 14 | Fit with the archive-first principle (domain model and export kept clean) | 10 | ADR 0006 makes the export the primary product; this is the criterion the owner cares about most. |

Justification in short: the highest weights go to longevity (11) and archive fit (10), which determine whether the archive outlives the operator's attention, followed by upgrade burden and security (9 each). Admin and i18n come next (8 each) because they are daily or near-daily tasks. Operations, jobs and testing are real but cheaper to change later.

## 5. Database choice: PostgreSQL, and the challenge to it

PostgreSQL is presumed. The challenge was asked for, so the tradeoff is stated here.

- The case for SQLite: one file, no database server, simple backup with its online backup mechanism, no extra service to patch, and enough capacity for a small archive. Its operational simplicity is real and would suit a successor.
- The case against SQLite for this project is specific. SQLite's FTS5 ships the unicode61 tokenizer (the default), an ascii tokenizer, a porter tokenizer and a trigram tokenizer. The porter stemmer is documented as designed for English only, and the document does not describe a French stemmer [S43]. French search would therefore be accent-folded and unstemmed, which is a real loss for a bilingual archive.
- The case for PostgreSQL: Snowball stemmers are documented for many languages [S42]; Django's own documentation uses config="french" in its search examples [S7], so PostgreSQL search configurations per testimony language are a practical option. PostgreSQL also gives row-level concurrency, LISTEN/NOTIFY and SKIP LOCKED for a job table. Rails' Solid Queue uses PostgreSQL's SKIP LOCKED [S13], and River runs on PostgreSQL [S40].
- Costs of PostgreSQL: one more service to install, patch and back up on the VPS; on the owner's Windows machine without Docker, a native PostgreSQL install (or WSL) is needed for local development. This is a real cost and is recorded as a risk.
- Version: PostgreSQL 18 is the current major (18.7 on the versioning page). PostgreSQL 14's final release is 12 November 2026, three days before this document's date, so a new deployment should not start on 14 [S41]. PostgreSQL 19 is at release-candidate stage and is not supported yet [S41].

Recommendation for this section: keep PostgreSQL 18. Keep SQLite as a documented fallback only if the owner decides that the one-server simplicity outweighs French stemming. No candidate argued for SQLite in this pass.

## 6. Candidates: verified facts, strengths and weaknesses

Each candidate section lists facts that were checked in this pass with source tags, then strengths, then weaknesses. Items marked "not verified" were not checked and must be checked before any commitment.

### 6.1 Django (Python)

Verified facts:

- Supported series on the download page: 5.2 LTS (mainstream support ended 3 December 2025, extended support to April 2028); 6.0 (mainstream to 4 August 2026, extended to April 2027); 6.1 (mainstream to April 2027, extended to December 2027). Django 6.2 is listed as the next LTS with a planned release in April 2027 [S1].
- Release dates from the endoflife cross-check: 6.0 on 3 December 2025, 6.1 on 5 August 2026, latest 6.1.3 on 3 November 2026; 5.2 LTS EOL 30 April 2028 [S2][S3].
- Django 6.0 ships a built-in Tasks framework and built-in Content Security Policy support [S3].
- The Tasks framework has no worker. Its built-in backends (ImmediateBackend and DummyBackend) are for development and testing only. Production needs a third-party backend with a worker process [S4].
- Admin: documented as recommended for an organization's internal management tool. Provides list filters, search, bulk actions, list_editable, and per-model permission hooks (has_view, has_change, has_delete and so on) [S6].
- i18n: gettext PO and MO files, makemessages and compilemessages, ngettext for plurals, i18n_patterns for locale-prefixed URLs, LocaleMiddleware and the LANGUAGES setting [S5]. The page does not describe the html lang attribute; it is normally set in the base template (not verified in docs).
- PostgreSQL search: SearchVector, SearchQuery, SearchRank, SearchHeadline, a config parameter per field (for example 'french'), GeneratedField maintained by PostgreSQL, and trigram similarity via pg_trgm [S7].
- Security policy: the two most recent release series and LTS releases receive security support. Reports go to security@djangoproject.com, acknowledgement within 3 working days, target resolution 90 days. Distributors get advance notice under embargo [S8].
- Foundation: the Django Software Foundation is a nonprofit with an elected board [S9].
- Magic-link packages (search results only, maintenance not verified): django-magiclink (PyPI shows 1.3.0) [S10]; django-magicauth from betagouv, version 1.0.2, which adds a second check via django-otp [S10]; django-magic-link appears to be unmaintained (metadata suggests about ten years old) [S10].
- Not verified: Django's deprecation policy and typical upgrade effort; Python minimum for Django 6.x; a first-party rate limiter (none was found in the pages read); the admin's change-history storage details.

Strengths:

- The strongest first-party admin of all candidates for one-person moderation work (R10).
- Mature gettext workflow with plurals and locale-prefixed URLs (R13). Translators can use standard PO tooling.
- PostgreSQL-native search with per-language configurations and maintained search columns, which makes deletion propagate to the search index automatically if the index is a generated column (R11).
- Server-rendered forms and templates by default, with no JavaScript needed for the core flow (R14).
- Foundation governance and a published, specific security process (R20).
- Large talent pool and documentation quality. Python 3.12 is already on the owner's machine. Python 3.12 is supported until 31 October 2028 [S45].

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
- Security: report to security@symfony.com; login throttling bypasses and similar hardening items are handled as regular bug fixes rather than security issues; patches go to all maintained versions [S28].
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
- PHP is not installed on the owner's machine. The owner is comfortable with TypeScript, not PHP.
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
- Security policy: security@laravel.com; no response timeline stated [S20].
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
- PHP is not installed on the owner's machine.

### 6.4 Ruby on Rails

Verified facts:

- Rails 8.1 was released 22 October 2025 [S11]. Bug fixes for 8.1.x ended 10 October 2026, and security fixes run to 10 October 2027 [S12]. Rails 8.0.x security fixes ended 7 November 2026, eight days before this document's date [S12]. Endoflife lists 8.1.4.1 and 8.0.5.2 as released 3 November 2026 [S11].
- Policy: each minor release gets one year of bug fixes and two years of security fixes [S12].
- Rails 8.0 was released 7 November 2024 [S13].
- Rails 8 ships a built-in authentication generator for password-based sign-in and password reset [S13][S14]. Magic-link sign-in is not part of the generator (the security guide describes passwords only) [S14].
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

- Phoenix documentation for v1.8.16 [S54][S55].
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

- .NET 10 is LTS, released November 2025, supported until November 2028 [S31][S32].
- .NET 11 is STS, released November 2026, supported until November 2028 [S31].
- .NET 8 and .NET 9 reached end of support on 10 November 2026 [S32]. Microsoft's support page lists only .NET 10 and 11 as currently supported [S31].
- Servicing updates ship monthly; security fixes ship on patch Tuesday [S31].
- The ASP.NET Core Identity introduction page, as fetched, does not describe passwordless or magic-link sign-in [S33].
- Not verified in this pass: localization (resx and IStringLocalizer), admin tooling, durable background-job options (Hangfire or others), and Npgsql full-text search support. General knowledge says there is no first-party admin UI.

Strengths:

- Long LTS windows and monthly security servicing.
- Strong typing and tooling; a large enterprise talent pool.
- Runs on Linux on a VPS, although the owner's tools are Windows-first.

Weaknesses:

- No first-party magic-link flow found; a third-party library or custom code would be needed.
- No first-party admin.
- The .NET LTS cadence is a three-year window; the owner would need to track two-year STS releases if they wanted them, though LTS-only is an option.
- Ecosystem and dependency footprint are larger than Go (judgement).

### 6.7 Go (standard library plus minimal libraries)

Verified facts:

- Go 1.27 was released 19 August 2026, Go 1.26 on 10 February 2026, and Go 1.25 reaches end of life on 19 August 2026 [S34]. The policy is that each major release is supported until two newer major releases exist [S34].
- Security: report to security@golang.org; fixes go to the two most recent major releases and the head of the repository; the stated commitment is that issues are fixed or made public within 90 days of acknowledgement [S35].
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
- Astro (considered, see 6.10): i18n routing verified, no message catalogs or pluralization on the routing page [S46].
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

### 6.10 Astro (considered, not a primary candidate)

- Astro's current major is 7 (astro@7.4.12 on 13 November in the GitHub releases page) [S46].
- Built-in i18n routing: locale folders, prefixDefaultLocale, fallback and domain mapping [S46]. No message catalogs or pluralization are covered on that page [S46].
- Astro is an excellent static-HTML generator. It fits the "static HTML for published testimonies and editions" idea (ADR 0006) well, but a dynamic app (magic links, admin, moderation queue) is not its centre of gravity. It is noted as a possible companion for Context and editions, not as the application.

### 6.11 CMS-on-framework options for Context pages (optional, not mandatory)

- Wagtail (on Django): Wagtail 7.4 is LTS (released 4 May 2026) with security support until 2 November 2027; Wagtail 8.1 was released 2 November 2026 [S57]. A page-tree CMS would add an editor UI for Context pages. The cost is another dependency stream and another upgrade stream. Judgement: markdown files in the repository, rendered by the app, are simpler and more archive-friendly. Not required.
- Filament (on Laravel): 5.11.3 active (13 November) [S23]. Relevant only if Laravel were chosen.
- EasyAdmin (on Symfony): 5.10.1 active (14 November) [S29]. Relevant only if Symfony were chosen.
- Statamic: not evaluated.

## 7. Scoring matrix

Scores are 1 to 5 (5 best). They are judgements based on the verified facts above and on general experience where marked "not verified". Weighted total = sum of (score times weight) divided by 5, so the maximum is 100.

| # | Criterion | Weight | Django | Symfony 7.4 | Go | ASP.NET Core | Rails 8.1 | Laravel 13 | Phoenix | SvelteKit | AdonisJS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Longevity | 11 | 5 | 4 | 4 | 4 | 3 | 3 | 3 | 3 | 2 |
| 2 | Upgrade burden | 9 | 4 | 4 | 5 | 3 | 2 | 3 | 3 | 2 | 3 |
| 3 | Admin | 8 | 5 | 3 | 1 | 2 | 2 | 3 | 2 | 1 | 2 |
| 4 | i18n | 8 | 5 | 5 | 3 | 4 | 3 | 3 | 4 | 4 | 4 |
| 5 | Magic-link ecosystem | 7 | 3 | 4 | 2 | 2 | 3 | 3 | 4 | 2 | 2 |
| 6 | Forms and no-JS | 7 | 5 | 4 | 4 | 4 | 4 | 4 | 3 | 5 | 3 |
| 7 | PostgreSQL integration | 6 | 5 | 3 | 3 | 4 | 4 | 3 | 4 | 3 | 3 |
| 8 | Security defaults and process | 9 | 5 | 4 | 4 | 4 | 4 | 3 | 3 | 3 | 3 |
| 9 | Jobs without extra infra | 5 | 3 | 5 | 3 | 3 | 5 | 4 | 3 | 2 | 2 |
| 10 | Operations on one VPS | 6 | 4 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 4 |
| 11 | Successor-friendliness | 6 | 5 | 4 | 3 | 3 | 4 | 4 | 2 | 3 | 3 |
| 12 | Dependency footprint | 5 | 4 | 3 | 5 | 3 | 3 | 3 | 4 | 2 | 2 |
| 13 | Testing | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3 |
| 14 | Archive-first fit | 10 | 4 | 4 | 4 | 4 | 3 | 3 | 3 | 4 | 3 |
| | Weighted total (out of 100) | 100 | 88.6 | 78.8 | 71.4 | 69.0 | 66.0 | 65.4 | 64.2 | 59.8 | 55.6 |

Ranking: Django (88.6), Symfony (78.8), Go (71.4), ASP.NET Core (69.0), Rails (66.0), Laravel (65.4), Phoenix (64.2), SvelteKit (59.8), AdonisJS (55.6).

Reading the matrix:

- Django's lead over Symfony comes mainly from admin (+3 points times weight 8), search and PostgreSQL integration, security process, longevity and successor-friendliness. Symfony leads on jobs and magic-link ecosystem, which are real but smaller in weight.
- Go ranks third mostly because of upgrade burden, dependency footprint and operations. It scores 1 on admin and 2 on magic links, which the one-person constraint makes expensive. A reasonable owner who values minimal dependencies more than first-party features could reasonably put Go higher.
- The scores are judgements. A score of 3 means "adequate with known gaps", not "average". The matrix does not weigh the owner's TypeScript familiarity, the local tooling on Windows, or personal taste; those are discussed in section 10.
- No formal sensitivity analysis was run. Django leads Symfony by 9.8 points, and the lead depends mostly on the admin, PostgreSQL and security weights. Treat the order from third place down as unstable; it is within the range that different judgements could move.

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

## 10. Owner context (noted, not scored)

- Windows 11, no Docker, no PHP. A local PostgreSQL install (native installer or WSL) is needed for every Postgres-backed option. SQLite would avoid that. This is recorded as a real cost of PostgreSQL.
- Python 3.12 is already installed; Django's development loop works natively on Windows. Python 3.12 is supported until 31 October 2028 [S45].
- Node 26 is installed. Node 26 is the current LTS line, released 5 May 2026, with active LTS support until 27 October 2027 and maintenance support until 30 April 2029 [S44]. This matters only for the TypeScript options.
- The owner is comfortable with TypeScript. If that comfort is weighted heavily, SvelteKit (with its assembly cost) becomes the best TypeScript choice. Under the current weights it does not overturn Django's lead. This should be the owner's explicit decision.
- Because ADR 0006 makes the archive the primary deliverable, a later move between stacks is less costly than usual if the archive specification and exporter are done first. This is the strongest argument for making a provisional choice now and recording it as an ADR that can be superseded.

## 11. Recommendation

Top recommendation: Django 6.x (or Django 5.2 LTS if the owner prefers the longer already-published LTS window to April 2028), with PostgreSQL 18.

Why:

- It scores highest on the criteria that matter most under this plan: longevity, archive fit, security, admin and i18n.
- Django's admin provides the one-person moderation surface with no extra product (R10).
- gettext plus i18n_patterns is a mature FR and EN workflow with a translator-friendly file format (R13).
- PostgreSQL search with per-language configurations can cover French and English (Django's documented examples use 'french' and 'english' [S7]; the full PostgreSQL configuration list was not verified [S42]), and a generated search column follows the row on deletion (R11, R12).
- The DSF governance, the published security policy and the release cadence were verified (S1, S8, S9; R20).
- The gaps are known and bounded: choose and audit a magic-link library; build the job runner from management commands and systemd timers (or a database-backed package); add rate limits at the proxy and in a small Postgres-backed counter; treat admin 2FA as a deliberate addition.

Upgrade plan (judgement): target 6.2 LTS when it ships (planned for April 2027 per the download page [S1]); until then use 6.1 or 5.2 LTS. Verify the 6.2 support window when released.

Runner-up: Symfony 7.4 LTS (PHP).

A reasonable owner might pick Symfony instead of Django for these reasons:

- The LTS model is the most explicit in this list, and the 7.4 security window to November 2029 is the longest verified (S24).
- Symfony has a first-party login-link feature, strong translation tooling with XLIFF and ICU, and a database-backed job transport with no extra service (S25, S26, S27).
- Its typed component model may suit a long-lived codebase with a strict domain model.

Reasons not to pick it: no first-party admin, PHP is not installed on the owner's machine, and the owner would be learning a stack without TypeScript in it. The Symfony login-link documentation also advises caution for security-critical use.

Honourable mention: Go, if the owner values minimal dependencies and a single binary more than first-party features and accepts building the admin, magic-link flow and job runner from the standard library and a few libraries. This is a larger one-person build than the verified facts for Django and Symfony suggest.

If the owner decides that TypeScript familiarity should dominate: SvelteKit with Drizzle and Paraglide is the strongest TypeScript option on the verified evidence. The cost is that admin, magic-link auth and background jobs are assembled from third-party packages, which the matrix scores against. AdonisJS is the more complete TypeScript framework, but the verified gaps (magic link, unverified job and ORM details, unassessed maintainer depth) keep it behind SvelteKit.

## 12. Risks

- Single operator: the decision is a one-person bet on a framework. Mitigation: the archive specification and exporter come first (ADR 0006), and an ADR records the choice so it can be superseded.
- Magic-link library maintenance (Django and Laravel options): the community packages are of uneven and partly unverified maintenance. Mitigation: pick one only after checking its last release, open issues and tests; keep the token logic thin and tested.
- Django Tasks framework has no worker: adopting the new API without a backend gives no background execution. Mitigation: use management commands and systemd timers, or a verified third-party database backend, not the built-in backends in production.
- Rate limiting: no first-party rate limiter was found in the Django pages read; a proxy-level and database-counter approach is needed (ADR 0003 point 4).
- Security support windows: Rails 8.0 security support has already ended (7 November 2026), and Rails 8.1 is security-only until 10 October 2027 [S12]. Symfony 6.4 bug fixes end in November 2026 [S24]. Upgrade windows are short for some candidates; the owner must schedule these.
- Ended support already: .NET 8 and .NET 9 reached end of support on 10 November 2026 [S32]. PostgreSQL 14's final release is 12 November 2026 [S41]. These are not choices against the candidates, but they show how quickly versions expire.
- PostgreSQL operations: one more service to back up, patch and restore. Mitigation: documented runbook, tested restores (plan 30).
- Local development on Windows without Docker: a native PostgreSQL install is needed (section 10).
- Supply chain: all candidates depend on large package ecosystems (PyPI, Composer, npm, Hex, NuGet, Go modules). Mitigation: lock files, reviewed updates, minimal dependency set, and a dependency list in the runbook.
- ALTCHA: the widget is MIT [S51], but the server component is ALTCHA Sentinel or a custom server. The Sentinel licence was not stated on the pages read; server libraries exist for Python, Go, PHP, Elixir and .NET [S51]. The licence of each library was not verified. If the owner wants a Python-side verifier, its licence and maintenance must be checked.
- Disposable-email blocklist: CC0 [S52], community-maintained, with no guarantee of completeness. ADR 0003 already puts it on the recurring duties list.
- Symfony login-link caveat: the docs say login links are less secure than password login and not recommended for security-critical applications [S25]. This caveat applies to magic links in every stack, not to Symfony's implementation specifically; ADR 0003 accepts it for contributors, and the [threat model](../specs/threat-model.md) (sections 3.1, 3.2) mitigates it with a confirmation POST and a phishing-resistant second factor for admin. It should not count against Symfony relative to the others.
- Governance records are dated for some candidates. Symfony's company structure is from a 2018 source [S30]. Rails Foundation details come from search results [S59]. These need refreshing before any final decision.
- Verification gaps: several facts in sections 6.4 to 6.9 are marked not verified. They must be checked before a final decision.

## 13. Questions for the owner

1. Do you accept Python (Django) as the application language, given that you are comfortable with TypeScript?
2. Do you confirm PostgreSQL 18 (not 14, which reaches its final release on 12 November 2026) and accept the local install cost on Windows, or do you want SQLite with the French-stemming loss?
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

## 14. Sources

Numbered sources. "Fetched" means the page was read in this pass through a fetch tool, and the stated facts are the ones the summaries returned. "Search result" means only the search snippet or listing was read.

- [S1] https://www.djangoproject.com/download/ - fetched. Django supported series and end-of-support dates; 6.2 LTS roadmap. Release dates not shown on this page.
- [S2] https://endoflife.date/django - fetched. Django release dates and EOL dates.
- [S3] https://www.djangoproject.com/weblog/2025/dec/03/django-60-released/ - fetched. Django 6.0 release, built-in tasks framework, CSP support.
- [S4] https://docs.djangoproject.com/en/6.0/topics/tasks/ - fetched. Tasks framework has no worker; development and testing backends only.
- [S5] https://docs.djangoproject.com/en/6.0/topics/i18n/translation/ - fetched. gettext, makemessages, compilemessages, ngettext, i18n_patterns, LocaleMiddleware, LANGUAGES.
- [S6] https://docs.djangoproject.com/en/6.0/ref/contrib/admin/ - fetched. Admin scope and features; page truncated, LogEntry details not read.
- [S7] https://docs.djangoproject.com/en/6.0/ref/contrib/postgres/search/ - fetched. PostgreSQL full-text search, config parameter, GeneratedField, trigram.
- [S8] https://docs.djangoproject.com/en/6.0/internals/security/ and https://docs.djangoproject.com/en/dev/internals/security/ - fetched. Django security policy. The fetched page included text addressed to AI tools; it was ignored and is not relied on.
- [S9] https://www.djangoproject.com/foundation/ - fetched. Django Software Foundation as a nonprofit with a board.
- [S10] https://pypi.org/project/django-magiclink/ ; https://github.com/betagouv/django-magicauth ; https://github.com/wejhink/django-magic-link - search results only. Magic-link packages; maintenance not verified.
- [S11] https://endoflife.date/rails - fetched. Rails release dates, EOL, latest patches.
- [S12] https://rubyonrails.org/maintenance - fetched. Rails support table and policy (1 year bug fixes, 2 years security per minor).
- [S13] https://rubyonrails.org/2024/11/7/rails-8-no-paas-required - fetched. Rails 8.0 release, Solid Queue, Solid Cable, Kamal 2, authentication generator.
- [S14] https://guides.rubyonrails.org/security.html - fetched (first 100,000 characters). Authentication generator (password-based), rate_limit, CSRF default.
- [S15] https://rubyonrails.org/security - fetched. Rails security reporting and disclosure process.
- [S16] https://endoflife.date/php - fetched. PHP branch support dates.
- [S17] https://laravel.com/docs/releases - fetched. Laravel support table, Laravel 13 release, support policy, product list (Nova).
- [S18] https://laravel.com/docs/13.x/localization - fetched. Laravel translation files, pluralization.
- [S19] https://laravel.com/docs/13.x/queues - fetched (first 100,000 characters). Queue drivers and queue:work.
- [S20] https://github.com/laravel/framework/security/policy - fetched. Laravel security contact.
- [S21] https://laravel.com/docs/13.x/license - search result only. MIT licence and copyright holder.
- [S22] https://packagist.org/packages/harrisonclewis/laravel-passwordless ; https://github.com/SpykApp/passwordless-login - search results only. Laravel magic-link packages.
- [S23] https://github.com/filamentphp/filament/releases - fetched. Filament 5.11.3.
- [S24] https://symfony.com/releases - fetched. Symfony release and support table; "Today" on the page read as November 15, 2026.
- [S25] https://symfony.com/doc/current/security/login_link.html - fetched. Login links, expiry, max_uses, warnings.
- [S26] https://symfony.com/doc/current/translation.html - fetched. XLIFF, ICU MessageFormat, _locale routing.
- [S27] https://symfony.com/doc/current/messenger.html - fetched (first 100,000 characters). Doctrine transport and messenger:consume.
- [S28] https://symfony.com/doc/current/contributing/code/security.html - fetched. Symfony security reporting and classification.
- [S29] https://github.com/EasyCorp/EasyAdminBundle/releases - fetched. EasyAdmin 5.10.1.
- [S30] https://symfony.com/blog/a-business-model-for-symfony - search result only (2018 post). Symfony SAS and SensioLabs; dated.
- [S31] https://learn.microsoft.com/en-us/dotnet/core/releases-and-support - fetched. .NET supported versions, LTS and STS windows, servicing.
- [S32] https://endoflife.date/dotnet - fetched. .NET release and EOL table.
- [S33] https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity - fetched (first 100,000 characters). No passwordless or magic-link terms found in the fetched text.
- [S34] https://endoflife.date/go - fetched. Go release dates and support rule.
- [S35] https://go.dev/security/policy - fetched. Go security reporting, versions receiving fixes, 90-day commitment.
- [S36] https://go.dev/doc/go1.25 - fetched. net/http CrossOriginProtection.
- [S37] https://go.dev/doc/go1.22 - fetched. net/http.ServeMux patterns.
- [S38] https://pkg.go.dev/golang.org/x/text/message - fetched. Localized formatting and catalogs; v0.44.0 shown.
- [S39] https://github.com/alexedwards/scs - fetched. MIT, stability statement, backend policy.
- [S40] https://riverqueue.com/ - fetched. River background jobs on PostgreSQL; vendor and Pro licence link.
- [S41] https://www.postgresql.org/support/versioning/ - fetched. PostgreSQL major versions, final release dates, 19 RC.
- [S42] https://www.postgresql.org/docs/current/textsearch-dictionaries.html#TEXTSEARCH-SNOWBALL-DICTIONARY - fetched. Snowball stemmers for many languages; French not confirmed on the page.
- [S43] https://sqlite.org/fts5.html - fetched (first 100,000 characters). FTS5 tokenizers; porter English only.
- [S44] https://endoflife.date/nodejs - fetched. Node release lines.
- [S45] https://endoflife.date/python - fetched. Python 3.12 EOL.
- [S46] https://github.com/withastro/astro/releases ; https://docs.astro.build/en/guides/internationalization/ - fetched. Astro version and i18n routing.
- [S47] https://github.com/sveltejs/kit/releases ; https://svelte.dev/docs/kit/form-actions - fetched. SvelteKit release; form actions and progressive enhancement.
- [S48] https://paraglidejs.com/ - fetched. Paraglide JS v2, MIT, plurals and URL localization.
- [S49] https://github.com/drizzle-team/drizzle-orm/releases - fetched. Drizzle stable and pre-release tags.
- [S50] https://docs.adonisjs.com/guides/digging-deeper/i18n ; https://docs.adonisjs.com/guides/auth/introduction ; https://github.com/adonisjs/core/releases - fetched. AdonisJS i18n, auth guards, release listing.
- [S51] https://github.com/altcha-org/altcha ; https://altcha.org/ - fetched. ALTCHA widget MIT; Sentinel and server libraries.
- [S52] https://github.com/disposable-email-domains/disposable-email-domains - fetched. CC0 licence and maintenance model.
- [S53] https://gettext.hexdocs.pm/Gettext.html - fetched. Gettext for Elixir v1.0.2.
- [S54] https://phoenix.hexdocs.pm/Mix.Tasks.Phx.Gen.Auth.html ; https://phoenix.hexdocs.pm/overview.html - fetched. Phoenix v1.8.16 docs; phx.gen.auth email-based authentication.
- [S55] https://phoenix.hexdocs.pm/installation.html - fetched. Elixir 1.17 and Erlang 25 requirement.
- [S56] https://github.com/phoenixframework/phoenix - fetched. MIT licence.
- [S57] https://endoflife.date/wagtail - fetched. Wagtail release and support table.
- [S58] https://github.com/thoughtbot/administrate - fetched. Maintenance statement; no release date visible.
- [S59] https://rubyonrails.org/foundation ; https://rubyonrails.org/foundation/37signals - search results only. Rails Foundation governance; not verified on the pages.
- Repository documents: docs/plans/main.md; docs/decisions/0002-single-eu-vps.md; 0003-email-magic-link-auth.md; 0006-archive-first-replaceable-application.md; 0007-privacy-review-path.md; docs/research/domain-and-persistence.md; docs/constitution/archival-model.md; AGENTS.md.

Not verified in this pass (listed so they are not mistaken for facts): Django deprecation policy and upgrade history; Django rate limiting; Django admin change-history storage; Python minimum for Django 6.x; Phoenix governance and security policy; Oban and Ecto full-text search; Laravel scheduler; Laravel and Rails i18n URL handling; ASP.NET localization and jobs; Go html/template, pgx and migration tools; AdonisJS Node requirement, Lucid, jobs and governance; SvelteKit magic-link and job libraries; Drizzle full-text search; Symfony full-text search; the licences of altcha-lib packages and the Sentinel server; Rails Foundation structure; Symfony governance today.
