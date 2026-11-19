# Identifiers and permanent URLs

Status: Draft

Issue: #15

Basis: plan sections 12, 14, 19, 22 and 33; [Archival model](../constitution/archival-model.md); [ADR 0006](../decisions/0006-archive-first-replaceable-application.md); [domain and persistence research](../research/domain-and-persistence.md), section 3.

Identifiers belong to the archive, not to the application. They must survive redesigns, re-implementations and changes of custodian. The domain is `theaiguestbook.org` ([ADR 0008](../decisions/0008-canonical-domain.md)).

## 1. Testimony identifiers

Every testimony has two identifiers.

| Identifier | Assigned | Visibility | Purpose |
| --- | --- | --- | --- |
| Internal ID | When the draft is created | Private. Never in URLs, pages or exports. | Joins and references inside the operational store, independent of state (plan section 33). |
| Public ID | When the testimony is first published | Public, permanent. | Permanent link, citation, archival records, tombstones. |

### 1.1 Public ID syntax

- 8 symbols from the Crockford base32 alphabet (`0123456789abcdefghjkmnpqrstvwxyz`), giving 40 bits.
- Canonical form: lowercase, no separators, for example `7q4km2xd`.
- Generated from a cryptographically secure random source. A candidate that collides with any existing or tombstoned ID is discarded and regenerated.
- Carries no meaning: no year, no sequence, no language and no information about the contributor.
- Never reused, never changed, never reassigned, including after withdrawal.

Rationale:

- Assigning at publication means rejected or never-published submissions have no public ID. Nothing about moderation outcomes or submission volume can be inferred from IDs (research section 3.8).
- Dates live in metadata. A year in the ID would be ambiguous between submission, publication and edition years, because late submissions join later editions (plan section 19).
- 40 bits is short enough to cite in print and large enough that random guessing is pointless at any plausible archive size. Guessing only ever finds published testimonies, which are public anyway.
- This replaces the plan's original illustrative `VOICE-2027-000184`, which the plan did not prescribe (section 12). "Voice" was a terminology mistake; the object is a testimony.

### 1.2 Input tolerance

Readers copy IDs by hand. Lookups normalize input before matching: case-insensitive; hyphens and spaces ignored; `i` and `l` read as `1`, `o` read as `0` (Crockford decoding rules). A non-canonical form permanently redirects (301) to the canonical URL.

## 2. URLs

| Resource | Permanent URL | Notes |
| --- | --- | --- |
| Testimony | `https://theaiguestbook.org/testimonies/<public-id>` | Language-neutral. This is the form used in citations and archives. |
| Testimony, localized interface | `https://theaiguestbook.org/<locale>/testimonies/<public-id>` | `<locale>` is `en` or `fr`, later more. Linked with `hreflang`. The neutral URL redirects (302, `Vary: Accept-Language`) to the visitor's preferred interface locale. |
| Edition | `https://theaiguestbook.org/time-capsules/<edition-id>` | See section 4. |
| Context document | `https://theaiguestbook.org/context/<slug>` | See section 5. |
| Reference record | `https://theaiguestbook.org/references/<slug>` | See section 5. |

Rules:

1. No slug, title or language of the testimony text appears in the canonical testimony path, because those can change.
2. URLs are never removed. Moved resources redirect permanently. Withdrawn testimonies become tombstones (section 3).
3. No technology-specific path elements (`.php`, `/app/`, `/api/v1/` for human pages) appear in permanent URLs.
4. The URL scheme is part of the archive specification. A re-implementation of the site must serve the same permanent URLs.

### 2.1 Data URLs

Every public resource has a machine-readable form at a URL separate from the interface, so that programs and agents never need to parse the interface, and a re-implementation of the interface leaves them unchanged (ADR 0006; owner decision, 2026-11-19).

