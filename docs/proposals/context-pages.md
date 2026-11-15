# Context pages: scope, first set and editorial rules

Status: Proposal - awaiting owner review (2026-11-15)

Issue: #36

Basis: plan sections 2.2, 16 and 17; [editorial principles](../constitution/editorial-principles.md), "Context"; [external archives](../constitution/external-archives.md); [data model](../specs/data-model.md), section 2.14; [archive format](../specs/archive-format.md) (context documents ship as HTML and plain text).

Context exists so that a future reader can understand what the contributors were describing. Its test: does a future reader need this to understand the testimonies and the world in which they were written (plan section 2.2)? It is selective, dated and maintainable by one person. It is not an encyclopedia, and it does not argue with the testimonies.

## Editorial rules

1. **Dated, not timeless.** Every page states when it was written and last revised, and describes the situation "as of" that date. Revisions are visible in a short changelog at the bottom. An edition freezes the version current at its build.
2. **Describe, do not adjudicate.** Pages report what was claimed, adopted, disputed and feared, with attribution, not which side was right. Testimonies are never cited as evidence that a view is correct or mistaken.
3. **Sourced and referenced.** Every factual claim cites a source. Lasting sources come from the reference shelf (#37), and contemporary press is acceptable when dated. Where a specialist archive covers a topic well, the page summarizes it and points to it (external archives, principle 1).
4. **Short.** Proposal: a target of 600 to 1,500 words per page. A topic that needs more is split, or delegated to a reference.
5. **Bilingual.** English and French versions are written and reviewed by a person. Machine translation may assist but is not published unreviewed (multilingual principles).
6. **Plain language.** Written for a reader who knows nothing of 2020s technology, avoiding jargon or defining it.
7. **Project material.** Context pages are licensed under the decision of #43 (CC BY 4.0 proposed), and authored as Markdown in the repository (ADR 0010 follow-up).

## Proposed first set

The plan's minimum for the MVP (section 16), ordered by how much a reader of early testimonies needs them.

| Slug | Page | Scope | Out of scope |
| --- | --- | --- | --- |
| `what-ai-means-here` | What "AI" means in this archive | The everyday sense of the word in the mid-2020s: chat assistants, image and voice generators, recommendation systems, coding agents. How the meaning shifted. | Technical history of the field |
| `how-people-met-ai` | How people encounter AI | Chat interfaces, assistants built into phones, office and search software, workplace tools, school use; free and paid access | Product reviews, market share figures beyond a mention |
| `systems-and-interfaces` | Important systems and interfaces | The handful of products and interface patterns most testimonies will mention, named and dated, each linked to an external record | A model database (delegated to the reference shelf, plan section 16) |
| `work-education-creativity` | Effects on work, education and creative activity | Adoption, displacement fears, cheating and assessment debates, creative-industry disputes, as reported at the time | Economic forecasting |
| `controversies` | Major societal controversies | Copyright and training data, misinformation and generated media, safety and risk debates, labour conflicts, companionship and dependence | Taking sides |
| `law-and-policy` | Law and regulation | The EU AI Act and other major frameworks, enforcement milestones | Legal analysis |
| `vocabulary` | Vocabulary | Terms a future reader will meet in testimonies ("prompt", "hallucination", "agent", "slop" and so on), each with its contemporary sense and a dated example | An exhaustive glossary |
| `chronology` | A concise chronology | Dated public events that shaped how people understood AI, one line each, with sources | Technical milestones of interest only to specialists |
| `about-the-reference-shelf` | Where to learn more | An introduction to the reference shelf (#37) and how to use it | |

Later candidates, once testimonies show what readers need: regional differences, AI companionship, public opinion over time, scams and generated content, attitudes towards automation.

## Maintenance

- Proposal: each page is reviewed yearly before the edition ([recurring duties](../operations/recurring-duties.md)), and when a major event makes it misleading.
- A page that can no longer be maintained is frozen with a note giving its last revision date, rather than left to decay silently (continuity, "Design for one person" 3).

## Open questions

- Who writes the pages: the owner alone, invited writers credited by name, or drafts by AI tools with disclosed AI involvement, mirroring the authorship disclosure required of testimonies.
- Whether context pages should carry their own authorship disclosure, which would be consistent with the project's stance on AI involvement.
- The target length and the first set.
