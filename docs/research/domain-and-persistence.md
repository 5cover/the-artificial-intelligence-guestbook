# Domain names and persistent identifiers: research notes

Date: 2026-11-15

Scope: plan sections 12 (addressable testimonies), 18-20 (reference shelf, annual editions, downloads), 23 (portability), 28-30 (continuity, succession, backups) and 38 (naming) of `docs/plans/main.md`.

Method: RDAP lookups were run with curl on 2026-11-15 (times in UTC around 17:30). Facts marked [verified] come from a primary page or RDAP output that was read directly. Facts marked [secondary] come from search-result summaries or commercial and blog sources and should be checked before a purchase or a public commitment. Facts marked [unverified] could not be confirmed in this session.

## Summary of recommendations

1. Canonical domain: register `theaiguestbook.org` as the canonical domain. It was unregistered on 2026-11-15 [verified, RDAP 404]. .org is a generic TLD that is not tied to one country, which suits a bilingual international archive. The registry operator, Public Interest Registry (PIR), is a US-based nonprofit; the .org price caps were removed in 2019 [secondary].
2. Defensive registrations, all redirected to the canonical domain with permanent (301) redirects: `theaiguestbook.fr` (French-facing and an AFNIC-governed backup; unregistered [verified]), `aiguestbook.org` (short name, matching the "The AI Guestbook" alias in plan section 38; unregistered [verified]), and `theaiguestbook.com` (unregistered [verified]). `aiguestbook.com` is already registered, so do not plan around it.
3. Do not use `.io` or other vanity ccTLDs for anything that must last decades. The `.io` code is tied to the British Indian Ocean Territory, and a treaty transfer to Mauritius has been signed but its status is contested [secondary].
4. Keep the French eligibility question in view. The operator is in France, so `.fr` and `.eu` are currently available to the project, but eligibility is a condition that can be withdrawn (the UK precedent for `.eu` in 2021). Treat them as secondary names, not as the single point of failure.
5. Registrar: use an EU registrar separate from the VPS host. Shortlist Gandi, OVHcloud and Infomaniak after checking live prices yourself; this research did not verify current prices. INWX could not be checked (its official page returned 404 in the fetch). Require: one-click DNSSEC, a registrar lock, multi-year registration (AFNIC and EURid both allow 1 to 10 years [secondary]), and an account recovery path that does not depend on one person.
6. Succession: write down the registrar, the account email, the renewal dates and the recovery method in the continuity documentation (plan section 29), name a digital executor, and plan for a second registrant contact or an institutional successor. Under French law, article 85 of the Loi Informatique et Libertes allows post-mortem directives, but the status of its implementing decrees is disputed in the sources found [secondary].
7. Email: publish SPF, DKIM (2048-bit) and DMARC on the canonical domain, start DMARC at p=none with reports, then tighten. Park the defensive domains with a null SPF record and p=reject, so that nobody can spoof mail from them. The current DMARC standard is RFC 9989 (May 2026), which obsoletes RFC 7489 [verified].
8. Identifiers: use `/entries/<ID>` (not `/voices/`, which conflicts with the public terminology in plan section 38) with an opaque, non-sequential ID, assigned at publication, never reused, with no year and no sequence number exposed. Details in section 3.8.
9. Zenodo can mint DOIs for editions, but a Zenodo removal keeps the DOI, the metadata and a tombstone page [verified against Zenodo policy]. Use Zenodo only for material that will never contain personal data, or wait for legal review before depositing any edition that contains testimony.
10. ARK identifiers: arks.org states that NAANs are for "stable memory organizations" and does not address individuals [verified]. Do not claim ARK identifiers unless an institutional partner assigns a NAAN later. Use your own domain as the persistence layer.
11. Preservation: request BnF collection by writing to <depot.legal.web@bnf.fr> or using the BnF form once the site is live; .fr sites and sites whose authors are domiciled in France are in scope [verified on bnf.fr]. Archive each code release with Software Heritage and cite its SWHID.
12. Edition packaging: use one BagIt bag (RFC 8493) per annual edition for transfer, and an OCFL (1.1) object for the successive editions 2027.0, 2027.1 and so on. OCFL version directories are immutable by specification, so the withdrawal mechanism of plan section 20 needs an explicit purge procedure; that design is an open question below.

## 1. Domain names for permanence

### 1.1 TLD comparison

