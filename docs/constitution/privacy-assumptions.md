# Privacy assumptions

Status: Draft, awaiting owner ratification

These are design assumptions, not legal conclusions. Their legal grounding is being established in [the legal research](../research/legal-landscape.md) and must be validated before launch ([ADR 0007](../decisions/0007-privacy-review-path.md)).

## Principles

1. **GDPR is a product requirement.** The project is operated from France by a private individual who is the data controller. Privacy is designed in, not added in a footer.
2. **Three separate layers.** Private account identity, optional public contributor information and the entry itself are distinct. Authentication never implies public identity.
3. **Collect the minimum.** The account holds only what login and withdrawal require: an email address and operational timestamps. No names, photos or profile data from identity providers. No behavioural analytics, no advertising, no third-party trackers.
4. **Public means public.** Before submitting, a contributor is told plainly that the entry is intended for public access and long-term historical preservation, including in downloadable editions that others may copy.
5. **Voluntary self-disclosure is legitimate.** A contributor may write about their own health, beliefs, disability, sexuality, work difficulties or other personal matters when it is relevant to their testimony. The consent flow is designed for that, with the care special-category data requires.
6. **Other people's privacy is protected.** Contributors are warned not to reveal private or sensitive information about identifiable third parties. Moderation enforces this.
7. **Anonymity is real.** Anonymous and pseudonymous entries must not be re-identifiable through the platform: no public account linkage, no granular filter combinations, no metadata that the contributor did not choose to publish.
8. **Private data never enters archives.** Account emails, authentication data, IP-derived data, moderation notes, privacy requests and secrets are excluded from every export by construction.
9. **Rights are operational.** Access, rectification, withdrawal and deletion have working mechanisms and documented procedures, not just a contact address.
10. **Few systems hold personal data.** Every system that holds it is listed, with its retention period, so that deletion can propagate without archaeology.
11. **EU processing.** Personal data is processed and stored in the EU, with processors under written agreements.
12. **Minors are included, carefully.** Young people may contribute. Where the law requires parental or guardian authorization, a distinct flow obtains it. The flow must be proportionate and must not pretend the problem does not exist.

## Known open questions

The legal basis for each processing purpose, the treatment of special-category data, age thresholds by country, retention obligations that may apply to hosts of user content, and the interaction between withdrawal and any licence granted for archival redistribution. These are tracked in issues #11, #12, #17 and #18.
