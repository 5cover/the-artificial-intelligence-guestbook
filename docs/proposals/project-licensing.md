# Licences for the project's own material and for editions

Status: Concluded by [ADR 0016](../decisions/0016-project-licensing.md) (2026-11-19)

Issue: #43

Basis: [ADR 0009](../decisions/0009-testimony-licensing.md) (testimonies are CC BY 4.0, and the owner's own intellectual property stays separate); [archival model](../constitution/archival-model.md) (mirrors are welcome); [legal research](../research/legal-landscape.md), section 11.

Today the whole repository is MIT-licensed by its single `LICENSE` file, including `docs/`. ADR 0009 settled the testimonies. This proposal settles everything else.

## What needs a licence

| Material | Where it lives | Today |
| --- | --- | --- |
| Application code | Repository | MIT |
| Documentation (plan, constitution, decisions, specs, research, procedures) | `docs/` | MIT, by accident of the single `LICENSE` file |
| Context documents and reference records (plan sections 16, 18) | Repository (Markdown) and editions | Undecided |
| Website design: templates, CSS, illustrations | Repository | MIT if committed |
| Name and logo | Everywhere | Not licensed by MIT, which covers copyright, not trademarks |
| Translations of testimonies produced by the project | Database and editions | Undecided. Derivative works of CC BY material (CPI art. L112-3, secondary source). |
| Each edition as a compilation | Edition packages | Undecided. The edition may be protected by the EU database right of its maker (Directive 96/9/EC), so mirrors need a licence for the compilation itself. |

## Options and recommendations

### L1. Application code

Recommendation: keep MIT. It is permissive and well understood, and anyone can rebuild the site, which serves the replaceable-application principle (ADR 0006).

### L2. Documentation, context documents and reference records

| Option | Effect |
| --- | --- |
| A. CC BY 4.0 (recommended) | Same licence as the testimonies, so an edition has one licence for all its text. Institutions and mirrors may reuse the context material with attribution. |
| B. CC BY-SA 4.0 | Reuses must stay open, but this adds friction to mixing with the CC BY testimonies. |
| C. All rights reserved | Maximum control, but editions would then contain material mirrors cannot lawfully redistribute, contrary to the archival model. |

Recommendation: A. The plan and the constitution are part of the documentation. Under A they become reusable too, which is consistent with the project's transparency, but it is the owner's choice. A variant keeps `docs/plans/` and `docs/constitution/` all rights reserved.

### L3. Website design

Recommendation: templates and CSS are code, so MIT, like L1. A distinctive logo or illustrations, if any, are excluded from MIT and listed as all rights reserved. The name "The Artificial Intelligence Guestbook" and the logo are not licensed for use as identifiers of another project. That needs no registration, just a notice.

### L4. Project translations of testimonies

Recommendation: CC BY 4.0, crediting the original contributor (per their chosen identity) and the translator (person, or "the project", or the named machine system). This matches the original's licence and the multilingual principles.

### L5. Editions as compilations

Recommendation: CC BY 4.0 for the edition as a whole. CC BY 4.0 also licenses sui generis database rights. Its section 1 defines them as rights "resulting from Directive 96/9/EC", and section 4 grants the right "to extract, reuse, reproduce, and Share all or a substantial portion of the contents of the database". Verified in the legal code on 2026-11-15: <https://creativecommons.org/licenses/by/4.0/legalcode.en>. One licence then covers the compilation, the testimonies, the context material and the project translations, and mirrors need to read only one licence.

## Implementation if adopted

1. The `LICENSE` file stays MIT for code. A `LICENSE-docs` file (CC BY 4.0) covers `docs/`, unless the variant of L2 is chosen.
2. The README states which licence covers what.
3. Optional: adopt the FSFE REUSE specification (machine-readable licence information per file). This is a well-known standard for exactly this situation, at the cost of a small header or a `REUSE.toml` file. Verify the current specification version before adopting it.
4. Each edition carries a `LICENSE.txt` stating:
   - the licence of the compilation (CC BY 4.0);
   - that testimonies are CC BY 4.0, each with its attribution;
   - the licence of the context material;
   - that the name and logo are excluded.
5. An ADR records the decisions.

## Open questions

- Whether L2 should cover the plan and constitution, or exclude them.
- Whether to adopt REUSE.
