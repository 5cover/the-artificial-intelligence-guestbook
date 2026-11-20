# Browsing, search and filters

Status: Accepted (2026-11-20)

Issue: #27

Basis: plan section 13; [editorial principles](../constitution/editorial-principles.md), "Presentation"; [privacy assumptions](../constitution/privacy-assumptions.md) 7; [data model](data-model.md); [privacy research](../research/privacy-failures.md), sections 3 and 4.5 (R27.1 to R27.10).

Visitors choose what to look for: chronological browsing, full-text search and filters. There is no ranking, recommendation, "related testimonies" or personalized feed (editorial principles, "Presentation" 1). Anonymity fails through combinations of ordinary attributes (privacy research, lessons 1 and 2). Because every public field is published in the index, that risk is handled by what is published, not by the filters (sections 3 and 4).

## 1. Browsing

1. The default listing shows published testimonies newest first. Each item shows:
   - an excerpt;
   - the original language;
   - the publication date, to the day (owner decision, 2026-11-19; the testimony page shows the day anyway, so a coarser listing date protected nothing);
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

Filters are a convenience, not a privacy control (owner decision, 2026-11-19). Every public field is already shown on its testimony page and listed in the public index (`/data/testimonies.json` and each edition's `index.json`), so anyone can filter the full set offline. Hiding rare values or counts in the interface would not protect an author, and would leave the guestbook unsearchable in its first months. Privacy is decided earlier, by which fields are public at all and by the contribution form (section 4).

### 3.1 Filters offered

Every public field with a controlled vocabulary is a filter: original language, translation language, country, field, relationship to AI, organization type, age range, frequency of AI use, self-described attitude, AI-authorship category, and edition period. Free-text fields (profession, organization, region, and the `_note` fields) are reached through full-text search, not filters.

1. A filter value with no matching testimony is not offered. There is no other threshold.
2. Filters combine freely with each other and with a search query.
3. Counts may be shown.
4. Nothing is ever derived or filtered that the contributor did not state, in particular no inferred special-category data (legal research, section 3).
5. A region filter is a deferred decision, to reconsider once enough testimonies give a region ([proposals README](../proposals/README.md), deferred decisions).

### 3.2 Search engines and archiving

1. Filter and search result pages carry `noindex`, so that combinations are not crawled or archived as pages of their own. Testimony pages and the plain chronological listing are indexable.
2. Filter URLs use stable, readable parameters, but are not permanent URLs ([identifiers](identifiers.md)).

## 4. Where privacy is decided

The interface cannot protect a combination of fields that the archive publishes. Protection comes from what is published and how the contributor is asked:

- every identity field is optional, and empty by default;
- the consent text explains that each detail makes identification easier (privacy research, section 5);
- minors' testimonies publish no age, link, organization or region ([data model](data-model.md), section 2.4);
- a field too identifying to publish should not be public at all; hiding it from filters would not help.

## 5. Editions

1. Editions contain each testimony's public fields as published (archive format).
2. `index.csv` and `index.json` list testimonies with their public fields. Aggregate statistics, if added, are computed from the same public data.

## 6. Open questions

- Resolved (2026-11-19): no threshold, no excluded filters (section 3).
- Resolved (2026-11-19): no region filter; a region filter is a deferred decision.
- Resolved (2026-11-19): dates to the day on listings and testimony pages.
