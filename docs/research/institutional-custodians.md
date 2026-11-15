# Institutional custodians for the annual editions

Status: Research (2026-11-15)

Issue: #42

Basis: [archival model](../constitution/archival-model.md), principle 6 and "Not yet decided"; [continuity](../constitution/continuity.md), "Beyond the founder" and "If the project ends"; [archive format](../specs/archive-format.md), sections 2, 6.1, 10 and 12; [deletion lifecycle](../specs/deletion-lifecycle.md), sections 2 and 4; [custodial research](custodial-indie-projects.md), lessons 5 and 9 and the reviewer's note on lesson 1; [domain and persistence research](domain-and-persistence.md), section 3.

## 1. Scope and method

Scope: institutions that could receive a deposit of the annual editions (the BagIt packages described in the archive format), or that could become a successor custodian of the Guestbook as a whole. France is weighted. Two EU examples outside France are included because they show the same problem in another legal system.

Method: WebSearch and WebFetch, run on 2026-11-15. Each claim carries one tag. [fetched] means the cited page was opened and the statement was read there. [search] means the statement comes only from a search-result summary, or from a page that WebFetch could not open (several official sites returned HTTP 403, 404 or a connection reset: the Huma-Num and Nakala documentation, the Huma-Num presentation page, the Internet Archive help articles and the Zenodo FAQ). [inference] means my reasoning from the sources. Where a fact could not be confirmed, the note says so rather than filling the gap.

Two CNIL PDFs could not be read by WebFetch because their text is stored in compressed streams. I downloaded them and extracted the text locally with Poppler (`pdftotext`). The quotations from the CNIL documents in section 3.4 come from that extraction, and the same applies to the 2021 oral-archives guide in section 3.5. The URLs are the public ones.

