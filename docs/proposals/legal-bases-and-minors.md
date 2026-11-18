# Legal bases, retention duty and minors

Status: Concluded by [ADR 0013](../decisions/0013-legal-bases-and-minors.md) (2026-11-18)

Issues: #12 (legal bases and minors policy), #17 (age and parental-consent flow), #18 (retention, partly)

Basis: [legal research](../research/legal-landscape.md), sections 2 to 6 and 10 (research, not legal advice); [privacy assumptions](../constitution/privacy-assumptions.md); [data model](../specs/data-model.md); [ADR 0007](../decisions/0007-privacy-review-path.md) (drafts plus CNIL PIA plus self-review). Once decided, the answers become an ADR, feed the DPIA and the privacy notice (#19), and fix the retention schedule (#18).

Each decision lists options and a recommendation. Uncertain legal points are marked, and none of this replaces a lawyer's review.

## D1. Legal basis for each processing purpose

| Purpose | Recommended basis | Alternatives | Why |
| --- | --- | --- | --- |
| Account and email (sign-in, withdrawal channel) | Art. 6(1)(b), necessary for the service the person asks for | 6(1)(f) legitimate interest (security) | The account is objectively needed to contribute and to withdraw. Consent is wrong for something the user cannot refuse and still use the service (legal research, section 2). Uncertain whether "contract" fits a free service. 6(1)(f) is the fallback and gives the same practical result. |
| Publishing the testimony | Art. 6(1)(a) consent | none | Consent is the only basis that fits unconditional withdrawal (legal research, section 2). |
| Sensitive self-disclosure in the text | Art. 9(2)(a) explicit consent, for every submission | Art. 9(2)(e) "manifestly made public" | Any text may contain it, so the explicit consent is asked of everyone, as a separate statement. 9(2)(e) is a weak fallback after the CJEU's broad reading of indirect revelation (C-184/20). |
| Optional public metadata | Art. 6(1)(a) consent, per field | none | Each field is withdrawable on its own (deletion lifecycle, section 1). |
| Moderation records, notices | Art. 6(1)(f); 6(1)(c) where LCEN or DSA duties apply | none | |
| Withdrawal evidence | Art. 6(1)(c) or (f) | none | Minimal record only (data model, section 2.12). |
| Security logs, rate limits | Art. 6(1)(f) | none | Keyed hashes with a rotating salt; no raw IP addresses (data model, section 2.16). |
| Archival editions | Consent at submission, plus the honest notice about mirrors | Art. 17(3)(d) archiving exemption | The archiving exemption needs art. 89 safeguards and a "serious impairment" test, and is risky for sensitive data. Recommended: no reliance on it; withdrawal is always honoured for copies under the project's control (deletion philosophy). |

Not used: art. 6(1)(e), because a public task must be laid down by law and no law gives this archive one. Loi I&L art. 80 ("expression littéraire") is not relied on either, since its application to a testimony archive is untested (legal research, section 2).

Recommendation: adopt the table as written.

## D2. Decree 2021-1362 (retention of identification data by hosts)

Whether a non-professional operator hosting submitted testimonies is a "fournisseur de services d'hébergement" under the decree is uncertain and decisive (legal research, section 6). If it is, the decree requires keeping:

- account identifiers for one year after closure (art. 3);
- civil identity data for five years, if collected (art. 2);
- connection data (IP address and port) for one year per content creation (art. 5).

Only data the operator actually collects is covered (art. 8).

The notion is defined by reference: LCEN art. 6 I 2 points to DSA art. 3(g)(iii), "the storage of information provided by, and at the request of, a recipient of the service", within an information society service. The definition does cover any site that stores what its users submit, by design. So the question is not whether the Guestbook stores testimonies at contributors' request, which it does, but whether a free, non-commercial archive run by an individual is an information society service at all. That is the same question as D3, and the two answers must agree: assuming the DSA applies (D3) means assuming the decree applies too (legal research, section 6, follow-up of 2026-11-18).

| Option | Effect |
| --- | --- |
| A. Assume the decree applies in full | Keep the account email one year after closure; collect and keep raw IP addresses at each submission for one year. More personal data, held longer, contrary to minimisation. |
| B. Assume it does not apply | Simplest. If the assumption is wrong, the operator risks a penalty (LCEN art. 6 V B, up to one year and EUR 250,000) for failing to produce data to a judicial authority. |
| C. Minimise on the merits, and comply cheaply with what remains (recommended) | Do not collect raw IP addresses at submission. They are not needed for the service: anti-abuse uses keyed, rotating hashes. Art. 5 then has nothing to apply to. Keep the account email for one year after closure in a restricted store, used for nothing else and disclosed only to a judicial authority on request. That covers art. 3 at a small privacy cost. Collect no civil identity, so art. 2 has nothing to apply to. Record the position and its reasoning in the DPIA. |

Owner: C accepted (2026-11-18), on the grounds that it is cheap.

Recommendation: C. Proxy logs must then not store raw IP addresses either (retention schedule, #18). Whether minimising collection is compatible with the decree's purpose is itself uncertain (legal research, section 6, open questions). This is the first question for any paid consultation (ADR 0007).

## D3. Treating the service as an online platform under the DSA

Whether a free, non-commercial archive is an "information society service" at all is uncertain (legal research, section 5).

Recommendation: assume the DSA applies, as the legal research does. The cost is small and the duties match the constitution anyway:

- a notice mechanism for illegal content (art. 16);
- a statement of reasons when content is restricted (art. 17);
- terms describing the restrictions (art. 14).

The micro-enterprise exemption removes the heavier platform duties (art. 19). The protocol for illegal content is #41.

## D4. Age thresholds

GDPR art. 8 lets each member state set the age of digital consent between 13 and 16. France sets 15, with joint consent below that (Loi I&L art. 45, CNIL Recommendation 4). Plan section 11 wants a French contributor who can consent alone not to be forced through the parental flow. The member-state table in the legal research is secondary and partly inconsistent (Denmark, for example).

| Option | Effect |
| --- | --- |
| A. 15 for everyone | Simple and matches the controller's law. But it may fall below the threshold of a contributor's own country (16 in several states), and the applicable-law question is uncertain. |
| B. 16 for everyone | Safe everywhere in the EU, but forces 15-year-olds in France through the parental flow, contrary to plan section 11. |
| C. Threshold by declared country of residence, from a verified table, with a default of 16 (recommended) | France: 15 (verified through the CNIL). Each other country gets its own threshold once it is verified against national law; until then it gets the GDPR default of 16. Non-EU residents get 16. |

Owner: B accepted (2026-11-18). GDPR art. 8(1) lets member states lower the age from 16 but never raise it, so 16 can never fall below a national threshold and needs no monitoring. No authoritative, maintained table of national thresholds was found. The cost is that French 15-year-olds go through the parental path. The per-country table below is not built.

Recommendation (superseded by the owner's choice): C. The table lives in the code and in `docs/legal/`, with the source of each entry. It grows as entries are verified, and starts with France only.

Also decide whether there is a minimum age below which no one may contribute, even with parental consent.

- Recommended: no hard minimum. The parental path applies below the threshold. Plan section 3 says anybody can express themselves, and section 11 says young people should not be excluded merely because their participation creates work.
- Alternative: a minimum of 13 even with consent, which is simpler to moderate.

## D5. Parental consent and verification

CNIL Recommendation 7 endorses no single method. It calls email checks and self-declaration easily circumvented, excludes purely declarative systems for higher-risk processing, and asks that verification data be deleted after the check (legal research, section 4). Every cheap method is therefore weak, and every strong one (identity documents, third-party verification) is disproportionate for a free archive and excludes families without those means.

Recommended: risk reduction by design, so that a light verification is proportionate.

1. **Age gate before the form:** the contributor declares their country and whether they are under the threshold for that country. No exact age is asked.
2. **Parental path below the threshold:**
   - the contributor gives a parent's or guardian's email address;
   - the parent receives an explanation in plain language and a magic link;
   - on the confirmation page, the parent states that they hold parental authority and agrees to the publication, and can read the testimony first;
   - the other holder of parental authority is presumed to agree, and the notice explains how they can object (CNIL Recommendation 4);
   - the parent's email is deleted once the consent is recorded (data model, section 2.8).
3. **Restrictions on what an under-threshold testimony may publish:**
   - identity mode `anonymous` or `pseudonymous` only;
   - no `link`, `organization`, `region` or `display_name` that looks like a real name (a moderator check);
   - no age or age range shown at all, since an "under-18" label would itself mark a minor ([privacy research](../research/privacy-failures.md), R17.2).

   Even if the age declaration or the parental consent were false, the published testimony then carries little that could identify or endanger a child.
4. **Moderation:** every under-threshold testimony is read with the third-party and self-identification rules applied strictly. The moderator can ask for changes rather than reject.
5. **Contributors from the threshold up to 17:**
   - the normal flow applies;
   - no age or age range is shown;
   - an additional warning appears about publishing their real name;
   - the accelerated erasure right (Loi I&L art. 51 II) is explained to them.
6. **Neutral choice for every minor:** a self-declared minor's testimony stays unpublished until they make a separate, explicit choice to publish. Nothing is pre-selected and no screen nudges towards publication ([privacy research](../research/privacy-failures.md), R17.1 and R17.7, drawing on the DPC's TikTok decision).
7. **The child's withdrawal prevails** over the parent's consent, without any adult's approval (R17.5).

Alternatives:

- Refuse contributors under the threshold. This is the simplest option, needs no verification at all, and is what the privacy research calls the least risky (question 2). It contradicts plan section 11, which asks that young people not be excluded merely because their participation creates work.
- Accept self-declaration below the threshold, with the residual risk recorded in the DPIA. Cheaper, but CNIL Recommendation 7 excludes purely declarative systems for higher-risk processing.
- Email confirmation only, without the publication restrictions. Cheaper, but weak under CNIL Recommendation 7, with no compensating safeguard.
- Stronger verification, for example a signed form, an identity check or third-party age verification. Disproportionate and excluding. Services that store documents for age checks have been breached (privacy research, section 3, Discord and Tea), so this is itself a privacy risk.

Recommendation: the design above, documented in the DPIA as the proportionality reasoning.

Owner: accepted as recommended (2026-11-18), with the threshold of D4 (16). The verification itself is light (a declaration and a parent's email); the publication restrictions are the protection that holds even when the declaration is false.

## D6. Explicit consent wording

Recommendation: one separate, mandatory statement for every submission, distinct from the publication consent and the licence. Draft wording, to be reviewed in both languages in #19:

> I agree that my testimony, which may include information about my health, beliefs, sexuality, political opinions or other sensitive aspects of my life, is published and preserved in the archive. I can withdraw it at any time.

Owner: a lighter form accepted (2026-11-18). The explicit consent is merged into the publication statement, in one sentence such as: "Publish my testimony in the guestbook, including anything personal it reveals about me." The detail (health, beliefs, sexuality, political opinions) goes in the privacy notice, linked from the statement. A notice alone would not be consent, since art. 9(2)(a) requires an act by the person. Whether the merged sentence is explicit enough is a question for the paid consultation (ADR 0007).

The consent screen must also state the honest limits plainly, before submission. The [privacy research](../research/privacy-failures.md), section 5, gives suggested wording. In particular:

- anonymity applies towards the public, not towards the operator;
- confidentiality holds only to the extent French and EU law allow: a court or authority can lawfully obtain the account email the project holds, as the Belfast Project's interviewees learned ([archive-failures research](../research/archive-failures.md));
- writing style, described events and the people mentioned can identify an author, and machine-assisted stylometry is improving;
- each optional detail makes identification easier;
- withdrawal cannot reach copies others already hold;
- backups keep withdrawn material for the published rotation window.

Recommendation: show anonymous and pseudonymous contributors a short stylometry warning before they submit (privacy research, question 9).

## D7. DPIA

Recommendation: carry out a DPIA with the CNIL PIA tool before launch, even though the CNIL list does not name this case. Its criteria (sensitive data, vulnerable persons, publication) are present, and the legal research considers it very likely required (section 7). The DPIA records D1 to D6 and their reasoning.

## Consequences if adopted

- The [data model](../specs/data-model.md) already supports D1, D2 (option C), D4 (option C) and D5. Option C of D2 adds the restricted one-year store for account emails after closure.
- The retention schedule (#18) can be fixed.
- The legal drafts (#19) can start: privacy notice, register, DPIA, consent texts and the parental flow texts.
- The first questions for any paid legal consultation (ADR 0007) are D2 and D5.