| TLD | Operator and jurisdiction | Who may register | Term | Notes for permanence |
| --- | --- | --- | --- | --- |
| .org | Public Interest Registry (PIR), Reston, Virginia, USA [secondary] | Anyone | Gandi and others offer 1-10 years; the gTLD 10-year ceiling applies to gTLD registry agreements generally [secondary]. The .org-specific term was not confirmed. | The 2019 renewal of the .org registry agreement (ICANN listing dated 30 June 2019) removed the price caps [secondary]. PIR said at that time it had no specific plans for price increases and would give advance notice [secondary]. ICANN's board withheld consent to the 2020 sale to Ethos Capital on 30 April 2020 and the deal was terminated [secondary]. |
| .com | Verisign (USA) | Anyone | Up to 10 years [secondary] | Verisign may raise the .com wholesale price by up to 7 percent in each of the final four years of each six-year period; the current cooperative agreement term runs to 30 November 2030 [secondary, Verisign 10-K summary]. The sources disagree on when the first increase may take effect (Verisign says the first two years of the term have no increase; NTIA cited 1 September 2026) [secondary]. |
| .net | Verisign (USA) | Anyone | Not verified | Not researched further; the same registry operator as .com. Lower priority because .com and .org are the usual defaults. |
| .fr | AFNIC, a French nonprofit association (naming charter, French jurisdiction) [verified on AFNIC site listings] | Holders resident in the EU, Iceland, Liechtenstein, Norway or Switzerland (individuals) or with a seat in those countries (companies) [secondary]. Sources differ: one says residence, another says "citizen or permanent resident". | 1 to 10 years [secondary, AFNIC charter 2025 summary] | Renewal is tacit by default unless the registrar asks for deletion [secondary, AFNIC charter]. A 30-day redemption period follows expiry [secondary]. The .fr zone has been DNSSEC-signed since 2010 [secondary, AFNIC announcement]. AFNIC can suspend or delete a domain whose holder data cannot be substantiated [secondary]. Google treats a ccTLD as a strong signal that the site targets that country [verified, Google Search Central]. |
| .eu | EURid, Belgium-based registry for the European Union | EU and EEA citizens wherever they live, residents of those countries and organisations established there [secondary, EURid timeline and summaries] | 1 to 10 years [secondary, EURid timeline: multi-year registrations from April 2011] | DNSSEC enabled June 2010 [verified, EURid timeline]. UK citizenship alone lost eligibility after Brexit; affected domains were suspended on 1 January 2021 and withdrawn in mid 2021 [secondary]. This is a concrete precedent for eligibility being withdrawn. |
| .io | NIC.IO, delegated to the British Indian Ocean Territory code | Anyone at second level; 1 to 5 year terms [secondary, Wikipedia .io] | 1 to 5 years [secondary] | See 1.2. Not recommended. |

### 1.2 New gTLDs and vanity ccTLDs

The `.io` case is the clearest example. The code IO is an ISO 3166-1 code for the British Indian Ocean Territory [verified, Wikipedia .io]. The UK and Mauritius signed an agreement on 22 May 2025 for sovereignty to pass to Mauritius, with the handover taking effect when the agreement enters into force [verified, Wikipedia .io summary]. Secondary reporting from April 2026 says the UK froze the plan because the US did not support it [secondary, Domain Incite]. If the IO code is removed from ISO 3166-1, IANA rules may require the .io domain to be phased out over at least five years, although exceptions have been granted before (for example .su) [verified, Wikipedia .io summary]. The registry's ownership has changed several times (Afilias in 2017, Donuts in 2020, Ethos Capital in 2021) and a 2021 complaint sought repatriation of the domain [verified, Wikipedia .io summary]. The price of about US$36 per year is dated (2023) [secondary].

New gTLDs carry a different risk: the operator can fail. ICANN's Emergency Back-End Registry Operator (EBERO) program takes over only the five critical registry functions and does not provide extra services such as hosting [secondary, ICANN EBERO page]. In March 2024 ICANN placed `.nowruz` into the program after its operator failed a contractual performance threshold [secondary, ICANN announcement]. The lesson for this project is to avoid small new gTLDs for a decades-long identifier.

Vanity .ai, .co, .me and .tv names carry the same kind of risk, and .ai was not researched in depth here. Google does not treat some widely used ccTLDs (.io, .co, .me, .tv) as country signals [secondary].

### 1.3 Registration terms, renewal and grace periods

- ICANN's Redemption Grace Period is 30 days after deletion, then Pending Delete for 5 days, then release on a first-come basis [verified, ICANN registrant FAQ].
- Registrars must send reminders around expiry, but ICANN does not fix the length of a registrar's auto-renew window; the registrar's terms govern it [verified, ICANN registrant FAQ].
- gTLD renewals are capped at a total of 10 years from the time of renewal, and this cap is in the new gTLD registry agreement [secondary, ICANN registry agreement text as summarized in search].
- AFNIC: a .fr domain can be renewed for 1 to 10 years, and the total may not exceed 10 years from the order date [secondary, AFNIC charter and guide summary].
- Recommendation: take the longest term the registrar offers, with auto-renew on, and set calendar reminders on the registrar account for 60 and 15 days before expiry. A decade-long prepaid term reduces dependence on one card but still needs a human who can receive registrar email.

### 1.4 Locks

- Registrar lock (clientTransferProhibited and related client statuses) is set by the registrar and can usually be removed by the account holder in the control panel [secondary].
- Registry lock (serverTransferProhibited and related server statuses) is set by the registry and removable only through the registry's own verification, usually routed through the registrar [secondary].
- Observed: the RDAP record of `aiguestbook.com` (registered 2025-08-18, expiring 2027-08-18, nameservers at DomainControl) shows four client statuses (clientDeleteProhibited, clientRenewProhibited, clientTransferProhibited, clientUpdateProhibited) [verified]. The RDAP record of `nic.fr` shows server-side statuses (serverTransferProhibited, serverDeleteProhibited) [verified], so server-side locks do exist in the .fr registry.
- Recommendation: enable the registrar lock on day one. Ask each shortlisted registrar whether a registry lock is available for `.org` and `.fr` and at what cost; this was not verified.

