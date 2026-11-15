# 0009. Testimonies are licensed CC BY 4.0, separately from the project's own intellectual property

Status: Accepted (2026-11-15)

Issue: #11

## Context

Contributors own the copyright (droit d'auteur) in what they write, and French moral rights cannot be transferred. To publish, translate, redact and redistribute testimonies in editions and mirrors, the project needs permission from each contributor. The [legal research](../research/legal-landscape.md), sections 10 and 11, found that:

- a written, scoped grant is advisable under French copyright formalism;
- CC BY 4.0 cannot be revoked for people who already received the work, so licence and GDPR withdrawal operate on different axes;
- fully AI-generated text may not be protected by copyright at all.

The owner chose CC BY 4.0 and asked that the project's code, website design and other personal intellectual property stay separate from licensed contributor content.

## Decision

1. **Contributors keep their copyright.** Nothing is assigned to the project.
2. **Public licence.** On publication, each testimony's text is licensed by its contributor under Creative Commons Attribution 4.0 International (CC BY 4.0). Attribution follows the contributor's chosen public identity: real name, pseudonym, or "Anonymous". Public metadata published with a testimony is released under the same licence.
3. **Project grant.** At submission, the contributor also grants the project a non-exclusive, free, worldwide permission covering what the project itself must be able to do: store and moderate the submission; publish, index and display it; produce and display labelled translations; redact it for moderation or privacy reasons with a visible notice; include it in archival editions and deposit those editions with archival institutions. The contributor declares that the text is theirs to license (or that AI involvement is disclosed), and that publishing it does not infringe someone else's rights. The project is never obliged to publish a submission.
4. **Withdrawal is separate from the licence.** Withdrawal is a privacy right handled by the [deletion lifecycle](../constitution/deletion-philosophy.md). The consent text explains plainly that withdrawal removes the testimony from everything the project controls, but cannot revoke the CC BY licence for copies already obtained by others.
5. **Separation from the project's own IP.** The CC BY licence covers testimonies and their public metadata only. It does not extend to the project's code, website design, name, logo, documentation or context material, which belong to the owner. Testimonies are never stored in the source repository. Editions carry a licence file that states which licence covers which part.

## Consequences

- Grant and licence texts must be drafted in French and English (#19). They will be clearer for being short.
- Each testimony's licence and attribution string are stored with it and exported in editions.
- Translations produced by the project are derivative works. Their own licence is decided with the project's material (#43).
- Open, to be decided separately (#43): the licence of project-authored context material and documentation, of the website design, and of the edition as a compilation. The edition as a whole may also be protected by the EU database right of its maker (Directive 96/9/EC), so mirrors need an explicit licence for the edition itself, not only for its individual testimonies. CC BY 4.0 also covers database rights, which makes it a natural candidate for the edition compilation.
- The repository is currently MIT-licensed as a whole, including `docs/`. Whether documentation and design assets should stay under MIT is part of #43.
