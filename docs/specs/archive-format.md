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
  tagmanifest-sha512.txt
  tagmanifest-sha512.txt.sig          detached signature (section 6)
  data/
    README.txt                        what this archive is, in English
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
    index.json                        list of testimonies with summary fields
    index.csv                         the same, for spreadsheets (RFC 4180)
    withdrawals.json                  withdrawal list (section 5)
    context/
      <slug>.<language>.md            context documents as authored (CommonMark)
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

Serialization for download: Proposal: a POSIX `tar` archive (pax format) compressed with gzip (RFC 1952), named `the-ai-guestbook-2027.0.tar.gz`. Both are readable by standard tools on every common system.

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

## 3. Testimony record

One JSON object per testimony, `data/testimonies/<public-id>.json`. Field names and values are the `public` fields of the [data model](data-model.md). Absent optional fields are omitted, never written as `null`, so that "not given" is unambiguous.

```json
{
  "format_version": 0,
  "public_id": "7q4km2xd",
  "url": "https://theaiguestbook.org/testimonies/7q4km2xd",
  "language": "fr",
  "published_on": "2027-03-14",
  "edition_period": 2027,
  "licence": "CC-BY-4.0",
  "attribution": "Anonymous",
  "citation": "Anonymous, testimony 7q4km2xd, The Artificial Intelligence Guestbook, 2027-03-14. https://theaiguestbook.org/testimonies/7q4km2xd",
  "redacted": false,
  "body": "Texte du témoignage...\n\nDeuxième paragraphe.",
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
      "source_version": 1,
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

## 5. Withdrawal list

`data/withdrawals.json` lists every testimony withdrawn from any earlier edition or revision, up to this package's build date. The live service publishes the current list at a permanent URL (proposal: `https://theaiguestbook.org/withdrawals.json`).

```json
{
  "format_version": 0,
  "generated_on": "2028-02-01",
  "withdrawals": [
    { "public_id": "9xk3m2pa", "withdrawn_in": "2027-06", "editions": ["2026-rehearsal.1"] }
  ]
}
```

Nothing else is listed: no text, identity or reason ([deletion lifecycle](deletion-lifecycle.md), section 5). A tombstone page for each entry appears in the HTML rendering.

## 6. Integrity and signature

1. `manifest-sha512.txt` and `tagmanifest-sha512.txt` follow RFC 8493. SHA-512 is the BagIt default (domain research, section 4).
2. Proposal: `tagmanifest-sha512.txt` is signed with an OpenPGP detached signature (RFC 9580), which libraries and archives recognize widely. The public key is published in the repository, on the website and in each edition's `README.txt`. Key custody and succession belong to #33.
3. The project keeps a public registry of editions (proposal: `https://theaiguestbook.org/time-capsules/editions.json`, also in the repository). It lists every revision ever published, including superseded ones, with its edition ID, build date, state and the SHA-512 of its `tar.gz`. A mirror can then tell exactly which revision it holds, even after the project has deleted it.

## 7. Licence file

`data/LICENSE.txt` states, in plain language:

- testimonies and their public metadata are licensed CC BY 4.0 by their contributors, with the attribution in each record (ADR 0009);
- the licence of the compilation, the context material and the project's translations (decided in #43; CC BY 4.0 proposed);
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

- Package serialization (`tar.gz` proposed) and signature scheme (OpenPGP proposed).
- Whether editions also include a single concatenated plain-text file of all testimonies, for readers without any tooling.
- The permanent URLs of the live withdrawal list and the editions registry. They extend the [identifiers](identifiers.md) spec once decided.
- Lessons from the archive-failures research, to be incorporated.
