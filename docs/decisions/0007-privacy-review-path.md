# 0007. Privacy review path for the MVP

Status: Accepted (2026-11-15)

Issue: #34

## Context

The plan makes a GDPR review a release requirement (plan sections 10, 21, 36). Minors and possible special-category self-disclosure raise the stakes. Options considered: drafts plus the CNIL PIA tool plus a paid lawyer review; drafts plus self-review only; a pro bono or law clinic review.

## Decision

For now: legal documents are drafted in `docs/legal/`, the DPIA is run through the CNIL's PIA tool, and the owner performs a structured self-review against the checklist in [the legal research](../research/legal-landscape.md). The approach is informed by how comparable independent projects handle it ([research](../research/custodial-indie-projects.md)).

## Consequences

- The residual legal risk is carried by the operator. The research must therefore be primary-source based and flag uncertainties explicitly.
- The pre-launch gate (#34) remains mandatory: no public collection before the self-review passes.
- Revisit this decision if the research shows a specific question (for example minors, or irrevocable licences versus withdrawal) that self-review cannot responsibly settle; a targeted paid consultation on that question alone may then be proportionate.
