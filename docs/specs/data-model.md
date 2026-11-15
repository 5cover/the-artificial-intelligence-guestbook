# Data model and testimony lifecycle

Status: Draft (2026-11-15). Items marked "Proposal" need owner review.

Issue: #14

Basis: plan sections 4 to 12, 22 and 33; the [constitution](../constitution/README.md); [ADR 0003](../decisions/0003-email-magic-link-auth.md), [ADR 0006](../decisions/0006-archive-first-replaceable-application.md), [ADR 0009](../decisions/0009-testimony-licensing.md), [ADR 0010](../decisions/0010-stack-django-postgresql.md); [identifiers](identifiers.md); [threat model](threat-model.md); [legal research](../research/legal-landscape.md), sections 2 to 4, 10 and 12.

This model is conceptual. It names objects, fields, classifications and transitions, not database tables. The Django implementation (#21) and the archive format (#13) must both conform to it. Field names are given in `snake_case` because they become identifiers in code and in exports.

## 1. Field classification

Every field belongs to exactly one class. The class decides where the field may go.

| Class | Meaning | Rendered publicly | Exported to editions | Example |
| --- | --- | --- | --- | --- |
| `public` | Chosen by the contributor or the project for publication | Yes, when the object is published | Yes | testimony text, display name |
| `private` | About the contributor, needed to run the service, never published | No | Never | account email, original text before redaction |
| `operational` | Needed to run, moderate or secure the service | No | Never | moderation notes, rate-limit counters |
| `evidence` | Kept to show that a legal duty or consent was met | No | Never | consent timestamps and text versions |

Rules:

1. Exports and public views are built from an explicit allow-list of `public` fields. Nothing reaches them by default.
2. A field without a class is a defect. An automated test fails if any model field is unclassified, or if a non-`public` field appears in an export or public template (threat model, section 3.6).
3. Changing a field's class is a data-model change and is recorded in this document.

## 2. Objects

### 2.1 Account (`private`)

The private identity behind contributions ([privacy assumptions](../constitution/privacy-assumptions.md) 2 and 3).

| Field | Class | Notes |
| --- | --- | --- |
| `internal_id` | private | Never exposed |
| `email` | private | Normalized to lowercase; unique. The only contact and withdrawal channel. |
| `email_verified_at` | private | Set by the first successful magic-link sign-in |
| `created_at`, `last_sign_in_at` | private | Dates only where precision is not needed |
| `interface_locale` | private | `en` or `fr` (later more), for emails |
| `status` | operational | `active`, `restricted`, `closed` |
| `restriction_reason` | operational | Publishing rule cited (moderation principles, "Practice" 1) |
| `closed_at` | private | Starts the retention clock (section 6) |

No names, photos, phone numbers, postal addresses or identity-provider data are collected.

### 2.2 Sign-in token (`operational`, short-lived)

| Field | Class | Notes |
| --- | --- | --- |
| `token_hash` | operational | Hash of a single-use random token. The token itself is never stored. |
| `email` | operational | The address it was sent to |
| `created_at`, `expires_at`, `used_at` | operational | Expiry 15 minutes (threat model, section 3.1) |

Deleted once used or expired, after at most 24 hours.

### 2.3 Testimony

The primary object. One account may have several testimonies. Their public identities are independent and must not be publicly linkable to each other (section 2.4).

| Field | Class | Notes |
| --- | --- | --- |
| `internal_id` | private | Assigned at draft creation; stable for the object's whole life ([identifiers](identifiers.md), section 1) |
| `public_id` | public | Assigned at first publication; never reused ([identifiers](identifiers.md), section 1.1) |
| `account` | private | Link to the account. Never public, never exported. |
| `state` | operational | See section 3 |
| `language` | public | BCP 47 tag of the original text, declared by the contributor |
| `body` | public | The current public text (section 2.5) |
| `received_at` | private | First submission. Decides the edition period (section 5). |
| `published_on` | public | Date only, no time, to limit correlation with events (threat model, section 3.3) |
| `withdrawn_on` | public, on the tombstone only | Date only |
| `edition_period` | public | The cutoff year of the period the testimony belongs to (section 5) |
| `licence` | public | `CC-BY-4.0` (ADR 0009), stored per testimony so a future change does not rewrite history |
| `attribution` | public | Derived from the public identity: display name, pseudonym, or "Anonymous" |
| `redacted` | public | Boolean. When true, the public page says part of the text was redacted, not what (moderation principles, "Practice" 3). |

Text rules: plain text, Unicode NFC, paragraphs separated by blank lines, no markup (threat model, section 3.3). Proposal: a maximum of 50,000 characters and a minimum of 1 non-whitespace character. The maximum stops abuse without constraining a long essay, and is reviewed if real testimonies approach it.

### 2.4 Public identity (per testimony, all optional)

Every field is optional and published only if the contributor fills it in. Identity is per testimony, not per account, so that a person can publish one testimony under their name and another anonymously without the two being linkable.

| Field | Class | Values |
| --- | --- | --- |
| `identity_mode` | public | `named`, `pseudonymous`, `anonymous` |
| `display_name` | public | Free text, for `named` and `pseudonymous` only |
| `age_range` | public, with rules | Controlled list (section 2.4.1) |
| `country` | public | ISO 3166-1 alpha-2 |
| `region` | public | Free text, shown only if the filter rules allow it (#27) |
| `languages` | public | BCP 47 tags of the languages the contributor lives in, distinct from the testimony's language |
| `profession` | public | Free text |
| `field` | public | Controlled list for browsing (to be defined in #27), optional alongside the free text |
| `organization` | public | Free text |
| `organization_type` | public | Controlled list: for example `none`, `self-employed`, `company`, `public-sector`, `education`, `non-profit`, `other` |
| `relationship_to_ai` | public | Multi-select controlled list, for example `user`, `non-user`, `refuser`, `builder`, `researcher`, `affected-by`, `unsure`. It must not invite sensitive disclosure (legal research, section 3). |
| `link` | public | One URL, rendered `rel="ugc nofollow noopener"` (ADR 0003) |

#### 2.4.1 Age ranges

Public values: `under-18`, `18-24`, `25-34`, `35-44`, `45-54`, `55-64`, `65-74`, `75-plus`. A minor's age is never published more precisely than `under-18` (legal research, section 4). The declared age used for consent (section 2.8) is a separate, private field, and is never derived from or into the public value.

### 2.5 Text versions (`private` history, one `public` current version)

The original submission and every later change are kept privately, so that redaction never destroys the original while the testimony exists (moderation principles, "Practice" 3).

| Field | Class | Notes |
| --- | --- | --- |
| `version_number` | operational | 1 is the submission |
| `body` | private | The text of this version |
| `source` | operational | `contributor` (submission or correction), `moderator` (redaction) |
| `reason` | operational | For redactions: the publishing rule cited. For corrections: optional contributor note. |
| `created_at` | operational | |
| `is_current_public` | operational | Exactly one version is current once the testimony is published |

Post-publication corrections by the contributor (rectification right) create a new version, which goes through moderation before it becomes public. A correction after an edition has been built appears in the next edition. The edition keeps the version that was current at build time.

### 2.6 Authorship disclosure (`public`)

As defined in [authorship disclosure](../constitution/authorship-disclosure.md).

| Field | Class | Notes |
| --- | --- | --- |
| `category` | public | One of `none`, `assisted-language`, `assisted-structure`, `substantially-generated`, `fully-generated`, `undisclosed` (required) |
| `model_or_product` | public | Optional, free text |
| `model_version` | public | Optional |
| `mode_or_setting` | public | Optional |
| `workflow` | public | Optional: prompts or workflow description |
| `changes_after` | public | Optional: what the person changed afterwards |
| `comment` | public | Optional |

### 2.7 Structured testimony fields (`public`, optional)

Proposal: a deliberately short set, to keep the form from feeling like a survey (editorial principles, "Testimonies" 3). The free text remains the testimony.

| Field | Values |
| --- | --- |
| `ai_use_frequency` | `never`, `rarely`, `monthly`, `weekly`, `daily`, `constantly`, `unsure` |
| `tools_used` | Free-text list |
| `attitude` | Self-described: `enthusiastic`, `positive`, `mixed`, `indifferent`, `negative`, `hostile`, `unsure` |
| `prediction` | Optional free text "to leave on record", with an optional `prediction_horizon` year |

Controlled values are stable codes with localized labels, like the authorship codes.

### 2.8 Consent and age record (`evidence`)

Kept to show that publication was lawful (legal research, sections 2 to 4). One record per submission, and per correction.

| Field | Class | Notes |
| --- | --- | --- |
| `publication_consent_at` | evidence | Consent to publication and archival editions |
| `explicit_consent_at` | evidence | Explicit consent covering sensitive self-disclosure (GDPR art. 9(2)(a)); required in the flow for everyone, because any text may contain it |
| `licence_grant_version` | evidence | Version of the CC BY 4.0 plus project-grant text accepted (ADR 0009) |
| `terms_version`, `privacy_notice_version` | evidence | Versions shown at submission |
| `consent_locale` | evidence | Language of the texts shown |
| `declared_age_band` | evidence | `under-threshold` or `at-or-over-threshold`, plus the country used to choose the threshold. Not the exact age. |
| `consent_path` | evidence | `self` or `parental` |
| `parental_consent_at`, `parental_method` | evidence | For the parental path only. Verification data itself (such as the parent's email) is deleted once verification completes (CNIL Recommendation 7, legal research section 4). |

The parental flow and its thresholds are proposed in [legal bases and minors](../proposals/legal-bases-and-minors.md) (#12, #17).

### 2.9 Translation (`public` once published)

As required by the [multilingual principles](../constitution/multilingual-principles.md).

| Field | Class | Notes |
| --- | --- | --- |
| `translation_id` | public | Short opaque ID, unique within the testimony. Several translations per language are allowed, for example machine and human. |
| `language` | public | BCP 47 |
| `body` | public | |
| `source_version` | public | Which text version was translated. A translation of an older version is flagged as possibly outdated. |
| `producer_kind` | public | `contributor`, `project-human`, `machine` |
| `producer_name` | public | For machines: system name and version. For people: as they wish to be credited, or "the project". |
| `created_on` | public | Date |
| `reviewed` | public | Whether a person reviewed it, and `reviewed_on` |
| `state` | operational | `draft`, `published`, `retracted` |

Only published testimonies may be machine-translated, and only through an EU processor under a DPA or a self-hosted system (threat model, section 3.6).

### 2.10 Moderation record (`operational`)

| Field | Class | Notes |
| --- | --- | --- |
| `testimony` | operational | |
| `decision` | operational | `publish`, `request-changes`, `redact`, `reject`, `remove`, `restrict-account` |
| `rule` | operational | Identifier of the publishing rule applied (moderation principles, "Practice" 1) |
| `note` | operational | Private moderator note. Must not copy the offending content (#41). |
| `decided_by`, `decided_at` | operational | |
| `statement_sent_at` | operational | Statement of reasons to the contributor (DSA art. 17, legal research section 5) |

### 2.11 Notice (`operational`)

A third-party notice about published content (DSA art. 16, LCEN; #41).

| Field | Class | Notes |
| --- | --- | --- |
| `received_at`, `channel` | operational | |
| `testimony_public_id` | operational | |
| `notifier_contact` | operational | Only what the notifier gives and the procedure needs |
| `grounds`, `outcome`, `outcome_at` | operational | |

### 2.12 Withdrawal request (`operational`, then minimal `evidence`)

| Field | Class | Notes |
| --- | --- | --- |
| `scope` | operational | `testimony`, `field` (one public-identity field), `account` (all testimonies and the account) |
| `testimony` | operational | Cleared when the request completes |
| `requested_at`, `verified_at` | operational | Verification by magic link to the account email |
| `steps` | operational | Propagation checklist ([deletion lifecycle](deletion-lifecycle.md)) |
| `completed_at` | evidence | Kept with the tombstone's `public_id` only, no account link (legal research, section 10) |
| `minor_at_collection` | evidence | Whether the accelerated erasure right for data collected from minors applied (Loi I&L art. 51 II) |

### 2.13 Tombstone (`public`)

What remains of a withdrawn or removed testimony.

| Field | Class |
| --- | --- |
| `public_id` | public |
| `status` | public: always `withdrawn` |
| `withdrawn_on` | public: date |

Nothing else: no text, identity, language, country, edition labels or cause (legal research, section 10). Contributor withdrawal and moderation removal look the same publicly, so a tombstone never says "removed for illegal content". The cause stays in the operational records for as long as they are retained.

### 2.14 Context document and reference record (`public`, project-authored)

Context documents (plan section 16): `slug`, `language`, `title`, `body` (Markdown in the repository; ADR 0010 follow-up), `published_on`, `updated_on`, `sources`. Each language version is a separate document linked by `slug`.

Reference records (plan section 18): `slug`, `name`, `role`, `homepage`, `resource_url`, `description`, `verified_on`, `local_snapshot` (path and checksum in the edition, if lawful), `licence`, `notes`.

Both are project material: their licence is decided in #43, not by ADR 0009.

### 2.15 Edition (`public`)

| Field | Class | Notes |
| --- | --- | --- |
| `edition_id` | public | `<cutoff-year>.<revision>`, or `<year>-rehearsal.<n>` ([identifiers](identifiers.md), section 4) |
| `cutoff` | public | Last `received_at` date included |
| `built_on` | public | |
| `supersedes` | public | The previous revision, if any |
| `state` | public | `rehearsal`, `current`, `superseded` |
| `manifest_digest`, `signature` | public | Defined by the archive format (#13) |

### 2.16 Operational records

- **Rate-limit counters:** keyed by account or by a keyed hash of the IP address, with a salt rotated at least daily, so stored keys cannot be reversed into addresses. Retention is the counting window only, at most 24 hours.
- **Admin audit log:** actor, action, object reference and time, append-only (threat model, section 3.2). Never contains testimony text or emails.
- **Sessions:** framework-managed, server-side and revocable.

## 3. Testimony states

```text
draft --submit--> submitted --claim--> under_review --publish--> published --withdraw or remove--> withdrawn (tombstone)
  ^                                      |      |                  |
  +---------- request changes -----------+      |                  +-- redact or correct --> published (new version)
                                                +--reject--> rejected --after retention--> deleted
draft or submitted --discard, or abandon after inactivity--> deleted
```

| From | To | Who | Effect |
| --- | --- | --- | --- |
| none | `draft` | contributor | `internal_id` assigned |
| `draft` | `submitted` | contributor | Consent record written. `received_at` is set on first submission only. The pending cap is checked (ADR 0003). |
| `submitted` | `under_review` | moderator | Claimed; another moderator would not take it |
| `under_review` | `published` | moderator | `public_id` assigned on first publication, `published_on` set, search index and static rendering updated |
| `under_review` | `draft` | moderator | Changes requested with a message (moderation principles, "Practice" 2) |
| `under_review` | `rejected` | moderator | Statement of reasons sent |
| `published` | `published` | moderator or contributor | New public version after redaction or a moderated correction |
| `published` | `withdrawn` | contributor | Withdrawal request verified. Deletion lifecycle runs and a tombstone is created. |
| `published` | `withdrawn` | moderator | Removal after a notice or a later finding. Same public effect, cause recorded privately. |
| `draft`, `submitted` | deleted | contributor | Contributor discards. No public ID ever existed. |
| `draft` | deleted | system | Abandoned after the inactivity period |
| `rejected` | deleted | system | After the retention period |

Invariants:

1. A testimony has a `public_id` if and only if it has been published at least once.
2. Only `published` testimonies are rendered at their URL. Every other state, including deleted, answers the same 404, except withdrawn, which answers 410 with the tombstone ([identifiers](identifiers.md), section 3).
3. No path leads from `withdrawn` back to `published`. A contributor who changes their mind submits a new testimony and gets a new `public_id`.
4. The consent record of the submission that led to publication is kept while the testimony is published.

## 4. Relationships and linkability

- Account to testimony is private. No public page, export, URL or identifier reveals that two testimonies share an account.
- Public IDs are random and assigned at publication, so publication order does not reveal account grouping.
- Moderators see the account link only where needed: pending caps, restriction, withdrawal verification.

## 5. Edition periods

Proposal:

1. A testimony belongs to the period of its `received_at` date: the period whose cutoff is the next 31 December. This follows plan section 19, where a submission received after the cutoff "becomes part of a subsequent archival period".
2. An edition is built after the moderation queue for its period has been cleared, for example in the following January. Testimonies received before the cutoff but still unmoderated at build time join the edition's first revision.
3. The edition period is public, because readers and researchers need to know which time capsule a testimony belongs to. It reveals no more than the publication date already does.

## 6. Retention

Retention periods are specified in the retention schedule (#18), because some depend on the legal decisions of #12, notably whether decree 2021-1362 applies. This model fixes what each period starts from:

| Object | Clock starts at |
| --- | --- |
| Abandoned draft | Last edit |
| Rejected testimony and its versions | Rejection |
| Moderation records | Decision |
| Sign-in tokens | Creation |
| Rate-limit counters | Window start |
| Account | Closure |
| Consent record | Withdrawal or deletion of the testimony |
| Withdrawal evidence | Completion |

## 7. Search

Full-text search uses PostgreSQL per-language configurations: `french` and `english` for those languages, and `simple` for languages without a stemmer (ADR 0010). The search vector is derived in the database from the current public version, so it is updated or deleted with the row (RFP section 8). Only `published` testimonies are indexed.

## 8. Open questions

- The controlled vocabularies (`field`, `relationship_to_ai`, `attitude` and others) need wording and translation review, and filter thresholds (#27).
- Whether contributors may edit their own pending submission after submitting, or only through "request changes".
- The maximum text length (section 2.3) and the structured-field set (section 2.7) are proposals.
