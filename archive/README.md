# Archive format artefacts

Machine-readable parts of the archive format, kept apart from any application code because the format must outlive the application ([ADR 0006](../docs/decisions/0006-archive-first-replaceable-application.md)).

- [schema/](schema/): JSON Schemas (draft 2020-12) for edition records. They are normative for [the archive format](../docs/specs/archive-format.md), and every edition carries a copy.

Format version 0 is unstable until the rehearsal edition (#38).