### 1.5 DNSSEC

- .fr: signed since the 2010 deployment [secondary, AFNIC announcement]. .eu: enabled at the registry in June 2010 [verified, EURid timeline]. .org and .com: not separately verified here.
- Registrars: Gandi's domain page excerpt describes one-click DNSSEC activation on the domain [verified, Gandi domain page excerpt]. OVHcloud's English domain page lists DNSSEC as offered and describes it as protecting against cache poisoning and traffic diversion [verified, OVH EN page excerpt], but its French page presents DNSSEC only as a separate network-protection product [verified]. Infomaniak's official .org page, as quoted in search results, says DNSSEC is included at no extra charge [secondary, not read in full].
- Recommendation: enable DNSSEC at the registrar, verify the DS record from an external resolver after the first change, and keep the DNSSEC key holder and the DNS host documented in the continuity file. A broken DS record makes validating resolvers fail, which is hard to diagnose from the outside.

### 1.6 Registrar comparison

| Registrar | Ownership and location | Features verified | Price status | Notes |
| --- | --- | --- | --- | --- |
| Gandi | Founded in April 2000. Private equity (Montefiore) acquired it in 2019; Total Webhosting Solutions (Your.Online) acquired it in February 2023 [verified, Wikipedia Gandi citing press release of 2023-02-10]. | One-click DNSSEC activation; registration term 1 to 10 years [verified, Gandi domain page excerpt and FAQ excerpt]. Registrar lock and renewal options were not shown in the fetched excerpt, so they must be checked on the live site [unverified]. | Gandi raised prices in June 2023 and removed previously free mailboxes [verified, Wikipedia citing Gandi News FAQ 13 June 2023]. The fetched Gandi domain page lists .fr at EUR 6.00 registration and EUR 23.98 renewal, and .eu at a EUR 3.99 promotional registration and EUR 30.00 renewal; the renewal figures look high and must be checked on the live page [unverified]. | Strong French track record, but the ownership change and the 2023 price changes are the relevant history. No 2024-2026 ownership change was found in this research. |
| OVHcloud | French, large listed group [secondary] | Registrar lock, DNSSEC and auto-renewal described on the English domain page [verified]. | The English page showed prices in USD (the site currency selector) and did not show .fr or .org in the excerpt [verified]. No official domain price-change notice was found. | Price tables could not be retrieved in a verifiable form. Verify live prices. |
| Infomaniak | Swiss registrar accredited by ICANN [verified, Infomaniak domains page]. Not in the EU, but .fr and .eu eligibility depends on the holder, not the registrar. | One-click DNSSEC on the .org page as quoted in search results [secondary]. Transfer, WHOIS lookup and bulk mode [verified]. | Prices are excluding VAT in EUR; the official .org page quoted by search results shows about EUR 9.20 first year and EUR 13.70 renewal [secondary, not read in full]. The fetched pages did not yield prices. | Good candidate if DNSSEC and privacy of holder data are priorities. |
| INWX | German registrar | Not verified. | Not verified. | The fetch of the official page returned 404; it was not compared. |

The registrar should be a different company from the VPS host, so that a single hosting failure or account lockout does not take down the domain, the mail and the website together.

### 1.7 Succession: what happens when the registrant dies or is incapacitated

- Nothing happens automatically at the registrar while billing is active. Auto-renew continues. Once payment fails, the domain expires, then goes through the registrar's renewal window, then the ICANN Redemption Grace Period of 30 days and Pending Delete of 5 days [verified, ICANN; secondary for typical registrar windows].
- The practical obstacle is the registrant's email account and the registrar login. ICANN transfer rules require confirmation by the registrant or a secure process for a change of registrant [secondary]. Registrars typically ask for a death certificate and proof of authority, such as a will, letters of administration or a court order [secondary]. Policies differ by registrar.
- AFNIC treats death of the holder as a case of forced transfer ("transmission forcee") and uses a Demande d'Operation Afnic (DOA) with a signed attestation of authority, plus supporting documents [secondary, AFNIC procedures guide and a 2016 registrar document]. AFNIC also publishes a practical guide for heirs (edition 2024, title verified; content not read) [verified title].
- French law: article 85 of the Loi Informatique et Libertes (added by the 2016 Loi pour une Republique numerique) lets a person write general directives, which may be registered with a CNIL-certified trusted third party, and particular directives, registered with each controller. A person may also be named to carry out the directives. Without directives, heirs may exercise rights needed to settle the estate [secondary]. One legal guide says the CNIL noted on 3 February 2025 that these provisions were not applicable for lack of implementing decrees; other sources treat them as in force. This must be checked on Legifrance or the CNIL site before relying on it [unverified].
- Recommendation:
  - Put the registrar account on a role mailbox (for example, a project address on the canonical domain) whose recovery codes and 2FA devices are stored in a sealed envelope or a password manager with emergency access.
  - Record in the continuity file (plan section 29): every domain, the registrar, the account holder, the expiry date, the DNS host, the mail host and the recovery route.
  - Name a digital executor in a written will or an article 85 directive, and tell that person where the recovery material is. Do not store credentials in the archive repository.
  - Prefer a multi-year prepaid term and a payment method that does not depend on one person.
  - Plan an institutional successor (association, archival partner) that can hold the registrant role later, which plan section 29 already anticipates.

