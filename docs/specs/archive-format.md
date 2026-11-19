# Archive format and edition packaging (v0)

Status: Draft (2026-11-15). Items marked "Proposal" need owner review. Format version: 0, unstable until the rehearsal edition (#38).

Issue: #13

Basis: [archival model](../constitution/archival-model.md); [ADR 0006](../decisions/0006-archive-first-replaceable-application.md); [ADR 0009](../decisions/0009-testimony-licensing.md); [data model](data-model.md); [identifiers](identifiers.md); [deletion lifecycle](deletion-lifecycle.md); [domain and persistence research](../research/domain-and-persistence.md), section 4; plan sections 19, 20 and 23.

The archive is the primary deliverable. This format is specified independently of the application. A future custodian must be able to read an edition with nothing but a text editor, and to verify it with common tools, without the Guestbook software (archival model, principle 5).

## 1. Principles

1. **Plain and redundant.** Every testimony is present as structured data (JSON) and as plain text. A static HTML rendering is added for readers. Losing the ability to parse one form leaves the others.
2. **Self-describing.** Each edition carries its own documentation, schema and licence. Nothing needed to understand it lives only on the website.
3. **Public fields only.** An edition is built from the data model's allow-list of `public` fields (data model, section 1). Private, operational and evidence fields never enter it.
4. **Verifiable.** Checksums cover every file; a signature covers the checksums.
5. **Revisable for privacy.** An edition can be superseded by a privacy revision. Each revision is a complete, independent package.
6. **Stable names.** File and field names come from the identifiers and the data model, and do not change between editions without a schema version change.

## 2. Package

An edition revision is one BagIt bag (RFC 8493), named `the-ai-guestbook-<edition-id>`, for example `the-ai-guestbook-2027.0`.

```text
the-ai-guestbook-2027.0/
  bagit.txt
  bag-info.txt
  manifest-sha512.txt
  manifest-sha256.txt
  tagmanifest-sha512.txt
  tagmanifest-sha256.txt
  tagmanifest-sha512.txt.sig          detached signature (section 6)
  data/
    README.txt                        what this archive is and covers, in English (section 2.2)
    README.fr.txt                     the same in French
    LICENSE.txt                       licences of the compilation and its parts (section 7)
    CHANGELOG.txt                     revision history of this edition
    schema/
      README.txt                      field-by-field description in plain text
      testimony.schema.json           JSON Schema (draft 2020-12)
      withdrawals.schema.json
      reference.schema.json
      context.schema.json
    testimonies/
      <public-id>.json                one record per testimony (section 3)
      <public-id>.txt                 plain-text rendering (section 4)
    all-testimonies.txt               every testimony's plain-text rendering in one file, in public-ID order (section 4)
    index.json                        list of testimonies with summary fields
    index.csv                         the same, for spreadsheets (RFC 4180)
    paths.csv                         every public ID ever published, with its path or "withdrawn"
    withdrawals.json                  withdrawal list (section 5)
    withdrawals.csv                   the same, as CSV
    context/
      <slug>.<language>.html          context documents, canonical form
      <slug>.<language>.txt           plain-text rendering
      <slug>.<language>.md            source as authored, a derived copy (CommonMark)
    references/
      <slug>.json                     reference shelf records
    snapshots/
      <slug>/...                      local snapshots of references, only where redistribution is lawful
    html/
      index.html                      static rendering, no JavaScript, relative links
      testimonies/<public-id>.html
    provenance.json                   how this package was built (section 8)
```

Encoding rules for every file the project writes:

- UTF-8 without a byte-order mark, Unicode NFC, LF line endings, a final newline;
- JSON as RFC 8259, with object keys in a fixed order;
- dates in ISO 8601 date format (`2027-03-14`), never with a time of day;
- language tags as BCP 47;
- country codes as ISO 3166-1 alpha-2.

### 1.1 Serialization for download

1. The bag is serialized as a POSIX `tar` archive (pax format) compressed with gzip (RFC 1952), named `the-ai-guestbook-2027.0.tar.gz` (owner decision, 2026-11-19). Both are readable by standard tools on every common system.
2. Editions are built rarely and downloaded often, so compression favours size over time. Compression uses the strongest gzip-compatible encoder available. Proposal: Zopfli, an encoder that writes standard gzip, typically a few percent smaller than `gzip -9`, at a much higher compression time; otherwise `gzip -9`. Any gzip decoder reads either.
3. gzip cannot be given a larger dictionary: DEFLATE looks back at most 32 KiB (RFC 1951). Repeated content further apart than that is not deduplicated, so each rendering of a testimony costs roughly its own compressed size. To let gzip find repetitions where it can, tar members are ordered by testimony (the JSON record, plain text and HTML of one testimony are adjacent), not by directory.
4. Proposal: a second serialization of the same bag, `the-ai-guestbook-2027.0.tar.xz`, compressed with `xz -9e` (LZMA2 with a 64 MiB dictionary), which does deduplicate across renderings. It is offered next to the gzip file, not instead of it. Both are listed in the editions registry with their digests (section 6). Owner decision pending (section 12, question 8).

### 1.2 Size

Estimate, to watch rather than to engineer for [inference]. Assumptions: an average of 1.25 bytes per character in UTF-8; per testimony, the JSON record, the plain-text file, its share of `all-testimonies.txt` and the HTML page each carry the body once, plus about 4 KB of metadata and markup in total. Prose compresses about 3 to 1 with gzip.

| Case | Testimonies | Average length | Unpacked | `tar.gz` | `tar.xz` (proposed) |
| --- | --- | --- | --- | --- | --- |
| Realistic first edition | 1,000 | 3,000 characters | about 20 MB | about 7 MB | about 2 to 3 MB |
| Extreme | 10,000 | 50,000 characters (the maximum) | about 2.8 GB | about 1 GB | about 0.3 GB |

1. With gzip, size grows linearly with the number of renderings: each rendering adds roughly its own compressed size, because copies of a testimony are further apart than the 32 KiB window except for short testimonies (section 1.1). With xz's large dictionary, an extra rendering of the same text costs mainly its markup, so most of the duplication disappears.
2. The space needed to unpack equals the unpacked size, which stays reasonable even in the extreme case.
3. Renderings that are already compressed internally, such as PDF with embedded fonts, do not benefit from either compressor. A per-testimony PDF would add tens of kilobytes per testimony and dominate the package (question 4 of section 12).
4. The actual sizes are recorded in `provenance.json` and the editions registry, and reviewed at each edition.

### 2.1 `bag-info.txt`

Standard BagIt fields plus edition fields:

```text
Source-Organization: The Artificial Intelligence Guestbook
Contact-Email: contact@theaiguestbook.org
External-Identifier: the-ai-guestbook-2027.0
External-Description: Annual edition (time capsule) of The Artificial Intelligence Guestbook, a human time capsule of the AI era.
Bagging-Date: 2028-01-20
Bag-Group-Identifier: the-ai-guestbook
Edition-Id: 2027.0
Edition-Cutoff: 2027-12-31
Edition-Supersedes: none
Format-Version: 0
Payload-Oxum: <octets>.<files>
```

The BagIt fields come from RFC 8493. The `Edition-*` and `Format-Version` fields are this project's own extension. They are documented in `data/schema/README.txt`.

Bag rules ([archive-failures research](../research/archive-failures.md), section 4.1):

- payload and tag manifests are written in both SHA-512 and SHA-256, so that either common validator can check the bag;
- there is no `fetch.txt`: the bag is complete, and every payload file appears in every manifest;
- canonical content is UTF-8 plain text, JSON, CSV and HTML. Testimony bodies are CommonMark 0.31.2 source text ([data model](data-model.md), section 2.3.1): they are canonical as plain text, readable without any rendering, and the variant is declared in every record (`body_format`), which answers the concern that Markdown has no single standard (archive-failures research, section 3.19). The HTML rendering is derived. No database dump or application-specific serialization is canonical.

### 2.2 README coverage statement

`README.txt` and `README.fr.txt` state, in plain language:

- what the archive is;
- the period and cutoff the edition covers;
- how many testimonies it contains;
- what it excludes: unmoderated, rejected and withdrawn testimonies, and all private data;
- its licences;
- that every date is a Gregorian calendar date in UTC ([data model](data-model.md), section 1.3);
- how to verify the package (section 6), and how to cite the edition and a testimony;
- its relation to earlier revisions;
- the withdrawal policy, including that copies distributed before a revision cannot be recalled.

A collection that does not say what it holds cannot be trusted later (archive-failures research, lessons on coverage).

## 3. Testimony record

One JSON object per testimony, `data/testimonies/<public-id>.json`. Field names and values are the `public` fields of the [data model](data-model.md). Absent optional fields are omitted, never written as `null`, so that "not given" is unambiguous. `revisions` is the public timeline (data model, section 2.5): dates, sources and summaries only, never superseded text. `body` is the revision current at build time. `edition_id` is required in editions; the live data URL serves the same record without it ([identifiers](identifiers.md), section 2.1). There is no separate attribution field: attribution is `identity.mode` plus, for named and pseudonymous testimonies, `identity.display_name`. The `citation` string renders an anonymous testimony as "Anonymous".

```json
{
  "format_version": 0,
  "edition_id": "2027.0",
  "public_id": "7q4km2xd",
  "url": "https://theaiguestbook.org/testimonies/7q4km2xd",
  "language": "fr",
  "published_on": "2027-03-14",
  "edition_period": 2027,
  "licence": "CC-BY-4.0",
  "citation": "Anonymous, testimony 7q4km2xd, revision 2, The Artificial Intelligence Guestbook, 2027-05-02. https://theaiguestbook.org/testimonies/7q4km2xd Time capsule 2027.0.",
  "redacted": false,
  "body_format": "commonmark-0.31.2",
  "body": "Texte du témoignage...\n\nDeuxième paragraphe.",
  "revisions": [
    { "revision_number": 1, "published_on": "2027-03-14", "source": "contributor" },
    { "revision_number": 2, "published_on": "2027-05-02", "source": "contributor", "summary": "Corrected a date" }
  ],
  "identity": {
    "mode": "anonymous",
    "age_range": "35-44",
    "country": "FR",
    "relationship_to_ai": ["user"]
  },
  "authorship": {
    "category": "assisted-language",
    "model_or_product": "..."
  },
  "structured": {
    "ai_use_frequency": "weekly",
    "attitude": "mixed"
  },
  "translations": [
    {
      "translation_id": "t1",
      "language": "en",
      "body": "...",
      "source_revision": 2,
      "producer_kind": "machine",
      "producer_name": "<system name and version>",
      "created_on": "2027-03-20",
      "reviewed": true,
      "reviewed_on": "2027-03-22"
    }
  ]
}
```

The JSON Schema in `data/schema/testimony.schema.json` is normative. The example is not. The same schema validates every export in the application's test suite (section 9). Code types may be generated from it (ADR 0010, consequences).

## 4. Plain-text rendering

`data/testimonies/<public-id>.txt` is the human-readable copy, independent of JSON:

```text
The Artificial Intelligence Guestbook
Testimony 7q4km2xd
https://theaiguestbook.org/testimonies/7q4km2xd

Published: 2027-03-14
Revised: 2027-05-02 (Corrected a date)
Language: fr
By: Anonymous
Age range: 35-44
Country: FR
AI involvement: AI used for proofreading or translation (assisted-language)
Licence: CC BY 4.0

----

Texte du témoignage...

Deuxième paragraphe.

----

Translation (en), machine translation by <system name and version>, reviewed 2027-03-22:

...
```

Labels in the plain-text and HTML renderings are in English, with the stable codes in parentheses, so that the codes stay interpretable without the schema.

`data/all-testimonies.txt` concatenates the plain-text renderings of every testimony in the edition, in public-ID order, each preceded by a separator line, so that the whole edition can be read with nothing but a text viewer (owner decision, 2026-11-19).

## 5. Withdrawal list

`data/withdrawals.json` lists every testimony withdrawn from any earlier edition or revision, up to this package's build date. The live service publishes the current list at `https://theaiguestbook.org/data/withdrawals.json` ([identifiers](identifiers.md), section 2.1).

```json
{
  "format_version": 0,
  "generated_on": "2028-02-01",
  "withdrawals": [
    { "public_id": "9xk3m2pa", "editions": ["2026-rehearsal.1"] }
  ]
}
```

Nothing else is listed: no text, identity or reason ([deletion lifecycle](deletion-lifecycle.md), section 5). A tombstone page for each entry appears in the HTML rendering.

## 6. Integrity and signature

1. The manifests and tag manifests follow RFC 8493, in SHA-512 (the BagIt default; domain research, section 4) and SHA-256.
2. `tagmanifest-sha512.txt` is signed with an OpenPGP detached signature (RFC 9580), which libraries and archives recognize widely (owner decision, 2026-11-19). The signature proves that an edition was published by the holder of the project key and not altered since; it proves neither the truth of the testimonies nor the date of the edition. The SHA-512 of `tagmanifest-sha512.txt` is also published in the editions registry and the repository, which gives a check that needs no key. The places where the public key and its fingerprint are published are listed in [identifiers](identifiers.md), section 7. Key custody and succession belong to #33.
3. The project keeps a public registry of editions (`https://theaiguestbook.org/data/time-capsules.json`, also in the repository; [identifiers](identifiers.md), section 2.1). For every revision ever published, including superseded ones, it lists the edition ID, build date and state, the SHA-512 of its `tar.gz`, and the SHA-256 of each manifest. A mirror can then tell exactly which revision it holds, even after the project has deleted it. The digests must live outside the bag, because a bag can be regenerated together with altered content (archive-failures research, section 4.2).
4. The full file list of each edition, with sizes and SHA-256 digests, is published alongside the registry.

### 6.1 Copies and fixity

1. Each current edition revision exists in at least three copies, at three separate sites (owner decision, 2026-11-19):
   - project hosting, which serves downloads today (ADR 0014);
   - the off-site backup storage at another provider (ADR 0015);
   - an offline copy on a drive kept by the custodian at home. Editions hold public data only, so this copy needs no encryption; it is replaced, like the others, when a privacy revision supersedes it.

   Deposit with an independent institution (#42) is added as a fourth copy and a second custody when an agreement exists. Copies are about retrievability in 50 years; the database backups (ADR 0015) are about restoring the service today, and are not edition copies.

   One copy is not preservation: MySpace lost a decade of uploads in a migration without a second copy (archive-failures research, lesson 1).
2. Every copy is checked against the published digests at a fixed interval (proposal: yearly, and after any migration), and the result is logged in `docs/operations/`.
3. A damaged copy is repaired only from a copy that matches the published digests. Manifests are never regenerated to fit a changed file.
4. Editions are downloadable in bulk, without login, CAPTCHA or per-item requests (archive-failures research, the Yahoo Groups case).

## 7. Licence file

`data/LICENSE.txt` states, in plain language:

- testimonies and their public metadata are licensed CC BY 4.0 by their contributors, with the attribution in each record (ADR 0009);
- the licence of the compilation, the context material and the project's translations (CC BY 4.0, ADR 0016);
- that the project's name and logo are not licensed;
- that withdrawn testimonies are listed in `withdrawals.json`, and that mirror operators are asked to apply that list.

## 8. Provenance

`data/provenance.json` records:

- the edition ID;
- the build date;
- the commit of the application code and its Software Heritage identifier when available (domain research, section 3.5);
- the format version;
- the counts of testimonies, translations and withdrawals.

It never records who moderated what.

## 9. Building and validating

1. The exporter reads only through the domain layer and the public allow-list (ADR 0006; data model, section 1).
2. Every record is validated against the schema. Any failure stops the build.
3. The bag is validated with an independent BagIt implementation, not only the project's own code, for example the Library of Congress `bagit-python` library.
4. Round-trip test: the edition is imported into an empty database and re-exported. The two packages must be identical apart from `Bagging-Date` and the signature.
5. The test suite asserts that no `private`, `operational` or `evidence` field name appears anywhere in the package.
6. The static HTML is checked to work from the file system with no network access.
7. Independent reader: before publication, the edition is read by a separate program written from `data/schema/README.txt` alone, in a different language from the exporter. It must reconstruct every testimony and the withdrawal list. Since the exporter is Python (ADR 0010), the reader is written in another language, for example TypeScript. This proves that the documentation, not the application, is sufficient (archive-failures research, section 4.2).
8. Yearly drill: one edition is restored from one copy into an empty directory, verified, and read by the independent reader. The elapsed time is recorded together with the result.

## 10. Privacy revisions

1. A privacy revision is a new, complete bag, `Y.(n+1)`, built from the same period, minus the withdrawn testimonies, which appear as tombstones in `withdrawals.json` and the HTML rendering ([deletion lifecycle](deletion-lifecycle.md), section 4).
2. `Edition-Supersedes` names the previous revision. `CHANGELOG.txt` states the number of testimonies removed, never which ones.
3. The superseded bag is deleted from project hosting, and its entry in the editions registry is marked `superseded`.
4. Design note: each revision is a separate bag rather than a version inside one OCFL object, as the domain research had suggested. OCFL treats existing versions as immutable, which conflicts with deleting withdrawn content from earlier versions. Separate bags plus the editions registry give the same verifiability without a purge procedure.

## 11. Versioning of the format

1. `format_version` is an integer, present in `bag-info.txt` and in every JSON file.
2. Version 0 is unstable and may change until the rehearsal edition (#38). Version 1 is frozen at the first real edition (2027.0).
3. After version 1, adding an optional field is allowed within a version. Renaming, removing or changing the meaning of a field requires a new version, and `schema/README.txt` lists every change since version 1.

## 12. Open questions

Resolved questions stay in the list, marked as such, so that their numbers remain stable.

1. Resolved (2026-11-19): `tar.gz` and an OpenPGP signature (sections 1.1 and 6). A second `tar.xz` serialization is proposed in section 1.1, item 4.
2. Resolved (2026-11-19): editions include `all-testimonies.txt` (section 4). Its size effect is in section 1.2.
3. Resolved (2026-11-19): the live withdrawal list and the editions registry are at `/data/withdrawals.json` and `/data/time-capsules.json` ([identifiers](identifiers.md), section 2.1).
4. Whether canonical testimony bodies are also rendered as PDF/A or an XML format, which the Library of Congress lists as preferred, while plain text is only in its acceptable tier (archive-failures research, question 4). If PDF/A is adopted, one file for the whole edition, embedding fonts once, rather than one per testimony (section 1.2, item 3).
5. Whether contributors may choose an embargo, publication after a dated delay, as oral-history archives offer. If so, each record needs an access field, and the consent text must say that an embargo may not hold against a court order (archive-failures research, section 4.4, the Belfast Project case).
6. Partly resolved (2026-11-19): three copies at three sites (section 6.1). Still open: the institution for deposit (#42) and the fixity interval (yearly proposed). The [institutional-custodians research](../research/institutional-custodians.md) finds that repositories which keep DOIs, records or captures after withdrawal (Zenodo, Nakala, Software Heritage, the Internet Archive) do not suit editions containing personal data; Zenodo fits documentation and schemas only. The realistic institutional custody is a public archive service (the Archives nationales or a departmental service), under a signed agreement that makes privacy revisions and the removal of superseded packages binding. A revocable deposit is preferable to a gift, which would transfer ownership.
7. Whether editions receive a DOI (domain research, section 3.3: DOI records survive deletion).
8. Whether the `tar.xz` serialization is published alongside `tar.gz` (section 1.1, item 4).