| Resource | Data URL | Content |
| --- | --- | --- |
| Testimony | `https://theaiguestbook.org/data/testimonies/<public-id>.json` | The testimony record in the edition schema ([archive format](archive-format.md), section 3), for the current revision, without `edition_id` |
| Testimony index | `https://theaiguestbook.org/data/testimonies.json` | Every published testimony with its summary fields, as the edition's `index.json` |
| Withdrawal list | `https://theaiguestbook.org/data/withdrawals.json` | As the edition's `withdrawals.json` (archive format, section 5) |
| Editions registry | `https://theaiguestbook.org/data/time-capsules.json` | Every edition revision ever published, with its state and digests (archive format, section 6) |
| Edition packages | `https://theaiguestbook.org/data/time-capsules/<edition-id>/<file>` | The serialized packages and their signature (archive format, section 1.1) |
| Signing key | `https://theaiguestbook.org/data/signing-key.asc` | The OpenPGP public key that signs editions, ASCII-armoured, standalone (section 7) |
| Context document | `https://theaiguestbook.org/data/context/<slug>.<language>.json` | The document and its metadata, as in editions |
| Reference record | `https://theaiguestbook.org/data/references/<slug>.json` | As the edition's reference records |
| Schemas | `https://theaiguestbook.org/data/schema/<format-version>/<name>.schema.json` | The JSON Schemas, also the `$id` of each schema |
| Markdown views | The interface URL with `.md` appended, for example `https://theaiguestbook.org/context/<slug>.md` and `https://theaiguestbook.org/testimonies/<public-id>.md` | The source text of documentation, context pages and testimonies, following the llms.txt companion-page convention |

Rules:

1. The data layer stops at the resource. There are no URLs into individual fields and no query language. A program reads the record and takes what it needs.
2. Data URLs serve only `public` fields, through the same allow-list and exporter as the editions ([data model](data-model.md), section 1.1). They are static files, regenerated with the static renderings when a testimony is published, edited or withdrawn ([deletion lifecycle](deletion-lifecycle.md), place 5).
3. A withdrawn testimony's data URL answers `410 Gone` with `{"public_id": "<public-id>", "status": "withdrawn"}`. Every other non-published state answers the same `404` as the interface (section 3).
4. Data URLs carry no version in the path. The format version is inside each document (`format_version`); a new format version publishes new schemas at a new schema URL.
5. Data URLs send `Access-Control-Allow-Origin: *`, so that browser-based tools can read them.
6. Interface pages point to their data form with `<link rel="alternate">` elements (`application/json` and `text/markdown`).

### 2.2 Discovery for programs and agents

1. `/robots.txt` allows crawling of interface and data URLs, except private and authenticated paths.
2. `/llms.txt` follows the llms.txt proposal (Jeremy Howard, 2024, an informal community convention, not a standard): an `h1`, a summary blockquote, and lists of links to the Markdown views of the public documentation and to the data URLs of section 2.1. It contains nothing that a human reader cannot find in the same documentation: it is an index, not separate documentation for machines.
3. Proposal: the methodology page documents the data URLs for people too, with examples, so that the human and machine descriptions are the same text.

### 2.3 Deep links

1. Each paragraph and heading of a rendered testimony has an anchor, `#p-<n>` for the `n`-th block. Anchors follow the current revision, so they are stable only until the next edit. The citation names the revision (section 6), and the timeline shows whether the text has changed since.
2. For quotations that should survive edits, the interface offers to copy a link with a text fragment (`#:~:text=`), which browsers that support it resolve by content rather than position. Nothing on the server depends on it.
3. Translations are addressed as `https://theaiguestbook.org/testimonies/<public-id>/translations/<translation-id>`, with the data form at `/data/testimonies/<public-id>.json` (translations are part of the record). Several translations per language are possible ([data model](data-model.md), section 2.9).

## 3. HTTP semantics by testimony state

| State | Response at the testimony URL |
| --- | --- |
| Never existed, draft, submitted and not yet published, quarantined | `404 Not Found`, identical in every case, so that state cannot be probed. Quarantine answers 404, not 410, because it can be lifted. |
| Published | `200 OK` |
| Withdrawn | `410 Gone`, with a content-free tombstone page: the ID, the fact of withdrawal, and nothing that identifies the contributor or the content |

Private views of a contributor's own unpublished testimonies are reachable only when authenticated, at URLs that use neither the internal ID nor a public ID.

## 4. Edition identifiers

- Format: `<cutoff-year>.<revision>`, for example `2027.0` for the first edition with a cutoff of 2027-12-31, and `2027.1` for its first privacy revision.
- Revision `0` is the original release. Each later revision supersedes the earlier one for the copies the project controls.
- Rehearsal editions use the suffix `-rehearsal.<n>`, for example `2026-rehearsal.1`, and are never confused with real editions.
- External deposit identifiers (for example Internet Archive items) derive from the edition ID: `the-ai-guestbook-2027.0`. They are chosen once and never renamed (research section 3.6).

