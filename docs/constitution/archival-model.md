# Archival model

Status: Draft, awaiting owner ratification

> The guestbook stays open. At the end of each year, we preserve a time capsule of what people had written and of the world they were writing about.

## The guestbook and the time capsules

1. The guestbook is the living collection. It never closes for submissions.
2. A time capsule is an annual edition: a dated snapshot of everything eligible that entered the archive by its cutoff. Entries received afterwards are fully valid and belong to the next period.
3. The first major edition has a cutoff of 2027-12-31. At least one rehearsal edition is produced before it.

## What an edition contains

Published entries, their public metadata and authorship declarations, translations intended for archival publication, contextual material, reference shelf records, relevant primary artifacts where redistribution is lawful, provenance information, documentation of the archive and its schema, manifests and checksums.

## Properties

4. **The archive is the primary deliverable.** The application is a replaceable front end ([ADR 0006](../decisions/0006-archive-first-replaceable-application.md)).
5. **Independently intelligible.** An edition can be understood without the live website, the production stack or the founder. Formats are simple, open and documented.
6. **Stable identity.** Every entry has a permanent identifier independent of its state, URL or the application's database. Identifiers are never reused.
7. **Revisable for privacy.** An edition is versioned (for example `2027.0`, `2027.1`). A privacy revision may remove withdrawn material and replace it with a content-free tombstone. The fact that a revision happened, and why in general terms, is recorded.
8. **Verifiable.** Editions ship with checksums, and the project publishes what each edition contains so that copies can be checked.
9. **Mirrors are welcome, with honesty about limits.** People and institutions may download and keep copies. The project publishes a machine-readable list of withdrawn identifiers so mirror operators can update their copies. The project does not claim it can remotely delete independent copies.
10. **Private data is excluded by construction.** Exports never contain account data, moderation notes, privacy requests, logs or secrets.

## Not yet decided

Exact formats, packaging, identifier syntax and where editions are deposited. Tracked in #13, #15, #38 and #39.
