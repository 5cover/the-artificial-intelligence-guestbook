# Interpretability dependencies of an edition

Status: Living report (first version 2026-11-19). Diagnostic only.

Basis: [archive format](../specs/archive-format.md); [data model](../specs/data-model.md); [archival model](../constitution/archival-model.md); [archive-failures research](archive-failures.md).

What a future reader must already understand, or be able to recover, to interpret an edition without the project, its software or its people. Every archive depends on shared conventions, and depending on them is not a defect. The purpose of this report is to keep those dependencies visible.

This report has no authority over the architecture. It recommends a change only where a significant interpretability burden can be avoided at minimal cost to the project. It is reviewed whenever the archive format changes, and with the yearly calendar review ([recurring duties](../operations/recurring-duties.md)).

## 1. Dependencies, from the outside in

Assessments are inference unless a source is given. "Carried in the edition" means the edition itself explains or contains what is needed.

| # | Layer | Dependency | Needed for | Durability assessment | Carried in the edition |
| --- | --- | --- | --- | --- | --- |
| 1 | Medium | A readable storage medium and file system | Everything | Outside the project's control; addressed by copies and migration (archive format, section 6.1) | No |
| 2 | Package | `tar` and `gzip` (proposed) | Opening the package | Decades of use, simple, many independent implementations | No; the README of an unpacked copy cannot explain how to unpack itself |
| 3 | Characters | Unicode, UTF-8 and NFC normalization | Every text file | UTF-8 dominates text interchange; its encoding rules are short | No |
| 4 | Text layout | Line feed as line end, blank line as paragraph separator | Reading bodies | Trivial to infer from the content | Partly: `schema/README.txt` |
| 4a | Light markup | CommonMark 0.31.2, declared in each record (`body_format`) | Reading emphasis, headings, lists and links in bodies | Readable as plain text even if the convention is forgotten, because the marks resemble their meaning; the specification is licensed CC BY-SA 4.0 and could be included | Variant declared; specification not yet included (see section 2) |
| 5 | Language | English and French, as written in the 2020s | READMEs, labels, testimonies | Long-lived and heavily documented, but drifts over centuries | The testimonies themselves are in many languages, by nature |
| 6 | Package structure | BagIt (RFC 8493) | Knowing which files belong and verifying them | A small, stable IETF specification used by libraries and archives | No (see section 2, item 1) |
| 7 | Integrity | SHA-512 and SHA-256 | Verifying files | Standardized and widely implemented; collision resistance may weaken over a long horizon, verification by recomputation stays possible | No |
| 8 | Authenticity | OpenPGP signatures (RFC 9580, proposed) and the project's public key | Proving the edition is the project's | Depends on surviving tooling and on the key being published elsewhere | Public key only |
| 9 | Records | JSON (RFC 8259) | Machine reading of testimony records | Ubiquitous today; the grammar fits on a page | No |
| 10 | Record meaning | JSON Schema draft 2020-12 | Validating records, knowing field types | Less durable than JSON itself; the meaning is also described in prose | Prose in `schema/README.txt` (archive format, section 9, item 7) |
| 11 | Tables | CSV (RFC 4180) | Index files | Ubiquitous, with dialect variations | No |
| 12 | Presentation | HTML and CSS | The browsable rendering | Ubiquitous; the plain-text copies make it non-essential | No; plain text is the fallback (archive format, section 4) |
| 13 | Calendar and time | Gregorian calendar, UTC, ISO 8601 date notation | Every date | Very durable, internationally standardized | Stated in the README (data model, section 1.3) |
| 14 | Codes | BCP 47 language tags, ISO 3166-1 country codes | Language and country fields | Codes change over time (countries split, merge and are renamed) | Plain-text labels give English names next to codes (archive format, section 4); the code tables themselves are not included |
| 15 | Vocabulary | The project's controlled codes (`assisted-language`, `relationship_to_ai` values...) | Structured fields | Exists only in this project | Labels in plain text; definitions in `schema/README.txt` |
| 16 | Identifiers | Crockford base32 public IDs, `https` URLs, the domain | Citation, linking | IDs are self-contained; URLs depend on the domain surviving (ADR 0008) | The ID syntax is documented in the README |
| 17 | Licence | CC BY 4.0 and the legal systems that give it effect | Lawful reuse | Widely adopted; legal interpretation can drift | The licence file states it; the legal code is linked, not included (see section 2, item 3) |

## 2. Cheap mitigations, for consideration

These are candidates, not decisions. Each would be decided in the archive format (#13).

1. **Include short, freely licensed specifications as plain text** in `data/schema/standards/`: RFC 8493 (BagIt), RFC 8259 (JSON), RFC 4180 (CSV) and the CommonMark 0.31.2 specification (CC BY-SA 4.0, per spec.commonmark.org; licence to confirm before inclusion). IETF documents may be reproduced in full without modification under the IETF Trust Legal Provisions (recollection, to verify before adoption). Their combined size is small. ISO standards (ISO 8601, ISO 3166) cannot be redistributed, so they are summarized in prose instead.
2. **Describe the record format in prose** independently of JSON Schema, which the archive format already requires through the independent reader.
3. **Include the CC BY 4.0 legal code** as a plain-text file, as the repository now does in `LICENSE-docs`, instead of only linking to it.
4. **Include a code table** for every language and country code used in the edition, with English and French names, so that later code changes do not orphan old values.
5. **A single plain-text file of all testimonies**, already an open question in the archive format (section 12), removes the dependency on JSON and on file-system layout for the most important content.

## 3. Not mitigated, and why

- The medium, the package format and UTF-8 cannot be explained from inside the package that depends on them. Copies, migration and institutional deposits address them instead.
- Natural language cannot be removed as a dependency. The editions are written in two widely documented languages.