### 1.8 Email authentication prerequisites

- SPF (RFC 7208, Proposed Standard, April 2014) lists the hosts allowed to send for the domain [verified, rfc-editor].
- DKIM (RFC 6376, September 2011, Internet Standard STD 76) signs messages with a key published in DNS [verified, rfc-editor].
- DMARC (RFC 9989, May 2026, Proposed Standard, obsoletes RFC 7489 and RFC 9091) tells receivers what to do with mail that fails SPF and DKIM alignment, and where to send reports [verified, rfc-editor]. The p tag takes none, quarantine or reject.
- Google's bulk-sender rules apply to senders above 5,000 messages per day to Gmail accounts, require SPF or DKIM plus DMARC with at least p=none, require DKIM keys of at least 1024 bits (2048 recommended), and require From-domain alignment [verified, Google support page].
- Recommendation: even at low volume, publish SPF (ending in -all or ~all), a 2048-bit DKIM key and DMARC p=none with rua reports. After four to six weeks of clean reports, move to quarantine and then reject. For the defensive domains, publish a null SPF record (v=spf1 -all) and DMARC p=reject so that they cannot be used to spoof the project. The "null SPF plus p=reject" pattern for non-sending domains is common practice; it was not separately sourced here.

### 1.9 SEO and the choice of TLD

- Google documents ccTLDs as a strong signal that a site targets one country, and recommends subdirectories or separate URLs with hreflang for multiple languages or countries under a generic TLD [verified, Google Search Central multi-regional guidance]. The page does not say a TLD is a ranking factor [verified].
- Implication: a canonical `.org` with `/fr/` and `/en/` paths (or equivalent) and hreflang annotations matches a bilingual international archive better than `.fr` as the main domain, which would signal France as the target country.
- The name itself matters more than the TLD for SEO. "AI guestbook" is already used by several unrelated products: hospitality guestbooks (myguestbook.ai, RedAwning) and guestbooks for AI agents (robocfo.ai, hosette.net) [secondary, search results]. The full name "The Artificial Intelligence Guestbook" in the title tag and on-page copy is more distinctive; "The AI Guestbook" should be used as the alias, as plan section 38 already says.

## 2. Name candidates and RDAP results

Candidate names follow plan section 38: full name "The Artificial Intelligence Guestbook", short name "The AI Guestbook", and a French variant based on "livre d'or" (guestbook) and "intelligence artificielle". Apostrophes are not valid in a domain label, so the French variant drops the apostrophe; hyphenated and unhyphenated forms are both offered for readability and to test availability.

Proposed candidates (8 to 15 requested, 14 shown with defensive variants):

1. theaiguestbook.org (canonical, full name)
2. theaiguestbook.fr (French-facing defensive, redirect)
3. theaiguestbook.com (defensive, redirect)
4. theaiguestbook.net (defensive, optional)
5. theaiguestbook.eu (secondary and defensive; RDAP not verified, see below)
6. aiguestbook.org (short name, redirect)
7. aiguestbook.fr (short name, French)
8. aiguestbook.net (short name, optional)
9. aiguestbook.eu (short name; RDAP not verified)
10. livredor-ia.org (French variant, "livre d'or IA")
11. livredor-ia.fr (French variant)
12. livredoria.fr (French variant, no hyphen; checked)
13. livredoria.org (French variant, no hyphen; checked)
14. ai-guestbook.org (hyphenated alias)

Other checked names (not proposed): guestbook-ai.org, ai-guestbook.fr, ai-guestbook.com, ai-guestbook.net, livredor-ia.com, livredor-ia.net, livredor-ia.eu (not verified), theaiguestbook.ai and aiguestbook.ai (both 404 via rdap.org; .ai was not otherwise researched and is not recommended).

### RDAP results (checked 2026-11-15, about 17:30 UTC)

Endpoints: `https://rdap.org/domain/<name>` for gTLDs and .ai (followed with curl -L). `https://rdap.nic.fr/domain/<name>` for .fr (AFNIC). Controls: `wikipedia.org` (rdap.org) 200, `google.net` (rdap.org) 200, `afnic.fr` (rdap.nic.fr) 200, `x.ai` (rdap.org) 200. `eurid.eu` returned 404 via rdap.org, so .eu through rdap.org is not a valid control. `rdap.eurid.eu` did not resolve from this environment. `nic.io` returned 404 via rdap.org, so .io through rdap.org is not a valid control either.

