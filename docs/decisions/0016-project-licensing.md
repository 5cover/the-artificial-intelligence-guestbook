# 0016. Licences for the project's own material and for editions

Status: Accepted (2026-11-19)

Issue: #43

## Context

[ADR 0009](0009-testimony-licensing.md) licensed testimonies under CC BY 4.0 and kept the owner's own intellectual property separate. Until now the single MIT `LICENSE` file also covered `docs/` by accident. The options are in [project licensing](../proposals/project-licensing.md). The owner accepted every recommendation as written on 2026-11-19.

## Decision

1. **L1, code:** MIT.
2. **L2, documentation, context documents and reference records:** CC BY 4.0, including the plan and the constitution (no exclusion).
3. **L3, website design:** templates and CSS are code, under MIT. A distinctive logo or illustrations, if any, are all rights reserved. The project's name and logo are not licensed for use as identifiers of another project.
4. **L4, project translations of testimonies:** CC BY 4.0, crediting the original contributor (per their chosen identity) and the translator (a person, "the project", or the named machine system).
5. **L5, editions as compilations:** CC BY 4.0 for the edition as a whole, which also licenses the sui generis database right (CC BY 4.0 sections 1 and 4).

The REUSE specification, offered as optional in the proposal, is not adopted for now.

## Consequences

- `LICENSE` stays MIT; `LICENSE-docs` carries the CC BY 4.0 legal code for `docs/`; the README states which licence covers what.
- Each edition's `data/LICENSE.txt` states one licence, CC BY 4.0, for the compilation, the testimonies, the context material and the translations, and excludes the name and logo ([archive format](../specs/archive-format.md), section 7).
- Anyone may republish the plan and the constitution with attribution.
