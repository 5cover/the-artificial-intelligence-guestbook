# Browsing, search and filters

Status: Draft (2026-11-15). Items marked "Proposal" need owner review.

Issue: #27

Basis: plan section 13; [editorial principles](../constitution/editorial-principles.md), "Presentation"; [privacy assumptions](../constitution/privacy-assumptions.md) 7; [data model](data-model.md); [privacy research](../research/privacy-failures.md), sections 3 and 4.5 (R27.1 to R27.10).

Visitors choose what to look for: chronological browsing, full-text search and filters. There is no ranking, recommendation, "related testimonies" or personalized feed (editorial principles, "Presentation" 1). The privacy risk is that filters and counts narrow a set until a person stands out. Anonymity fails through combinations of ordinary attributes (privacy research, lessons 1 and 2).

## 1. Browsing

1. The default listing shows published testimonies newest first. Each item shows:
   - an excerpt;
   - the original language;
   - the publication month and year (R27.6);
   - the attribution chosen by the contributor;
   - labels for any available translations.
2. Order: by publication day, ties broken by public ID, never by submission order or any hidden score (R27.7).
3. Pagination is by page number. There is no infinite scroll, so pages stay citable and archivable.
4. The testimony page shows the publication day, for citation, but never a time of day.

## 2. Full-text search

1. PostgreSQL full-text search over the current public text and the published translations (data model, section 7). The `french` and `english` configurations are used for those languages, `simple` for others.
2. Matching is by the search engine's ranking within the results only. There is no popularity or engagement signal.
3. No autocomplete or suggestions drawn from testimony text.
4. Name search covers only display names that contributors chose to publish (R27.8). Nothing links an anonymous or pseudonymous testimony to an account or to other testimonies.
5. Search queries are not logged with any identifier. Search is rate-limited like other dynamic endpoints (threat model, section 3.4).

## 3. Filters

### 3.1 Allowed and excluded filters

| Filter | Allowed | Notes |
| --- | --- | --- |
| Original language | Yes | |
| Translation available in language | Yes | |
| Country | Yes | Country level only (R27.5) |
| Region | Proposal: no filter at first | Only once its values pass the threshold. Region also appears on testimony pages only under the same rule (data model, section 2.4). |
| Field (controlled list) | Yes | Not combined with country (R27.4) |
| Relationship to AI | Yes | |
| Frequency of AI use | Yes | |
| Self-described attitude | Yes | |
| AI-authorship category | Yes | |
| Edition period (year) | Yes | |
| Age range | No | R27.4. Also, minors have no public age at all (data model, section 2.4.1). |
| Organization, organization type | No | Too identifying in small sets (R27.4) |
| Profession (free text) | No | Free text is searchable through full-text search only |
| Any special-category inference | No | Never derived, never filtered (legal research, section 3) |

### 3.2 Thresholds

1. Proposal: N = 10. A filter value is offered only when at least N published testimonies match it (R27.1).
2. A combination of filters, or of filters and a search query, whose result has fewer than N testimonies is not shown. The page says "too few testimonies match these criteria to show them", without revealing how many (R27.2).
3. Counts are not displayed. A value is either offered or not. This avoids differencing attacks, where comparing two counts before and after a withdrawal reveals the removed testimony (R27.3).
4. Thresholds are computed on the published set only, and recomputed on each publication or withdrawal.

### 3.3 Search engines and archiving

1. Filter and search result pages carry `noindex`, so combinations are not crawled or archived. Testimony pages and the plain chronological listing are indexable.
2. Filter URLs use stable, readable parameters, but are not permanent URLs ([identifiers](identifiers.md)).

## 4. What thresholds cannot do

Thresholds protect the browsing interface, not the testimony page. A testimony page shows what its contributor chose to publish, however rare that combination is. In the first months every combination is rare. The protection for an individual therefore comes from the contribution form:

- every identity field is optional, and empty by default;
- the consent text explains that each detail makes identification easier (privacy research, section 5);
- region is withheld from public display until enough testimonies share it.

## 5. Editions

1. Editions contain each testimony's public fields as published (archive format). The filter thresholds do not alter records.
2. `index.csv` and `index.json` list testimonies, not aggregates. Any aggregate statistics added to an edition (for example counts per country) apply the same threshold, with values below N suppressed (R27.10).
3. A test cross-tabulates the exported fields used by aggregates against the threshold.

## 6. Open questions

- The value of N, and whether rarely populated filters should exist at all (privacy research, question 1).
- Whether region should ever be published (section 3.1).
- Month and year on listings with the day on the testimony page (proposed), or month only everywhere (privacy research, question 4).