| Name | Endpoint | HTTP | Raw status (RDAP) | Note |
| --- | --- | --- | --- | --- |
| theaiguestbook.org | rdap.org | 404 | none; 404 body from PIR RDAP | Likely available; RDAP 404 is not a reservation |
| theaiguestbook.com | rdap.org | 404 | none | Likely available |
| theaiguestbook.net | rdap.org | 404 | none | Likely available |
| theaiguestbook.fr | rdap.nic.fr | 404 | body: NOT_FOUND_DOMAIN_NAME_WITH_NAME | Likely available |
| theaiguestbook.eu | rdap.org | 404 | not verified | .eu RDAP not reachable; treat as unknown |
| aiguestbook.org | rdap.org | 404 | none | Likely available |
| aiguestbook.com | rdap.org | 200 | clientDeleteProhibited, clientRenewProhibited, clientTransferProhibited, clientUpdateProhibited | Registered 2025-08-18, expires 2027-08-18; registrar appears to be GoDaddy; taken |
| aiguestbook.net | rdap.org | 404 | none | Likely available |
| aiguestbook.fr | rdap.nic.fr | 404 | NOT_FOUND | Likely available |
| aiguestbook.eu | rdap.org | 404 | not verified | Unknown |
| livredor-ia.org | rdap.org | 404 | none | Likely available |
| livredor-ia.fr | rdap.nic.fr | 404 | NOT_FOUND | Likely available |
| livredor-ia.eu | rdap.org | 404 | not verified | Unknown |
| livredoria.fr | rdap.nic.fr | 404 | NOT_FOUND | Likely available |
| livredoria.org | rdap.org | 404 | none | Likely available |
| ai-guestbook.org | rdap.org | 404 | none | Likely available |
| ai-guestbook.fr | rdap.nic.fr | 404 | NOT_FOUND | Likely available |
| guestbook-ai.org | rdap.org | 404 | none | Likely available |
| livredor-ia.com | rdap.org | 404 | none | Likely available |
| livredor-ia.net | rdap.org | 404 | none | Likely available |
| ai-guestbook.com | rdap.org | 404 | none | Likely available |
| ai-guestbook.net | rdap.org | 404 | none | Likely available |
| aiguestbook.ai | rdap.org | 404 | none | .ai not otherwise researched |
| theaiguestbook.ai | rdap.org | 404 | none | .ai not otherwise researched |
| theaiguestbook.io, aiguestbook.io | not verifiable | n/a | n/a | rdap.org does not route .io; not checked |

No domain was registered, purchased or reserved in this research. "Likely available" means only that the registry returned no record at the time of the query.

## 3. Persistent identifiers and URL stability

### 3.1 Cool URIs

Tim Berners-Lee's "Cool URIs don't change" states that "A cool URI is one which does not change." It advises avoiding software details such as "cgi" or "exec" in URIs, and observes that the owner of the domain name space owns every URI in it [verified, W3C page, 1998]. Implication: the persistence of every testimony link is bounded by the persistence of the domain. The domain strategy in section 1 is therefore part of the identifier strategy.

Recommendations:

- Canonical form: `https://theaiguestbook.org/entries/<ID>`. Plan section 12 uses `/voices/` as a conceptual example, but plan section 38 says the public interface should say "entry". Prefer `/entries/`.
- No slug in the canonical path. If a readable slug is wanted, it can be accepted and redirected, but the canonical link must not depend on the title, because titles change.
- No language code in the entry path. Translations are linked from the entry page with hreflang and a visible language label.
- Old paths are kept as redirects; nothing is deleted from the URL space, only tombstoned (plan section 22).

### 3.2 ARK identifiers

- ARK syntax is ark:/NAAN/name. The NAAN identifies the naming authority and is registered with the N2T resolver [verified, n2t.net and arks.org].
- Eligibility: "Any stable memory organization may obtain a NAAN at no cost and begin assigning ARKs." The page discusses only organizations; a NAAN is meant "for an organization that directly curates or creates content" [verified, arks.org NAANs page]. Requests are processed manually.
- Minting tools such as Noid ensure that the same name string is never assigned twice [verified, arks.org].
- Recommendation: not for now. An individual operator is not clearly eligible, and the project would be dependent on a resolver that is not the project's domain. Reconsider if a university, library or association adopts the archive and can hold a NAAN. The ID scheme in section 3.8 can be adopted into an ARK later without changing the entries.

### 3.3 DOI through Zenodo

- Zenodo's DOI versioning gives a DOI for each version and a concept DOI that resolves to the latest version [secondary, Zenodo help summarized in search]. Zenodo's general policy states "Data files are versioned. Records are not versioned." and that original content is never modified [verified, about.zenodo.org/policies].
- Removal: when content is withdrawn, the policy says a tombstone page replaces it, and "The DOI and the URL of the original object are retained" [verified]. The policy also says "Records can be retracted from public view; however, the data files and record are preserved" [verified]. Content that falls outside the repository scope is removed and its DOIs revoked [verified].
- Owners can delete a record themselves within 30 days of publication; after that, a justification goes to Zenodo support [secondary, Zenodo help summarized in search].
- The policy requires that content "must not violate privacy or copyright" [verified]. It does not describe a GDPR erasure procedure. The Zenodo privacy policy was not read and is an open question.
- Implication for plan section 20: a DOI on an edition with personal data is effectively a permanent public reference to content that may later have to be withdrawn, and the metadata survives a withdrawal. Zenodo is therefore suitable for documentation, schemas, code, aggregate statistics and fully anonymised material. It is not suitable for an edition containing testimony with personal data until legal review is complete.

### 3.4 w3id.org and purl.org

- Both services were reachable on 2026-11-15 (HTTP 200 on the root) [verified].
- w3id.org is run by the W3C Permanent Identifier Community Group; a 2016 post noted there is no formal W3C maintenance commitment [secondary].
- purl.org was managed by OCLC for more than 20 years; the Internet Archive took over management of purl.org, purl.com and purl.net on 27 September 2016 [secondary].
- Recommendation: these are redirect services that the project would not control. The canonical domain is the better persistence layer. A w3id or purl alias could be added later as a secondary name if there is a concrete reason; the procedure was not verified.

