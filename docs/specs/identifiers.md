# Identifiers and permanent URLs

Status: Draft

Issue: #15

Basis: plan sections 12, 14, 19, 22 and 33; [Archival model](../constitution/archival-model.md); [ADR 0006](../decisions/0006-archive-first-replaceable-application.md); [domain and persistence research](../research/domain-and-persistence.md), section 3.

Identifiers belong to the archive, not to the application. They must survive redesigns, re-implementations and changes of custodian. The domain is written `<domain>` below until #8 is decided.

## 1. Entry identifiers

Every testimony has two identifiers.

| Identifier | Assigned | Visibility | Purpose |
| --- | --- | --- | --- |
| Internal ID | When the draft is created | Private. Never in URLs, pages or exports. | Joins and references inside the operational store, independent of state (plan section 33). |
| Public ID | When the entry is first published | Public, permanent. | Permanent link, citation, archival records, tombstones. |

### 1.1 Public ID syntax

- 8 symbols from the Crockford base32 alphabet (`0123456789abcdefghjkmnpqrstvwxyz`), giving 40 bits.
- Canonical form: lowercase, no separators, for example `7q4km2xd`.
- Generated from a cryptographically secure random source. A candidate that collides with any existing or tombstoned ID is discarded and regenerated.
- Carries no meaning: no year, no sequence, no language and no information about the contributor.
- Never reused, never changed, never reassigned, including after withdrawal.

Rationale:

- Assigning at publication means rejected or never-published submissions have no public ID. Nothing about moderation outcomes or submission volume can be inferred from IDs (research section 3.8).
- Dates live in metadata. A year in the ID would be ambiguous between submission, publication and edition years, because late submissions join later editions (plan section 19).
- 40 bits is short enough to cite in print and large enough that random guessing is pointless at any plausible archive size. Guessing only ever finds published entries, which are public anyway.
- This replaces the plan's illustrative `VOICE-2027-000184`, which the plan does not prescribe (section 12). "Voice" also conflicts with the public term "entry" (plan section 38).

### 1.2 Input tolerance

Readers copy IDs by hand. Lookups normalize input before matching: case-insensitive; hyphens and spaces ignored; `i` and `l` read as `1`, `o` read as `0` (Crockford decoding rules). A non-canonical form permanently redirects (301) to the canonical URL.

## 2. URLs

| Resource | Permanent URL | Notes |
| --- | --- | --- |
| Entry | `https://<domain>/entries/<public-id>` | Language-neutral. This is the form used in citations and archives. |
| Entry, localized interface | `https://<domain>/<locale>/entries/<public-id>` | `<locale>` is `en` or `fr`, later more. Linked with `hreflang`. The neutral URL redirects (302, `Vary: Accept-Language`) to the visitor's preferred interface locale. |
| Edition | `https://<domain>/time-capsules/<edition-id>` | See section 4. |
| Context document | `https://<domain>/context/<slug>` | See section 5. |
| Reference record | `https://<domain>/references/<slug>` | See section 5. |

Rules:

1. No slug, title or language of the entry text appears in the canonical entry path, because those can change.
2. URLs are never removed. Moved resources redirect permanently. Withdrawn entries become tombstones (section 3).
3. No technology-specific path elements (`.php`, `/app/`, `/api/v1/` for human pages) appear in permanent URLs.
4. The URL scheme is part of the archive specification. A re-implementation of the site must serve the same permanent URLs.

## 3. HTTP semantics by entry state

| State | Response at the entry URL |
| --- | --- |
| Never existed, draft, submitted, under review, rejected | `404 Not Found`, identical in every case, so that state cannot be probed |
| Published | `200 OK` |
| Published with moderation redaction | `200 OK`, with a visible note that part of the entry was redacted, without revealing what |
| Withdrawn | `410 Gone`, with a content-free tombstone page: the ID, the fact of withdrawal, and nothing that identifies the contributor or the content |

Private views of a contributor's own unpublished entries are reachable only when authenticated, at URLs that use neither the internal ID nor a public ID.

## 4. Edition identifiers

- Format: `<cutoff-year>.<revision>`, for example `2027.0` for the first edition with a cutoff of 2027-12-31, and `2027.1` for its first privacy revision.
- Revision `0` is the original release. Each later revision supersedes the earlier one for the copies the project controls.
- Rehearsal editions use the suffix `-rehearsal.<n>`, for example `2026-rehearsal.1`, and are never confused with real editions.
- External deposit identifiers (for example Internet Archive items) derive from the edition ID: `the-ai-guestbook-2027.0`. They are chosen once and never renamed (research section 3.6).

## 5. Context and reference identifiers

- Context documents and reference shelf records use lowercase ASCII slugs (`[a-z0-9]+(-[a-z0-9]+)*`), for example `epoch-ai-models` (plan section 18).
- A slug is permanent once published. A renamed document gets a redirect from its old slug. Slugs are never reused for a different subject.

## 6. Citation

Each entry page offers a copyable citation that respects the contributor's chosen public identity:

```text
<Display name | "Anonymous">, entry <public-id>, The Artificial Intelligence Guestbook, <publication date, ISO 8601>. https://<domain>/entries/<public-id>
```

A pseudonym is cited as given. An anonymous entry is cited as "Anonymous" and never with any other identifying metadata. When an edition is cited, ` Time capsule <edition-id>.` is appended.

## Open questions

- The exact domain (#8).
- How translations are addressed: one per language, or several per language (human and machine) with their own identifiers. To be settled in the data model (#14).
- Whether entry fragments get stable anchors for quoting (plan section 14 says optional).
