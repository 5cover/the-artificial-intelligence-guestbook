# 0006. The archive is the primary deliverable; the application is replaceable

Status: Accepted (2026-11-15)

Issue: #13

## Context

The plan requires that the archive can survive the application and that a future custodian need not resurrect the production stack to understand the testimonies (plan sections 19, 23). When asked to choose a stack, the owner stated that the site is not the primary deliverable, the archive is, and that the site should be replaceable by design. A "static public site plus small API" architecture was considered; its lessons are kept without necessarily adopting it.

## Decision

1. The canonical archive format is specified first and independently of any application ([#13](https://github.com/5cover/the-artificial-intelligence-guestbook/issues/13), `docs/specs/archive-format.md`). It uses simple, documented formats: structured records, plain text, manifests, checksums and schema documentation.
2. The application database is an operational store. Its job is to collect, moderate and serve testimonies, and to export them losslessly to the canonical format.
3. Public pages for published testimonies are designed to be cacheable and reproducible as static HTML, so that editions can ship a static rendering and the live site can be rebuilt by another implementation.
4. Stable identifiers and URLs belong to the archive, not to the application's routing or database keys.

## Consequences

- The stack decision (#7) becomes less consequential: any stack that can implement the spec and its export is acceptable.
- The export is part of the core, tested continuously, not an annual afterthought. A round-trip test (export, re-import or validate) is a requirement.
- Some duplication between the database schema and the archive schema is accepted as the price of independence.