### 3.5 Software Heritage

- SWHID format: `swh:1:<type>:<40 hex digits>`, for example `swh:1:cnt:94a9ed024d3859793618152ea559a168bbcbb5e2` for the GPL-3 text, the example given in Software Heritage's FAQ [verified, softwareheritage.org FAQ as quoted in search].
- The identifier is computed from content, so anyone can verify it locally with swh-identify [secondary].
- Standardisation: one source says the specification is ISO/IEC 18670 and gives April 2025 as the date; the sources differ slightly [secondary].
- Recommendation: archive the repository and each release with Software Heritage, and cite the release SWHID in the methodology and in the edition documentation. Software Heritage's save-request procedure was not verified here.

### 3.6 Internet Archive and the Wayback Machine

- web.archive.org was reachable on 2026-11-15 [verified].
- Internet Archive item identifiers are unique across the whole site, cannot be changed once set, appear in the item URL, and are recommended to be 5 to 80 characters of letters, digits, hyphen and underscore [secondary, IA developer documentation as summarized]. Choose edition item identifiers deliberately, for example with the edition number.
- Open question: the Internet Archive's removal-request process was not verified. It matters for plan section 22, because a copy held by the Internet Archive is outside the project's control.

### 3.7 BnF dépôt légal du web

- The BnF collects French websites under legal deposit. Eligible sites include .fr domains and other French extensions, and sites whose authors are domiciled in France or whose content is produced or hosted in France [verified, bnf.fr "Signaler un site web" page].
- To suggest a site: use the BnF form (up to five URLs; the email address is required) or write to <depot.legal.web@bnf.fr> [verified]. The BnF does not issue a receipt for a suggestion, and sites are not individually listed in the general catalogue [secondary, BnF help summarized in search].
- Timing: a requested site is collected within a maximum of three months [secondary]; the bnf.fr page itself gives no timeline [verified].
- Do not block the BnF crawler in robots.txt [secondary].
- Open question for legal review: how the BnF treats erasure requests for collected personal data, and how that interacts with plan section 21. The archive should expect that the BnF copy may not follow the same deletion lifecycle as the live site.

### 3.8 Identifier scheme for entries

Options compared:

| Option | Example | Pros | Cons |
| --- | --- | --- | --- |
| A. Year plus sequence, from the plan | VOICE-2027-000184 | Human readable; sorts by time; shows that the year is 2027 | The year is ambiguous (submission, publication or edition cutoff; plan section 19 says late submissions join a later period). Sequence reveals volume. If assigned at submission, gaps reveal rejected or withdrawn entries. The word VOICE conflicts with the public term "entry". |
| B. Year plus random | ENT-2027-7K2Q9M | Keeps a year for readers | Same year ambiguity; random part still needs a collision check. |
| C. Sequential, assigned at publication | ENT-000184 | Simple; no gaps from rejected submissions | Enumerable; volume visible. The public set is already enumerable, so the main leak is the count of published entries. |
| D. Opaque random, assigned at publication, with optional check character | e.g. 10 Crockford base32 characters, about 50 bits of randomness | No year, no volume, no enumeration; collisions negligible; works in print | Not sortable; less readable; sorting needs the metadata. |

Recommendation: option D for the public identifier, assigned when the entry is published, never reused, and never derived from the submission sequence. Use an internal database key for joins and an unguessable draft token for submissions before publication. Dates (submission, publication, edition cutoff) live in metadata, not in the ID. Withdrawn entries keep their ID as a content-free tombstone (plan section 22), so IDs must never be recycled. Rejected or unpublished submissions have no public ID and no public URL, so they cannot be enumerated.

Privacy point: a sequential ID exposed at submission time would let anyone who sees two IDs infer how many submissions were rejected in between. Assigning the ID at publication avoids that. An unpublished entry must return the same 404 as a nonexistent one.

## 4. Practices of long-lived archives

- arXiv: identifiers take the form YYMM.NNNNN, where the first four digits are the year and month the paper was added to arXiv; the sequence is within the month; a version suffix vN gives a unique citation, and the base ID stays the same across revisions [verified, arXiv help]. Lesson: a base identifier plus version suffix fits annual editions (2027.0, 2027.1). Embedding the year works here only because the date is the date of addition, which is a fixed, system-assigned event. The archive's year would be an edition or submission year, which is less fixed.
- Wikipedia permanent links (oldid): each revision has a stable numeric ID, and a permalink points to one saved version [secondary, Wikipedia Help:Permanent link]. Help pages say only the main text is retained and revisions can be hidden or removed [secondary]. Lesson: a stable ID does not guarantee the content stays visible; withdrawals need explicit tombstones.
- Internet Archive identifiers: unique, immutable once set, human readable, visible in the URL [secondary]. Lesson: choose edition identifiers carefully because they cannot be renamed.
- Mass Observation Archive: replies are cited by directive reply numbers (DR followed by the respondent number and the directive date) and hierarchical archive codes (SxMOA2/...); quotations carry a correspondent number in square brackets, such as [F3341] [secondary, MOA referencing guidance as summarized]. Lesson: pseudonymous contributor numbers, separate from names, with the collection's hierarchy in the code.
- BagIt (RFC 8493, Informational, October 2018): a bag has bagit.txt, a data/ directory, and manifest files with checksums; SHA-256 and SHA-512 are required and SHA-512 is the default [verified, rfc-editor]. Lesson: a self-describing transfer unit that does not need the application. Recommended for each edition as the transfer container.
- OCFL 1.1 (October 2022; 1.1.1 editorial update November 2024): each object has an inventory.json, version directories are "expected to be immutable" (section 3.3), sha512 is recommended and sha256 is also allowed, and the layout works on plain disk storage without a database [verified, ocfl.io 1.1 spec]. Lesson: OCFL keeps every edition readable without the application. Its immutability is a conflict with the withdrawal design in plan section 20: a privacy revision must remove content from earlier version directories through a deliberate purge that is recorded as a tombstone. That procedure is not defined by the spec and must be designed (open question).