No institution was contacted. Nothing here is legal advice. The legal points are for the legal review that the plan requires (#12, #19).

## 2. Summary of candidates

| Candidate | Accepts | Cost | GDPR withdrawal handling | Fit |
| --- | --- | --- | --- | --- |
| BnF, dépôt légal du web and online publications (3.1) | Crawls freely accessible French web pages. Owners may suggest URLs by email. No deposit procedure for online publications yet. | Not stated on the pages read | Harvested web archives cannot be deleted, only access restricted in exceptional circumstances. No owner removal procedure found. | Good as a passive second copy of the public pages. Poor as a custodian of a package. |
| Archives nationales, Pierrefitte (3.2) | Private archives from any holder, including associations, in any medium, born-digital included | No fee mentioned | A gift transfers ownership. A deposit is revocable. Withdrawal terms would have to be written into the signed letter or agreement. | Strongest long-term option, if it accepts an agreement with privacy revisions. Acceptance is not confirmed. |
| Departmental and municipal archives (3.3) | Private archives under a contract. COVID-19 testimony calls in 2020. | Not stated on the pages read | The contract sets the conservation and communication rules. No withdrawal precedent found. | Strong for a local, human-scale deposit. Each service decides for itself. |
| CNIL guidance on private archives (3.4) | Not an institution. It states the legal position of private archives. | Not applicable | Private owners must comply with GDPR and must justify the historical interest that supports indefinite retention. | Sets the legal frame for any deposit. |
| La Contemporaine and the MMSH phonothèque, oral archives (3.5) | Donations and deposits from researchers, associations and individuals (La Contemporaine). Deposit agreements (MMSH). | Not stated on the pages read | Donation letters. Online diffusion excluded unless agreed. The MMSH invites people to ask for withdrawal. | Good model for oral archives. Online diffusion limits conflict with an open edition. |
| Archivio Diaristico Nazionale, Italy (3.5) | Diaries and memoirs under a licence agreement, with conditions the donor can set | Participation in the prize is free. Deposit cost not stated. | Withdrawal terms not found | Possible EU option. Italian-language contract to be read. |
| Huma-Num and Nakala (3.6) | Social-science research data from French higher education and research. Administrative data excluded. | Not verified | Published data cannot be deleted by the depositor. Removal only on request to Huma-Num. The DOI and a tombstone are kept. | Poor fit without an academic partner. |
| Recherche Data Gouv (3.7) | Datasets from account holders authorised to deposit. Personal data only with consent or a legal provision. | Free up to a usage threshold | The platform can remove content without notice. A contributor's deletion request goes through the platform representative. | Possible only through an academic partner. |
| University libraries and archives (3.8) | Research data, usually from affiliated researchers | Not verified | Paris 1 guidance: consent can be withdrawn, but a withdrawal after publication can mean reversing a publication | Only through a partner project. |
| Software Heritage (3.9) | Source code and development history of public repositories | Not stated in the FAQ | Removal form with a formal request. Mirror handling not stated. | Good for the code. Not for testimonies. |
| Internet Archive (3.10) | Uploads and web captures | Not verified | Copyright removal under its policy. Personal-data and exclusion routes not confirmed. | Mirror copy only. No control over removal. |
| Zenodo (3.11) | Versioned data files, up to 50 GB per record | Free ([search]) | Owner can delete within 30 days. Later, a support request. A tombstone and the DOI remain. | Documentation, schema and code with DOIs. Not testimonies with personal data. |
| Association under loi 1901 (3.12) | Not a repository. A legal person that can hold the project. | Declaration cost not verified | Becomes controller of the data it holds, with GDPR duties | Only as a long-term successor. |

Key findings:

1. Only the Archives nationales and the departmental archives offer a documented route for a private archive to be held permanently. Both rely on a signed letter or contract, and both are the main places where the privacy revision mechanism can be written in advance. [inference] from sections 3.2 and 3.3.
2. The BnF has no procedure for a package, and it states that harvested web archives cannot be deleted. Its copy of a public page is outside the project's control. [inference] from section 3.1.
3. DOI-based repositories keep the record and the DOI after withdrawal. Their files are versioned, so the superseded package stays unless the repository intervenes. This conflicts with the design in archive format section 10, which deletes superseded bags. [inference] from sections 3.6 and 3.11.

## 3. Candidates

### 3.1 BnF, dépôt légal du web and online publications

Accepts. The BnF collects the French web under the legal deposit of the internet. The Code du patrimoine allows collection of freely accessible digital content, and the bodies may collect by automated procedures "dont ils informent les personnes" concernées, or agree the collection methods with those persons. [fetched] <https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006845522>

Accepts, for a site, the following. A site open without a password is collected automatically in general. The BnF cannot guarantee that its harvest is complete, so owners may send a URL for a future collection. No receipt is issued, and a requested site is archived within a maximum of three months. [fetched] <https://www.bnf.fr/fr/centre-d-aide/depot-legal> [fetched] <https://www.bnf.fr/en/help-center/web-legal-deposit-instructions>

Accepts, for online publications. The BnF's own page says there is currently no deposit procedure for online publications, although the obligation exists in principle. [fetched] <https://www.bnf.fr/fr/centre-d-aide/depot-legal>

Procedure. Send the URL to `depot.legal.web@bnf.fr`. The page states "You do not have to submit anything" and does not ask for files. [fetched] <https://www.bnf.fr/en/help-center/web-legal-deposit-instructions> The BnF's robot is authorised to ignore robots.txt, and the owner's only obligation is not to block it. [fetched] <https://www.bnf.fr/en/your-website-harvested-bnfs-robot>

Cost. No cost stated on the pages read. [fetched] <https://www.bnf.fr/en/help-center/web-legal-deposit-instructions>

Personal data. Harvested web content is collected under the legal deposit. The BnF's own web pages do not say how personal data in harvested pages is handled. [inference] from the absence of a stated rule.

Withdrawals. "Web archives cannot be deleted, but access may be restricted in exceptional circumstances." [fetched] <https://www.bnf.fr/en/help-center/web-legal-deposit-instructions> The page names no owner removal procedure. The BnF's BCweb contributor page gives access, rectification and deletion rights for the personal data of contributors, exercised by email with proof of identity at `depot.legal.web@bnf.fr`. That page concerns people who submit sites, not the content captured by the crawl. [fetched] <https://collecteweb.bnf.fr/legal> The general data protection contact is given as `dpd@bnf.fr`. [search] <https://www.bnf.fr/fr/politique-de-confidentialite>

Needs to provide. For a package, the BnF would need a written agreement under the agreed-modalities clause of article L132-2-1. Nothing in the sources says the BnF has used this clause for an external package. [inference]

Fit. Useful as an independent copy of the public web pages, which the BnF would collect anyway if they are linked and freely accessible. Not usable as the custodian of a downloadable edition, and its copy cannot be revised. [inference] from the statement above.

Earlier research (domain and persistence, section 3.7) gives the eligibility rule for French sites: .fr domains and sites whose authors are domiciled in France. [fetched] in that earlier pass, not re-verified here.

### 3.2 Archives nationales, Pierrefitte

Accepts. Any person or legal entity, French or foreign, may entrust private archives to the Archives nationales. Accepted holders include individuals, families, associations, companies and researchers. Accepted media include "tout type de support", with born-digital documents named. [fetched] <https://www.archives-nationales.culture.gouv.fr/particuliers-et-associations>

Procedure. Contact by email at `dap.an@culture.gouv.fr`. The proposer is put in touch with a conservateur du patrimoine, and asked for the biographical or historical elements about the producer, the volume and the content. [fetched] <https://www.archives-nationales.culture.gouv.fr/particuliers-et-associations> [search] <https://fr.wikipedia.org/wiki/Archives_nationales_de_France>

The preferred route is the manual gift (don manuel). The gift transfers the material ownership. The heirs keep the moral rights, including copyright, and control over access and use. [fetched] <https://www.archives-nationales.culture.gouv.fr/particuliers-et-associations> A search summary adds that donated archives are then protected by law as public archives. [search] <https://www.archivesnationales.culture.gouv.fr/camt/fr/egf/deposer.html> A deposit (dépôt) does not transfer ownership, is "réservée à certains cas précis (indivisions successorales)", and is revocable by nature. [fetched] <https://www.archives-nationales.culture.gouv.fr/particuliers-et-associations>

Cost. The page mentions no fee for offering archives. [fetched] <https://www.archives-nationales.culture.gouv.fr/particuliers-et-associations>

Personal data. Not addressed on the page. Donated archives are protected as public archives, which in principle places them under the Code du patrimoine regime. The consequences for personal data in testimonies need legal review. [inference]

Withdrawals. Owners sign a donation letter or a deposit agreement that sets the terms for communication, reproduction and reuse. Requests to digitise a donation are examined case by case. [fetched] <https://www.archives-nationales.culture.gouv.fr/particuliers-et-associations> A privacy-revision clause would have to be written into that document. The page says nothing on withdrawals. [inference]

Needs to provide. A donation letter or agreement, a description of the editions, the metadata (edition ID, cutoff, schema), the format rules and the list of documents with their licences. [inference]

Fit. The strongest candidate for permanent custody if it accepts the edition package with a clause on revisions. Acceptance is not confirmed, and the owner should not assume it. [inference] No Archives nationales COVID-19 testimony call was found in searches. [search] <https://www.archimag.com/archives-patrimoine/2020/03/23/memoires-confinement-projets-archivent-quotidien-coronavirus-covid-19>

The Archives nationales du monde du travail and the Archives nationales d'outre-mer have their own intake procedures, one with a committee. [search] <https://fr.wikipedia.org/wiki/Archives_nationales_de_France>

### 3.3 Departmental and municipal archives

Accepts. Departmental and municipal archives are public archive services. The CNIL's archiving schema states that public archive services may accept the documents of private archive owners to keep them under better security conditions and to make them available to the public. The rules on conservation, on access for the original owner, and on public communication "sont formalisées dans un contrat". [fetched] <https://www.cnil.fr/sites/cnil/files/2024-01/schema_archivage_des_documents_presentant_un_interet_historique.pdf>

Precedents. In March to May 2020, several services ran testimony calls for lockdown memories. The Archives départementales des Vosges started #memoiredeconfinement on 18 March 2020, promising to keep testimonies "pour l'éternité". [fetched] <https://labo.societenumerique.gouv.fr/fr/articles/comment-les-mus%C3%A9es-services-des-archives-et-la-bnf-archivent-et-documentent-la-crise-sanitaire/> The Aube archives ran theirs from 20 April to 7 May 2020. [search] <https://www.archimag.com/archives-patrimoine/2020/03/23/memoires-confinement-projets-archivent-quotidien-coronavirus-covid-19> According to a search summary, about 80 percent of the Vosges material was digital, and the digital collection was to stop after lockdown while written testimony was still accepted. [search] <https://www.banquedesterritoires.fr/covid-19-les-services-darchives-multiplient-les-collectes-de-memoires-sur-le-confinement>

Terms of the 2020 calls, from the summaries. The Vosges archives asked for testimonies by email to `vosges-archives@vosges.fr` and planned to have contributors sign an agreement. [search] <https://vosgesmag.fr/articles/articleid/15645/confinement-envoyez-vos-t%C3%A9moignages-aux-archives-d%C3%A9partementales> The Maine-et-Loire archives let contributors keep their own material or donate it, and their deposit form included a transfer of patrimonial rights. [search] <https://www.archives49.fr/le-temps-suspendu/sevader-en-famille/votre-confinement/> The Pas-de-Calais archives offered donation, deposit or a loan for scanning. [search] <https://www.archivespasdecalais.fr/Participer/Collectes-d-archives/Paroles-de-confine-e-s> The Val-de-Marne archives collected nearly 200 documents from about a hundred contributors and later published anonymised selections in virtual mini-exhibitions. [search] <https://www.valdemarne.fr/espace-presse/les-communiques-de-presse/les-archives-departementales-publient-les-temoignages-recueillis-pendant-le-confinement>

Cost. Not stated on the pages read. The 2020 calls were free to contribute to. [search] <https://www.cap-com.org/actualit%C3%A9s/les-memoires-du-confinement-les-collectivites-collectent-deja-temoignages-et-photos>

Personal data. None of the 2020 sources read describes handling of personal data, consent or removal. [search] This is the main gap. Consent texts of these calls need to be read directly from each service.

Withdrawals. No precedent found. The contract is the only instrument, and its terms vary by service. [inference]

Needs to provide. Probably the same as 3.2, plus the format rules of each service. [inference]

Fit. Good for a local, human-scale deposit and for a public face in the department. Each service decides for itself, so the owner would approach the service where the owner lives first. [inference]

### 3.4 CNIL guidance on private archives

The request was to read again the CNIL guide on definitive archiving, which an earlier pass could not read. Two CNIL PDFs were read this time, by text extraction.

The CNIL archiving schema says the following about private archives. "Il n'existe pas de règles particulières : les archives privées ne sont soumises à aucune obligation juridique de conservation et de dépôt à des fins historiques." Private owners are "libres de décider du sort des documents qu'ils détiennent" subject to data protection rules, and "En particulier, ils doivent s'assurer de l'intérêt historique des documents justifiant leur conservation sans limitation dans le temps." [fetched] <https://www.cnil.fr/sites/cnil/files/2024-01/schema_archivage_des_documents_presentant_un_interet_historique.pdf>

On private operators and public archives, the schema says that public archive services "peuvent également accueillir les documents des propriétaires d'archives privées" and that the rules are "formalisées dans un contrat". It also says that public archive services "peuvent fournir aux organismes privés des conseils en matière de sélection, de conservation et de valorisation". [fetched] <https://www.cnil.fr/sites/cnil/files/2024-01/schema_archivage_des_documents_presentant_un_interet_historique.pdf> I did not find a model convention between private operators and public archives. [search] The CNIL guide on retention periods refers to the public sector: definitive archiving "concerne uniquement les traitements mis en oeuvre à des fins archivistiques dans l'intérêt public", and the phase "concerne essentiellement le secteur public". [fetched] <https://www.cnil.fr/sites/default/files/atoms/files/guide_durees_de_conservation.pdf>

The same guide says that private bodies entrusted with a public service mission produce public archives subject to the Code du patrimoine. [fetched] <https://www.cnil.fr/sites/default/files/atoms/files/guide_durees_de_conservation.pdf> The Guestbook is not such a body. [inference] For electronic definitive archiving, the guide refers to the standard NF Z42-013. [fetched] <https://www.cnil.fr/sites/default/files/atoms/files/guide_durees_de_conservation.pdf>

Implication. A private archive with personal data may be kept indefinitely only if its historical interest is justified, and that justification has to be written down. The archive's own explanation of its historical value (the coverage statement in the archive format, section 2.2) serves this purpose. [inference] The reviewer's note on lesson 1 of the custodial research still applies: the archiving exemptions need a basis in Union or Member State law, and a private deposit does not create one by itself. [inference]

### 3.5 Oral-history and testimony collections

La Contemporaine (Nanterre). Accepts donations and deposits from a researcher, an association or a private person. The donor and the interviewees sign a donation letter and rights-assignment contracts. The donor keeps moral rights. Online diffusion is excluded unless the donor and the interviewees agree in the letter and the contracts. [fetched] <https://www.collexpersee.eu/wp-content/uploads/2021/06/Guide-sur-les-archives-orales.pdf> This is a 2021 guide, not the institution's current terms.

Phonothèque of the Maison méditerranéenne des sciences de l'homme (MMSH). Accepts oral archives deposited by researchers under a deposit agreement. Where interviewees signed nothing, the record says that rights holders are being sought. The phonothèque invites people who recognise their testimony to get in touch, to sign a rights-assignment contract or to ask for withdrawal. [fetched] <https://www.collexpersee.eu/wp-content/uploads/2021/06/Guide-sur-les-archives-orales.pdf> This is the closest precedent for the withdrawal of a testimony after publication. It is an invitation, not a procedure.

The guide also says that depositing does not automatically mean public access, and that communication can be delayed. [fetched] <https://www.collexpersee.eu/wp-content/uploads/2021/06/Guide-sur-les-archives-orales.pdf>

Archivio Diaristico Nazionale (Pieve Santo Stefano, Italy). Accepts diaries, memoirs and letter collections. A donor signs the licence agreement for creative works, which the archive requires for any submission. A donor can deposit at any time without entering the prize, and can state constraints or particular wishes, which the archive respects. [fetched] <https://www.premiopieve.it/invia-un-diario/> The page says nothing on withdrawal, and the licence is a linked PDF that I did not read. [fetched] <https://www.premiopieve.it/invia-un-diario/> The contact is given as `info@archiviodiari.it`. [search] <http://archiviodiari.org/index.php/modalita-di-donazione.html>

Fondation pour la mémoire de la déportation. Deposits originals at the Archives nationales under a deposit contract, with the foundation and the witness keeping copies. [search] <https://fondationmemoiredeportation.com/archives-orales/> The summary is from a search result and the page was not opened. The Fondation is cited here only as a precedent for deposit at the Archives nationales.

Fit. The oral-archive model fits a testimony collection, with a donation letter and a withdrawal route. The online-diffusion exclusion of La Contemporaine conflicts with an open edition unless the donation letter allows it.

### 3.6 Huma-Num and Nakala

Accepts, from the documentation summaries. Deposit requires a HumanID account and an access request, which Huma-Num treats in about one week and up to three weeks in August. [search] <https://documentation.huma-num.fr/nakala/> Eligibility: the depositor must be attached to French higher education and research, or take part in a project led by such an institution. The data must be social-science and humanities research data. Administrative or pedagogical data is not accepted. [search] <https://www.univ-smb.fr/bu/en/science-ouverte/nakala/> [search] <https://cat.opidor.fr/index.php/Nakala>

Procedure. Create a HumanID account, request access, then deposit. Publication assigns a DOI automatically. [search] <https://documentation.huma-num.fr/nakala/>

Cost. Not verified.

Personal data. The search summary of the quality page says that depositors must follow a quality-deposit training. I found no statement on personal data in the summaries, and the Huma-Num and Nakala pages could not be opened. [search] <https://documentation.huma-num.fr/nakala-qualite/>

Withdrawals. Publication is treated as final. The depositor cannot delete or unpublish a public dataset. Deletion is done on request to `nakala@huma-num.fr`, and the FAQ summary says published data is deleted only in cases of force majeure, after verification. The landing page of the deleted record stays reachable, with a deletion date and a replacement pointer. The erasure takes effect after a latency for media refresh and backup rotation. [search] <https://documentation.huma-num.fr/nakala-faq/>

Needs to provide. Metadata to Huma-Num's quality standard, and an academic link. [search]

Fit. Poor without an academic partner. Even with one, the DOI-plus-tombstone model would keep the record of each edition after a privacy revision. [inference]

### 3.7 Recherche Data Gouv (INRAE)

Accepts. Datasets from account holders authorised by the platform. A contributor is anyone with an account who is authorised to deposit, documents or publishes a dataset. The generic space is not open to private companies or foreign institutions. [fetched] <https://recherche.data.gouv.fr/fr/page/conditions-generales-d-utilisation-de-la-plateforme-de-recherche-data-gouv>

Cost. Publication is free up to a usage threshold set in a separate agreement, beyond which generic-space deposit is no longer allowed. [fetched] <https://recherche.data.gouv.fr/fr/page/conditions-generales-d-utilisation-de-la-plateforme-de-recherche-data-gouv>

Personal data. A dataset containing personal data may be published by the repository only if the persons concerned have agreed, or a legal provision allows it. The contributor is responsible for what it publishes and must tell the platform about personal data in the documentation. [fetched] <https://recherche.data.gouv.fr/fr/page/conditions-generales-d-utilisation-de-la-plateforme-de-recherche-data-gouv>

Withdrawals. The administrators may remove content without notice, challenge or appeal. Deleting a contributor's account does not delete the datasets, which are removed on the contributor's request through the platform's representative. Platform-initiated deletion requires at least three months' notice. [fetched] <https://recherche.data.gouv.fr/fr/page/conditions-generales-d-utilisation-de-la-plateforme-de-recherche-data-gouv> Contact: `support-recherchedatagouv@inrae.fr`. [fetched] <https://recherche.data.gouv.fr/fr/page/conditions-generales-d-utilisation-de-la-plateforme-de-recherche-data-gouv>

Fit. Possible only through an academic partner, because the owner is a private individual. The personal-data rule (consent or legal provision) is the same constraint as the reviewer's note. [inference]

### 3.8 University libraries and archives

Accepts. Institutional repositories are generally for researchers and projects affiliated to the university. I found no source on external depositors who are not affiliated. [search] <https://sorbonne-alliance.pantheonsorbonne.fr/sites/default/files/2026-04/2026_up1_fiche-pratique-rgpd-donnees-personnelles_ouvrir-des-donnees-de-recherche-contenant-des-donnees-personnelles.pdf> The Paris 1 institutional space asks for an account created with the university's address. [search] <https://entrepot.recherche.data.gouv.fr/dataverse/univ-paris1>

Personal data and withdrawal. The Paris 1 guide says consent can be withdrawn at any time, and that a consent that is too broad or vague does not legally secure opening the data. It adds that after publication, a withdrawal request can mean reversing published data. [search] <https://sorbonne-alliance.pantheonsorbonne.fr/sites/default/files/2026-04/2026_up1_fiche-pratique-rgpd-donnees-personnelles_ouvrir-des-donnees-de-recherche-contenant-des-donnees-personnelles.pdf> The PDF I could extract did not show these passages, so this is a search summary only.

Fit. Through a partnership with a research unit only. The owner would need an academic project, and the project's own rules would then apply. [inference]

### 3.9 Software Heritage

Accepts. The core mission is source code. Binaries are not filtered out. The archive collects everything publicly available, without preliminary tests. [fetched] <https://www.softwareheritage.org/software-heritage-faq/> Its content policy says it does not vet collected code. [fetched] <https://www.softwareheritage.org/legal/content-policy/>

Procedure. The Save Code Now form takes a public repository URL. Software Heritage supports Git, Mercurial and Subversion. [search] <https://www.softwareheritage.org/2019/01/10/save_code_now/>

Cost. Not stated in the FAQ. [fetched] <https://www.softwareheritage.org/software-heritage-faq/>

Personal data. The GDPR notice lists name, email address and developer username. Data is stored outside Europe. [fetched] <https://www.softwareheritage.org/legal/content-policy/>

Withdrawals. A removal request needs an online form, the date of the request, the identification of the requester, a description of the infringing content with its exact location in the archive, and the reasons, with legal references. Requests can also go by post to Inria. [fetched] <https://www.softwareheritage.org/legal/content-policy/> The content policy does not say whether removals apply to mirrors. [fetched] <https://www.softwareheritage.org/legal/content-policy/>

Fit. For the code of the Guestbook and its schema tooling. Not for testimonies, which are not source code. The release SWHID is the recommended citation (domain and persistence research, section 3.5). [inference]

### 3.10 Internet Archive

Accepts. Items uploaded by users and captures of public web pages by the Wayback Machine. [inference] The upload terms and the Wayback Machine collection policy were not read.

Copyright. If the Internet Archive is made aware of infringing content, it "will remove it per our Copyright Policy". The copyright agent is reachable at `info@archive.org`. [fetched] <https://help.archive.org/help/rights/> The Archive "is unable to release any contact information for patrons." [fetched] <https://help.archive.org/help/rights/>

Personal information and exclusion. The official help article for non-consensual intimate images is a dedicated form and not a general route. [search] <https://help.archive.org/help/how-do-i-request-removal-of-intimate-images-of-me-published-without-my-consent/> A general removal of personal data appears to be discretionary. [search] I did not confirm the exclusion route for the Wayback Machine. The help article titled "Publishers Blocking the Wayback Machine" exists, but its body was not opened. [fetched] <https://help.archive.org/help/rights/>

Fit. A mirror copy only. The owner would not control removal. Whether an owner can remove or replace an item they uploaded was not verified, because the help article was not opened. [inference]

### 3.11 Zenodo

Accepts. Research outputs and data files with DOIs. "Data files are versioned. Records are not versioned." Each record has a file size limit of 50 GB, with higher quotas on request. [fetched] <https://about.zenodo.org/policies/>

Cost. Free. [search] <https://www.openaire.eu/zenodo/>

Personal data. "Content must not violate privacy or copyright." Metadata is licensed CC0, except email addresses. [fetched] <https://about.zenodo.org/policies/> The Zenodo privacy policy was not read.

Withdrawals. If a record is less than 30 days old, the owner can delete it. [fetched] <https://support.zenodo.org/help/en-gb/1-upload-deposit/215-can-i-delete-my-record-after-publishing> After that, deletion needs a justification to Zenodo support. [search] <https://www.openaire.eu/zenodo-introduces-a-new-way-to-manage-and-correct-published-records> Files in a published record can be changed or removed only through support. [search] <https://help.zenodo.org/docs/deposit/manage-records> Content can be retracted from public view, but "the data files and record are preserved". The DOI and the URL of the original object are retained, and the withdrawal reason is shown on a tombstone page. [fetched] <https://about.zenodo.org/policies/>

Fit. Good for the schema, documentation, the code citation and aggregate statistics. Not for editions containing testimonies with personal data until a legal review is complete. This is the same conclusion as the domain research (section 3.3). [inference]

### 3.12 Association under loi 1901 as successor custodian

Procedure, from the text of article 5 of the loi du 1er juillet 1901. The declaration is made at the prefecture or sub-prefecture of the seat. It states the title, the object, the seats of establishments, and the names, professions, domiciles and nationalities of those who administer it. A copy of the statutes is attached. A receipt is issued within five days. The association is made public only by insertion in the Journal officiel on production of the receipt. [fetched] <https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000006294257/2014-08-02> The page shows a consolidated version in force from 2006 to 2015, so the current text should be checked before the declaration is made. The declaration may be filed online. [search] <https://associations.gouv.fr/lassociation-declaree-regie-par-la-loi-du-1er-juillet-1901> Associations with their seat in Bas-Rhin, Haut-Rhin or Moselle fall under local law. [search] <https://associations.gouv.fr/lassociation-declaree-regie-par-la-loi-du-1er-juillet-1901>

Examples. Framasoft is a loi 1901 association recognised as being in the general interest, financed mainly by donations. [search] <https://framablog.org/2021/10/12/frama-cest-aussi-des-humain%C2%B7es-qui-sassocient/> The custodial research (`docs/research/custodial-indie-projects.md`, lesson 2 and section 3.2) records Framasoft's 2019 decision to close most of its services, citing maintenance load beyond team capacity. That shows the limit of a volunteer body. [inference]

Digital-rights and digital-preservation associations were not researched beyond their names. Whether any of them would accept the Guestbook is unknown, and no contact has been made. [inference]

Fit. An association gives the project a legal person that can hold domain, hosting and data, as the continuity note requires. It becomes a controller under GDPR for what it holds, with the same duties the project has now. It would not by itself give a public-interest basis for the data. [inference]

## 4. Recommended path

Before the first edition (cutoff 2027-12-31, with a rehearsal edition first, as in the archival model):

1. Decide the consent wording for deposit, as set out in section 5. No institution should be approached before the owner has approved the text, because the answers depend on it. [inference]
2. Write to the Archives nationales (`dap.an@culture.gouv.fr`) and to the departmental archives of the owner's department. Ask in writing: whether they accept born-digital edition packages in BagIt; whether they accept a gift or a deposit with a privacy-revision clause; how superseded packages are removed; what fixity checks they run; what licence they apply; and whether there is a cost. [inference] from sections 3.2 and 3.3.
3. Write to the BnF (`depot.legal.web@bnf.fr`). Ask whether it will collect the public edition pages, and whether an agreed collection modality under article L132-2-1 is possible for an edition package. Ask how it applies removals to harvested pages. [inference] from section 3.1.
4. Test the chosen format with the rehearsal edition (archive format, section 9). Use fixture data, not real testimonies, for any deposit test. [inference]
5. Choose at least one institution and sign a written agreement before the first public edition. The agreement should cover: privacy revisions and the removal of superseded packages; the list of withdrawn identifiers; the licence; the metadata; the formats; fixity checks; named contacts; and what happens if the institution cannot keep the edition. [inference]
6. Archive the public repository with Software Heritage when it is public (section 3.9), and cite the release SWHID in the edition documentation.
7. Keep Zenodo for documentation and schema DOIs only, not for testimonies (section 3.11).
8. Consider an association under loi 1901 only if the succession plan requires a legal person (section 3.12). Read the current text of article 5 before filing.
9. Consider Huma-Num or Recherche Data Gouv only if an academic partner runs a research project that the editions can join (sections 3.6 and 3.7).

After the first edition:

1. Send the edition 2027.0 package to the agreed institution, and record the receipt and the digests in the editions registry (archive format, section 6, item 3).
2. Keep at least three copies in at least two places, as archive format section 6.1 proposes, and check each copy against the published digests once a year. Log the result in `docs/operations/`.
3. For each privacy revision, send the replacement package to the institution and ask for the superseded package to be removed. Record the request and the answer in `docs/operations/`.
4. Once a year, check that the institution's contacts and terms are still current, and update this note.
5. Keep the withdrawal list in the same form for every institution, because the list is the only mechanism that reaches mirrors that have no agreement. [inference] from archival model, principle 6.

## 5. Implications for consent text, licences and the archive format

Consent text. The text must say that editions may be deposited with public or institutional archives, which will keep copies outside the project's control. It must also say what withdrawal reaches: the project's copies, and deposited copies as far as the agreement allows. Copies already downloaded and captures by the BnF or the Internet Archive cannot be recalled. [inference] from sections 3.1 and 3.10 and the deletion lifecycle, section 2. The reviewer's note on lesson 1 applies: consent remains the workable basis until an institution with a public-interest mandate takes custody, at which point the basis should be reviewed. [inference]

Licences. Testimonies are licensed CC BY 4.0 by their contributors (ADR 0009). A donation or deposit of an edition by the project needs the contributors' licence to allow the institution to hold and redistribute it. The Archives nationales and the departmental archives also take rights through the donation letter or the contract (sections 3.2 and 3.3). I did not re-read ADR 0009 for this note, so the consent text must be checked against it. [inference] The Zenodo CC0 metadata licence does not affect the testimony text. [fetched] <https://about.zenodo.org/policies/>

Archive format. The edition must be valid BagIt with both manifests, as the spec already requires. It must carry the French and English README and the licence file, which the institutions will need. [inference] from archive format, sections 2 and 7. The institution's acceptable formats are unknown. The CNIL names the standard NF Z42-013 for electronic definitive archiving by public services, and an institution is likely to ask for it. [fetched] <https://www.cnil.fr/sites/default/files/atoms/files/guide_durees_de_conservation.pdf> [inference]

Superseded packages. The archive format (section 10) deletes superseded bags from project hosting. Repositories that version files and keep records (Zenodo, Nakala) will not delete a superseded version on request without their own process. The design must therefore not assume that an institution deletes the superseded bag. It must ask for it in the agreement and record the answer. [inference] from sections 3.6 and 3.11.

DOI. Archive format section 12 asks whether editions receive a DOI. DOIs survive withdrawal in the repositories reviewed (sections 3.6 and 3.11), so a DOI should only be assigned to a package without personal data, or after the legal review. [inference]

## 6. Open questions

1. Will the Archives nationales accept a born-digital edition package with a privacy-revision clause? The answer decides whether the rest of the plan needs a fallback. [inference]
2. Which departmental archive covers the owner's place of residence, and does it accept born-digital packages? The owner should ask. [inference]
3. Does the BnF's agreed-modality clause (article L132-2-1) apply to an edition package, and how does the BnF apply removals to harvested pages? [fetched] for the clause, [inference] for the application.
4. Does a public archive's acceptance of a private deposit create a public-interest basis for processing under GDPR article 89? The reviewer's note says a basis in Union or Member State law is needed. A contract with a public archive may or may not be such a basis, and this needs legal review. [inference]
5. What is the exact text of the CNIL guide on definitive archiving, and does it contain a model convention for private operators? The two CNIL PDFs read here do not contain one. [fetched]
6. What do the Huma-Num and Nakala rules say, verified from their own pages? The documentation pages could not be opened. [search]
7. What is the current Internet Archive procedure for removing one's own items, and for excluding a site from the Wayback Machine? The help article was not read. [search]
8. Is the Archivio Diaristico Nazionale's licence agreement compatible with CC BY 4.0, and what does it say about withdrawal? The licence is a linked PDF that was not read. [fetched] for the existence of the licence, [inference] for the rest.
9. Which digital-rights or digital-preservation associations would accept the Guestbook, and on what terms? [inference]
10. What is the cost of the Nakala and Software Heritage deposit routes? The Nakala cost was not found, and the Software Heritage FAQ does not state one. [fetched] for the Software Heritage FAQ silence.

## 7. Sources

Repository documents read: `AGENTS.md`, `docs/constitution/continuity.md`, `docs/constitution/archival-model.md`, `docs/specs/archive-format.md`, `docs/specs/deletion-lifecycle.md`, `docs/research/custodial-indie-projects.md` (lesson 5, reviewer's note, sections 3.2 and 3.16), `docs/research/domain-and-persistence.md` (section 3).

BnF:

- <https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006845522> [fetched]
- <https://www.bnf.fr/fr/centre-d-aide/depot-legal> [fetched]
- <https://www.bnf.fr/en/help-center/web-legal-deposit-instructions> [fetched]
- <https://www.bnf.fr/en/your-website-harvested-bnfs-robot> [fetched]
- <https://collecteweb.bnf.fr/legal> [fetched]
- <https://www.bnf.fr/fr/politique-de-confidentialite> [search]

Archives:

- <https://www.archives-nationales.culture.gouv.fr/particuliers-et-associations> [fetched]
- <https://fr.wikipedia.org/wiki/Archives_nationales_de_France> [search]
- <https://www.cnil.fr/sites/cnil/files/2024-01/schema_archivage_des_documents_presentant_un_interet_historique.pdf> [fetched, read by text extraction]
- <https://www.cnil.fr/sites/default/files/atoms/files/guide_durees_de_conservation.pdf> [fetched, read by text extraction]
- <https://labo.societenumerique.gouv.fr/fr/articles/comment-les-mus%C3%A9es-services-des-archives-et-la-bnf-archivent-et-documentent-la-crise-sanitaire/> [fetched]
- <https://www.banquedesterritoires.fr/covid-19-les-services-darchives-multiplient-les-collectes-de-memoires-sur-le-confinement> [search]
- <https://www.cap-com.org/actualit%C3%A9s/les-memoires-du-confinement-les-collectivites-collectent-deja-temoignages-et-photos> [search]
- <https://www.archives49.fr/le-temps-suspendu/sevader-en-famille/votre-confinement/> [search]
- <https://www.archivespasdecalais.fr/Participer/Collectes-d-archives/Paroles-de-confine-e-s> [search]
- <https://www.valdemarne.fr/espace-presse/les-communiques-de-presse/les-archives-departementales-publient-les-temoignages-recueillis-pendant-le-confinement> [search]
- <https://www.archimag.com/archives-patrimoine/2020/03/23/memoires-confinement-projets-archivent-quotidien-coronavirus-covid-19> [search]
- <https://vosgesmag.fr/articles/articleid/15645/confinement-envoyez-vos-t%C3%A9moignages-aux-archives-d%C3%A9partementales> [search]
- <https://www.archivesnationales.culture.gouv.fr/camt/fr/egf/deposer.html> [search]
- <https://fondationmemoiredeportation.com/archives-orales/> [search]

Oral archives and testimony:

- <https://www.collexpersee.eu/wp-content/uploads/2021/06/Guide-sur-les-archives-orales.pdf> [fetched, read by text extraction]
- <https://www.premiopieve.it/invia-un-diario/> [fetched]
- <http://archiviodiari.org/index.php/modalita-di-donazione.html> [search]
- <https://entrepot.recherche.data.gouv.fr/dataverse/univ-paris1> [search]

Huma-Num, Nakala and Recherche Data Gouv:

- <https://documentation.huma-num.fr/nakala/> [search]
- <https://documentation.huma-num.fr/nakala-faq/> [search]
- <https://documentation.huma-num.fr/nakala-qualite/> [search]
- <https://cat.opidor.fr/index.php/Nakala> [search]
- <https://www.univ-smb.fr/bu/en/science-ouverte/nakala/> [search]
- <https://recherche.data.gouv.fr/fr/page/conditions-generales-d-utilisation-de-la-plateforme-de-recherche-data-gouv> [fetched]
- <https://sorbonne-alliance.pantheonsorbonne.fr/sites/default/files/2026-04/2026_up1_fiche-pratique-rgpd-donnees-personnelles_ouvrir-des-donnees-de-recherche-contenant-des-donnees-personnelles.pdf> [search]

Software Heritage:

- <https://www.softwareheritage.org/software-heritage-faq/> [fetched]
- <https://www.softwareheritage.org/legal/content-policy/> [fetched]
- <https://www.softwareheritage.org/2019/01/10/save_code_now/> [search]

Internet Archive:

- <https://help.archive.org/help/rights/> [fetched]
- <https://help.archive.org/help/how-do-i-request-removal-of-intimate-images-of-me-published-without-my-consent/> [search]
- <https://archive.org/post/345681/removing-site-from-wayback-machine> [search]

Zenodo:

- <https://about.zenodo.org/policies/> [fetched]
- <https://support.zenodo.org/help/en-gb/1-upload-deposit/215-can-i-delete-my-record-after-publishing> [fetched]
- <https://www.openaire.eu/zenodo-introduces-a-new-way-to-manage-and-correct-published-records> [search]
- <https://help.zenodo.org/docs/deposit/manage-records> [search]
- <https://www.openaire.eu/zenodo/> [search]

Associations:

- <https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000006294257/2014-08-02> [fetched]
- <https://associations.gouv.fr/lassociation-declaree-regie-par-la-loi-du-1er-juillet-1901> [search]
- <https://framablog.org/2021/10/12/frama-cest-aussi-des-humain%C2%B7es-qui-sassocient/> [search]
