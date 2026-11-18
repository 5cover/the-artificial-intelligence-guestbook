# 0013. Legal bases, identification-data retention and minors

Status: Accepted (2026-11-18)

Issue: #12, #17

## Context

The privacy notice, the register, the DPIA and the consent texts (#19) all depend on the legal positions taken for the processing. The options and their reasoning are in [legal bases, retention duty and minors](../proposals/legal-bases-and-minors.md), drawing on the [legal research](../research/legal-landscape.md). None of this is legal advice; the review path is [ADR 0007](0007-privacy-review-path.md).

The owner reviewed D1 to D7 on 2026-11-18. Three questions changed the outcome: whether the Guestbook is a hosting provider for decree 2021-1362 (D2), whether a per-country age table could be kept current (D4), and how heavy the explicit-consent statement must be (D6).

## Decision

1. **D1, legal bases.** As in the proposal's table: art. 6(1)(b) for the account (6(1)(f) as fallback), art. 6(1)(a) consent for publication and each optional public field, art. 9(2)(a) explicit consent for sensitive self-disclosure, art. 6(1)(f) or (c) for moderation records, withdrawal evidence and security logs. No reliance on art. 6(1)(e), the art. 17(3)(d) archiving exemption or Loi I&L art. 80.
2. **D2, decree 2021-1362: option C.** No raw IP addresses are collected at submission or kept in proxy logs; anti-abuse uses keyed, rotating hashes. No civil identity is collected. The account email is kept for one year after account closure in a restricted store, used for nothing else and disclosed only to a judicial authority on request.
3. **D3, DSA.** The service is treated as an information society service and a hosting service, and so as an online platform: a notice mechanism (art. 16), statements of reasons (art. 17) and terms describing restrictions (art. 14). This is the same assumption that makes the decree apply under D2; the two positions are taken together.
4. **D4, age threshold: 16 for everyone.** GDPR art. 8(1) lets member states lower the age from 16 but never raise it, so 16 cannot fall below any national threshold and needs no monitoring. No per-country table is kept. There is no minimum age: below 16, the parental path applies.
5. **D5, parental path.** As recommended: an age gate (under 16 or not, no exact age); below 16, a parent's or guardian's email, a magic link, and a confirmation page where the parent states their authority and may read the testimony; the parent's email deleted once consent is recorded. Testimonies from under-16 contributors publish no age, no link, no organization, no region and no real-looking display name, and are moderated strictly. Every minor makes a separate, unprompted choice to publish, and a minor's withdrawal prevails over a parent's consent.
6. **D6, explicit consent: one merged statement.** The explicit consent is part of the publication statement, in a single sentence such as "Publish my testimony in the guestbook, including anything personal it reveals about me", linked to the privacy notice, which names the sensitive categories. The honest-limit statements of the proposal (anonymity towards the public only, legal access, stylometry, mirrors, backups) are shown before submission, with the short stylometry warning for anonymous and pseudonymous contributors.
7. **D7, DPIA.** A DPIA is carried out with the CNIL PIA tool before launch and records these positions and their reasoning.

## Consequences

- The legal drafts (#19) can start: privacy notice, register, DPIA, consent and parental-flow texts.
- The retention schedule keeps row 5 (account email, one year after closure) and can be finalized (#18).
- The data model records the age band against a fixed threshold of 16, with no country, and records the merged statement as both the publication and the explicit consent.
- French 15-year-olds go through the parental path, at the cost of one email to a parent.
- Questions for the paid consultation (ADR 0007): whether minimising collection satisfies the decree (D2), whether a free, non-commercial archive is an information society service at all (D2, D3), whether the merged sentence is explicit enough for art. 9(2)(a) (D6), and the proportionality of the parental check (D5).
- Revisit if the project ever takes revenue (which strengthens the information society service reading), if the follow-up to loi 2026-813 on minors and social networks reaches this kind of service, or if the consultation disagrees with any position.