## 5. Context and reference identifiers

- Context documents and reference shelf records use lowercase ASCII slugs (`[a-z0-9]+(-[a-z0-9]+)*`), for example `epoch-ai-models` (plan section 18).
- A slug is permanent once published. A renamed document gets a redirect from its old slug. Slugs are never reused for a different subject.

## 6. Citation

A citation component offers three formats as tabs, with plain text open by default: plain text, BibTeX and Hayagriva YAML (the bibliography format of Typst). It appears on each testimony page and on each edition page; the testimony record also carries the plain-text form in `citation` (owner decision, 2026-11-19). All three are generated from the public record, so any program can produce them the same way.

Plain text:

```text
<attribution>, testimony <public-id>, revision <n>, The Artificial Intelligence Guestbook, <publication date of the revision, ISO 8601>. https://theaiguestbook.org/testimonies/<public-id>
```

BibTeX (biblatex fields; the double braces keep a display name from being parsed into first and last names):

```text
@misc{aiguestbook-<public-id>,
  author       = {{<attribution>}},
  title        = {Testimony <public-id>},
  howpublished = {The Artificial Intelligence Guestbook},
  date         = {<publication date of the revision>},
  version      = {<n>},
  url          = {https://theaiguestbook.org/testimonies/<public-id>}
}
```

Hayagriva:

```yaml
aiguestbook-<public-id>:
  type: Web
  title: Testimony <public-id>
  author: <attribution>
  date: <publication date of the revision>
  publisher: The Artificial Intelligence Guestbook
  url: https://theaiguestbook.org/testimonies/<public-id>
  serial-number:
    serial: <public-id>
```

Rules:

1. `<attribution>` is the display name as given for named and pseudonymous testimonies, and "Anonymous" for anonymous ones, never with other identifying metadata ([data model](data-model.md), section 2.3). Display names are not split into first and last names. How each format renders single-word and multi-word display names is checked when the component is built.
2. The revision number tells a reader whether the text they find is the one cited; superseded text is not kept (data model, section 2.5).
3. When an edition is cited, the plain-text form ends with `Time capsule <edition-id>.` after a space, and the structured forms add the edition ID to the title.

## 7. Edition signing key

Editions are signed with one OpenPGP key ([archive format](archive-format.md), section 6). A signature is only as trustworthy as the reader's copy of the public key, so the key is published in several independent places, and its fingerprint wherever the key itself cannot go.

| Place | What | Notes |
| --- | --- | --- |
| `https://theaiguestbook.org/data/signing-key.asc` | The public key, standalone | Data URL (section 2.1) |
| The website's page on verifying editions | The fingerprint, a link to the key, and verification instructions | Human-readable counterpart of the data URL |
| The repository, `keys/edition-signing-key.asc` | The public key | Versioned and mirrored with the repository, independent of the website |
| The repository documentation on editions | The fingerprint | |
| Each edition's `README.txt` and `README.fr.txt` | The fingerprint, and where to get the key | Inside the signed package, so it confirms the key but cannot establish it alone |
| The editions registry (`/data/time-capsules.json`) | The fingerprint of the key that signed each revision | Keeps old revisions verifiable after a key change |
| Proposal: the keys.openpgp.org keyserver and a Web Key Directory for `contact@theaiguestbook.org` | The public key | Standard discovery for OpenPGP tools. The Web Key Directory is specified by the IETF Internet-Draft `draft-koch-openpgp-webkey-service`, not an RFC, and serves static files under `/.well-known/openpgpkey/`, a well-known URI path in the sense of RFC 8615. |

Rules:

1. A new key is announced in all these places, signed by the old key where it is still available, and the registry records which key signed each revision.
2. Key custody and succession belong to the succession arrangements (#33), like the backup key.

## Open questions

1. Resolved (2026-11-19): translations are addressed by `translation_id`, several per language (section 2.3, item 3).
2. Resolved (2026-11-19): paragraph anchors, stable per revision, plus text fragments (section 2.3).
3. Resolved (2026-11-19): context documents and reference records get JSON data URLs too, `/data/context/<slug>.<language>.json` and `/data/references/<slug>.json`, since editions already export them. What generates them and when is decided with the implementation.