Suggested edition layout (illustrative, to be refined):

- An OCFL object `the-ai-guestbook-editions`, with versions 2027.0, 2027.1 and so on.
- Each version is a BagIt bag with bagit.txt, bag-info.txt, manifest-sha512.txt and a data/ directory.
- data/ holds one JSON record per entry, public metadata, translations marked by language, reference records (plan section 18), context files, a schema document, a README explaining the archive and its licence, and a withdrawal log with tombstones and no personal data.

## Open questions

1. EURid RDAP: the .eu status of the candidate names is unknown. Check on EURid's WHOIS or RDAP service from a network that resolves it.
2. .io RDAP: not checked. Only needed if .io is ever reconsidered, which this research does not recommend.
3. Current prices: not verified for any registrar. Pull prices from each registrar's live page in EUR, excluding and including VAT, for the chosen TLDs.
4. INWX: the official page returned 404 in the fetch. Check manually if it remains on the shortlist.
5. Registry lock for .org and .fr: availability and cost at each registrar not verified.
6. Eligibility wording for .fr: the sources disagree between residence and "citizen or permanent resident". Check the current AFNIC charter (a version dated 6 July 2026 appears in search results; it was not read).
7. .org maximum registration term: not confirmed for .org specifically.
8. Verisign .com pricing: the first permitted increase date differs between Verisign's summary and NTIA's statement. .com is not the recommended canonical TLD, so this is low priority.
9. Article 85 of the Loi Informatique et Libertes: the status of its implementing decrees is disputed. Check Legifrance and the CNIL before drafting the directive.
10. Zenodo and GDPR erasure: the Zenodo privacy policy and support process were not read. Needed before any edition with personal data is deposited anywhere with a DOI.
11. BnF and erasure: how the BnF handles erasure requests for collected material. Needs legal review alongside plan section 21.
12. Internet Archive removal requests: not verified.
13. ARK NAAN for individuals: arks.org addresses organizations only. Confirm by asking the ARK Maintenance Agency if the project later wants an ARK.
14. OCFL purge procedure for privacy revisions: needs design, since the spec treats version directories as immutable.
15. Software Heritage save requests: procedure not verified.
16. w3id.org and purl.org: current maintenance commitments not verified; not needed for the recommended design.
17. AFNIC and EURid DNSSEC or lock options for individual holders: not verified in primary documents.
18. .ai: not researched beyond RDAP.

## Sources

Domains and registries

