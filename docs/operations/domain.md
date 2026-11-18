# Domain

Status: Living record (last checked 2026-11-18)

Non-secret facts about the project's domain. Credentials, backup codes and account numbers are never recorded here: they live in the custodian's password manager and the succession envelope ([procedure](../procedures/register-and-configure-domain.md), section 7). Decisions: [ADR 0008](../decisions/0008-canonical-domain.md) (domain), [ADR 0012](../decisions/0012-project-mailbox.md) (mailbox).

## Registration

| Fact | Value |
| --- | --- |
| Domain | `theaiguestbook.org` |
| Registrar | OVHcloud (RDAP: "OVH sas") |
| Registrant | Raphaël Bardini, private individual. Contact data is redacted from public RDAP (no registrant entity is published). |
| Registered | 2026-11-15 (RDAP registration event) |
| Expires | 2027-11-15 (RDAP expiration event) |
| Term paid | 1 year, first year free with the offer; renewal EUR 12.99 per year (VAT status to confirm from the invoice) |
| Auto-renew | On, for the domain and the free hosting (confirmed by the owner, 2026-11-18) |
| Locks | `client transfer prohibited` and `client delete prohibited` (RDAP) |
| Registry lock | Not asked yet (optional) |
| Registrar notices go to | The owner's personal mailbox, outside the domain |
| Term policy | Extend to at least 5 years at public launch (ADR 0008, #34) |

## DNS

Hosted by OVHcloud. Checked on 2026-11-18 with `Resolve-DnsName` against 1.1.1.1 and with RDAP.

| Record | Value | Notes |
| --- | --- | --- |
| NS | `dns103.ovh.net`, `ns103.ovh.net` | |
| DNSSEC | Delegated: DS key tag 46517, algorithm 8 (RSA/SHA-256), digest type 2 (SHA-256); the zone publishes a KSK and a ZSK | 1.1.1.1 is a validating resolver and answers normally, so the chain is not broken. A dnsviz.net check is still recommended (procedure, section 6.3). |
| A (`@`, `www`) | `51.91.236.255` | OVHcloud shared hosting of the free plan |
| AAAA | None | |
| MX | `1 mx1.mail.ovh.net`, `5 mx2.mail.ovh.net`, `100 mx3.mail.ovh.net` | Set by OVHcloud at mailbox activation |
| SPF | `v=spf1 include:mx.ovh.com -all` | Hard fail outside OVHcloud's mail servers |
| DKIM | `ovhmo-selector-1._domainkey` and `ovhmo-selector-2._domainkey`, CNAMEs to OVHcloud | Both resolve to 2048-bit RSA keys (`v=DKIM1; k=rsa`) |
| DMARC | `v=DMARC1; p=none; rua=mailto:contact@theaiguestbook.org; sp=none; aspf=r` | Monitoring mode. Tighten to `quarantine`, then `reject`, after four to six weeks of clean reports (section 4). |
| Other TXT | `1\|www.theaiguestbook.org` | Added by OVHcloud with the hosting plan; presumably its hosting ownership marker (inference) |
| Mail autoconfiguration | `autodiscover` CNAME and `_autodiscover._tcp` SRV to `mailconfig.ovh.net` | Added by OVHcloud |
| CAA | None | To add with the VPS (procedure, section 8.2) |

## Web

The domain serves OVHcloud's default page ("Site en construction", marked `noindex`) from the free hosting, over HTTP and HTTPS. The certificate could not be inspected from the custodian's network, whose proxy intercepts TLS. Nothing project-authored is published yet. Publishing a project page would require mentions légales first ([ADR 0004](../decisions/0004-operator-identity.md)).

## Pending

Tracked in #46:

1. Send a message from `contact@` to a personal address and back, and check that the received headers show `dkim=pass`, `spf=pass` and `dmarc=pass` ([mailbox procedure](../procedures/project-mailbox-and-dmarc.md), section 1.3).
2. Optionally, ask OVHcloud whether a registry lock is available for `.org`, and at what price.
3. Run the domain through dnsviz.net once from a network without a TLS-intercepting proxy.
4. DMARC: review the aggregate reports, then move to `p=quarantine` no earlier than 2026-12-16, and only once the transactional email provider (#10) is configured and passing; then to `p=reject` a few weeks later ([mailbox procedure](../procedures/project-mailbox-and-dmarc.md), section 2.4).