- ICANN, Expired registration and renewal FAQs for registrants: <https://www.icann.org/resources/pages/domain-name-renewal-expiration-faqs-2018-12-07-en>
- ICANN, Emergency Back-End Registry Operator: <https://www.icann.org/en/contracted-parties/registry-operators/resources/emergency-back-end-registry-operator>
- ICANN, .nowruz EBERO announcement (March 2024): <https://www.icann.org/en/announcements/details/icann-to-place-nowruz-into-emergency-back-end-registry-operator-program-03-07-2024-en>
- ICANN, .org registry agreement listing: <https://www.icann.org/en/registry-agreements/details/org>
- Domain Name Wire, .org sale terminated: <https://domainnamewire.com/2020/05/12/org-registry-sale-officially-terminated/>
- Clarivate, ICANN board rejects sale of .org PIR: <https://clarivate.com/intellectual-property/blog/icann-board-rejects-sale-of-orgs-public-interest-registry/>
- Technical.ly, PIR will no longer be acquired (Reston, Virginia): <https://technical.ly/startups/reston-org-manager-public-interest-registry-will-no-longer-be-acquired-ethos-capital/>
- NTIA, Amendment 35 to the Cooperative Agreement with Verisign: <https://www.ntia.gov/press-release/2018/ntia-statement-amendment-35-cooperative-agreement-verisign>
- Verisign 10-K (FY2024 summary via search): <https://www.sec.gov/Archives/edgar/data/1014473/000101447325000006/vrsn-20241231.htm>
- NTIA blog on .com cooperative agreement (2024): <https://www.ntia.gov/blog/2024/com-cooperative-agreement-ensuring-internet-stability-and-security>
- Wikipedia, .io: <https://en.wikipedia.org/wiki/.io>
- Domain Incite, .io safe for now as Trump puts Chagos deal on ice: <https://domainincite.com/31642-io-safe-for-now-as-trump-puts-chagos-deal-on-ice>
- EuroDNS, The End of the .IO Domain? (2026 update): <https://www.eurodns.com/blog/end-of-io-domain>
- AFNIC, Charte de nommage (2025 version, via search results): <https://www.afnic.fr/wp-media/uploads/2025/04/afnic-charte-de-nommage-2025-05-05.pdf>
- AFNIC, Guide pratique du titulaire 2024 (via search results): <https://www.afnic.fr/wp-media/uploads/2024/07/Afnic-Guide-pratique-du-Titulaire.pdf>
- AFNIC, Guide des procedures (via search results): <https://www.afnic.fr/wp-media/uploads/2022/10/Guide-des-procedures-Afnic-VF.pdf>
- AFNIC, Guide pratique a l'attention de l'ayant droit 2024 (title only): <https://www.afnic.fr/wp-media/uploads/2021/01/GuidePratique_Ayant-Droit_VF_.pdf>
- AFNIC, Signature du .fr et .re: <https://www.afnic.fr/fr/l-afnic-en-bref/actualites/actualites-operationnelles/3774/showOperational/signature-du-fr-et-re.html>
- AFNIC, Brexit and .fr domain names: <https://www.afnic.fr/en/observatory-and-resources/expert-papers/brexit-and-fr-domain-names/>
- EURid, Timeline: <https://eurid.eu/en/about-eurid/timeline/>
- Wiggin LLP, EEA citizens can register .eu (2020): <https://wiggin.co.uk/insight/eurid-confirms-that-all-eea-citizens-can-register-eu-domain-names-from-2-september-2020/>
- Gandi, Wikipedia article: <https://en.wikipedia.org/wiki/Gandi>
- Gandi, domain page excerpt: <https://www.gandi.net/en/domain>
- Gandi, changing the owner of a domain: <https://docs.gandi.net/en/domain_names/change_owner/standard_process.html>
- OVHcloud, domain page (English): <https://www.ovhcloud.com/en/domains/>
- OVHcloud, domain page (French): <https://www.ovhcloud.com/fr/domains/>
- Infomaniak, domains page: <https://www.infomaniak.com/en/domains>
- Infomaniak, .org prices page (excerpt quoted in search results): <https://www.infomaniak.com/en/domains/prices/org>

Email

- RFC 7208, SPF: <https://www.rfc-editor.org/rfc/rfc7208>
- RFC 6376, DKIM: <https://www.rfc-editor.org/rfc/rfc6376>
- RFC 9989, DMARC (obsoletes RFC 7489): <https://www.rfc-editor.org/rfc/rfc9989>
- RFC 7489, DMARC (historic): <https://www.rfc-editor.org/rfc/rfc7489>
- Google Workspace Admin Help, email sender guidelines: <https://support.google.com/a/answer/81126>

SEO

- Google Search Central, managing multi-regional and multilingual sites: <https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites>
- Search Engine Journal on ccTLD geotargeting (secondary): <https://www.searchenginejournal.com/google-uses-cctlds-search-console-settings-geotarget-search-results/205486/>
- Search results on AI guestbook products: <https://myguestbook.ai/> ; <https://robocfo.ai/ai-guestbook> ; <https://hosette.net/projects/guestbook/> ; <https://pm.redawning.com/ai-guestbook>

Persistent identifiers and archives

- W3C, Cool URIs don't change (Berners-Lee): <https://www.w3.org/Provider/Style/URI>
- ARK, NAANs and systems: <https://arks.org/about/ark-naans-and-systems/>
- N2T, ARK identifiers: <https://n2t.net/e/ark_ids.html>
- Zenodo, General policies: <https://about.zenodo.org/policies>
- Zenodo help, DOI versioning: <https://zenodo.org/help/versioning>
- Zenodo help, manage records (via search results): <https://help.zenodo.org/docs/deposit/manage-records>
- w3id.org: <https://w3id.org/>
- purl.org: <https://purl.org/>
- Software Heritage FAQ: <https://www.softwareheritage.org/software-heritage-faq/>
- Software Heritage, SWHID seminar post (2025): <https://www.softwareheritage.org/2025/11/20/swhid-seminar-post/>
- Internet Archive developer documentation, items: <https://archive.org/developers/items.html>
- Internet Archive, Wayback Machine: <https://web.archive.org/>
- BnF, Signaler un site web a la BnF: <https://www.bnf.fr/en/submitting-website-bnf>
- BnF, Dépôt légal: <https://www.bnf.fr/fr/centre-d-aide/depot-legal>
- arXiv, identifier help: <https://info.arxiv.org/help/arxiv_identifier.html>
- Wikipedia, Help:Permanent link: <https://en.wikipedia.org/wiki/Help:Permanent_link>
- Mass Observation Archive, referencing and publishing: <https://massobs.org.uk/research/referencing-and-publishing/>
- RFC 8493, BagIt: <https://www.rfc-editor.org/rfc/rfc8493>
- OCFL 1.1 specification: <https://ocfl.io/1.1/spec/>

Law

- Legifrance, loi n 78-17 (article 85), to be checked directly: <https://www.legifrance.gouv.fr/>
- CNIL, digital legacy and post-mortem directives (search results, to be checked): <https://www.cnil.fr/>
- Donnees personnelles, deceased persons' data (secondary): <https://www.donneespersonnelles.fr/donnees-personnes-decedees>
