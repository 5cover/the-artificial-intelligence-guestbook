# Register and configure the domain

Status: Ready to run with OVHcloud (registrar chosen 2026-11-15; offer details checked the same day)

Applies to: `theaiguestbook.org` ([ADR 0008](../decisions/0008-canonical-domain.md)), issue #8. Reusable for any future domain of the project.

Background: [domain research](../research/domain-and-persistence.md), section 1; [threat model](../specs/threat-model.md), section 3.8.

The procedure has one part to do now (sections 1 to 7) and later phases to do when their dependency exists (section 8). Every permanent testimony URL will depend on this domain, so the priorities are: never lapse, never be hijacked, never be used to spoof the project.

## 0. Registrar and offer

### 0.1 Registrar: OVHcloud

The owner chose OVHcloud: it is French, so ADR 0008's "EU registrar" applies as written, and it is the cheapest of the three to start with.

| | OVHcloud (chosen) | Infomaniak | Gandi |
| --- | --- | --- | --- |
| Country | France | Switzerland (EU adequacy decision) | France |
| .org first year | Free with the current offer, then EUR 12.99 per year (seen by the owner on 2026-11-15; confirm in the cart whether VAT is included) | EUR 9.20 excl. VAT [1] | EUR 15.20 regular, EUR 7.99 promotional, excl. VAT [2] |
| .org renewal per year | EUR 12.99 | EUR 13.70 excl. VAT [1] | EUR 31.98 excl. VAT [2] |
| DNSSEC | Free option ("DNS sécurisé") | On by default [4] | Available [2] |
| Account 2FA | TOTP app, U2F security key, 10 single-use backup codes [6] | TOTP, YubiKey, SMS [5] | Not verified |
| Mail | One mailbox with the free hosting plan, DKIM set up automatically [7] [8] | One free address [1] | Free mailboxes removed in 2023 [research 1.6] |

Consequence: the VPS must not be at OVHcloud (ADR 0002, ADR 0008), so that one account lockout or outage cannot take down the domain, the mail and the site together. Choose Hetzner or Scaleway in #9.

### 0.2 What to take from the OVHcloud offer

| Item | Take? | Why |
| --- | --- | --- |
| Domain `theaiguestbook.org` | Yes, for 1 year, with auto-renew | See section 4. |
| DNSSEC ("DNS sécurisé") | Yes | Free, and required by the threat model (section 3.8). |
| "Hébergement gratuit" (free 100M hosting) | Yes, mainly for its mailbox | 100 MB of space, SSL, FTP and one mailbox, free as long as the domain stays at OVHcloud, with no database [7]. The mailbox gives the project the contact address ADR 0004 requires (#45). The web space can hold an optional static placeholder page (section 6). |
| "Starter" hosting | No | It is the same kind of shared web hosting, with 1 GB and two mailboxes. It cannot run the application either, and it costs EUR 2.59 per month after the first year. |
| "CDN Basic" | No | Testimonies are text, traffic is low, and a CDN would add a processor. The threat model (section 3.4) excludes a CDN by default. |
| Paid privacy, SSL, site builder or SEO add-ons | No | Not needed (sections 4 and 6). |

None of these hosting plans can run the Guestbook application. Shared web hosting serves files and PHP, the free plan has no database, and none provides the long-running process and PostgreSQL that every candidate stack needs ([stack RFP](../proposals/stack-rfp.md)). The application goes on the VPS ([ADR 0002](../decisions/0002-single-eu-vps.md)) whichever stack is chosen.

Prices change: confirm them in the cart before paying, and record what you actually paid in section 7.

## 1. Prepare

1. **Registrar login email: use a mailbox outside the domain**, for example your personal address. Renewal warnings, transfer confirmations and account recovery go to this address. A mailbox on `theaiguestbook.org` would stop working exactly when the domain has a problem. This applies even though the project mailbox will be at OVHcloud too. This corrects the research note (section 1.7), which suggested a mailbox on the canonical domain.
2. A password manager entry for the OVHcloud account, with a unique, generated password.
3. A second factor: a U2F security key (YubiKey or similar) if you have one, otherwise a TOTP app. Avoid SMS.
4. A payment card whose expiry date is more than a year away, or note its expiry for a reminder (section 7).
5. The registrant identity: your legal name, postal address, phone and email. Registrants must give accurate data; inaccurate registrant data can lead to suspension. This data is not published in the mentions légales, and registrars normally redact it from public registration data for individuals (checked in section 6).

## 2. Check that the domain is still free

PowerShell:

```powershell
curl.exe -sL -o NUL -w "%{http_code}`n" https://rdap.org/domain/theaiguestbook.org
```

`404` means unregistered. `200` means someone holds it: stop and reconsider. On 2026-11-15 the result was 404, served by the .org registry's RDAP (`rdap.publicinterestregistry.org`), while the control `wikipedia.org` returned 200.

Registration is first come, first served. Do not search for the name on random "availability checker" sites before buying.

## 3. Create the OVHcloud account

1. Sign up with the email from step 1.1, as a private individual.
2. Enable two-factor authentication immediately, before buying anything: click your initials at the top right, then "Sécurité" [6].
3. OVHcloud then shows 10 single-use backup codes. Store them in the password manager **and** on paper in the succession envelope (section 7). Without a second factor or a code, regaining access requires proving your identity with documents [6].

## 4. Register

1. Search `theaiguestbook.org` on ovhcloud.com and add it to the cart.
2. **Period: 1 year, with auto-renew.** The permanence obligation starts when the first testimony URL is published, not before. Until launch, a lapse would cost the name but break no citation. At public launch, extend the registration to at least 5 years (section 8.4).
3. **Registrant (holder):** you, as a private individual, with accurate data. Not a pseudonym and not a company. A later transfer to an association or institution is a change of registrant, not a problem.
4. **Options in the cart:** DNSSEC yes; the free hosting ("Hébergement gratuit") yes. Decline Starter, the CDN and the other add-ons (section 0.2). The free hosting can only be attached to a domain that has no other web hosting or mail plan [7], so do not add any.
5. **DNS:** keep OVHcloud's own DNS servers, so OVHcloud manages DNSSEC and the mail records automatically.
6. Pay, then keep the invoice.

## 5. Secure the domain

In the OVHcloud control panel, under "Web Cloud", "Noms de domaine", then your domain:

1. **Transfer lock:** on. It appears as `client transfer prohibited` in registration data.
2. **DNSSEC:** on.
3. **Auto-renew:** confirm that it is on for both the domain and the free hosting.
4. **Notifications:** make sure renewal, expiry and security notices go to the email from step 1.1.
5. **Registry lock:** ask OVHcloud support whether a registry lock is available for `.org` and at what price. It is optional at this scale; record the answer.

## 6. Mail and DNS records

### 6.1 Recommended: activate the project mailbox now

1. Activate the free hosting under "Web Cloud", "Noms de domaine", your domain. Let OVHcloud configure the MX records automatically [7].
2. Create the mailbox. Suggested address: `contact@theaiguestbook.org`, which ADR 0004 requires to be published for contributors, privacy requests and legal notices. It is not the registrar login (step 1.1).
3. DKIM is proposed and enabled by default for this mailbox when the domain is at OVHcloud. In "Web Cloud", "MX Plan", "Informations générales", the DKIM indicator should turn green within 30 minutes to 24 hours. If it is red, click it and choose "Activer" [8].
4. Check that the DNS zone contains an SPF record (TXT starting `v=spf1`) for OVHcloud's mail servers. If it does not, add the one given in OVHcloud's mail documentation, ending in `-all`.
5. Add a DMARC record: name `_dmarc`, type TXT, value `v=DMARC1; p=none; rua=mailto:contact@theaiguestbook.org`. After four to six weeks of clean reports, move to `p=quarantine`, then `p=reject` (research 1.8).
6. Website, optional: OVHcloud may point the domain's `A` record at the free hosting. Either leave it serving a single static `index.html` (plain HTML, no forms, no scripts, no analytics) with a short description of the project, or remove the `A` record until the VPS exists. A placeholder gives the project an early public presence, which helps SEO, but it also makes the project public before its documents are ready. That is the owner's choice. Either way, the application goes on the VPS later (section 8.2).

### 6.2 Alternative: no mailbox yet

If you do not want a mailbox yet, publish records that say "this domain sends no mail", so nobody can send convincing phishing as `@theaiguestbook.org`:

| Name | Type | Value | Meaning |
| --- | --- | --- | --- |
| `@` | MX | `0 .` | Null MX (RFC 7505): the domain accepts no mail |
| `@` | TXT | `v=spf1 -all` | No server may send mail for the domain |
| `_dmarc` | TXT | `v=DMARC1; p=reject` | Receivers should reject mail that fails authentication |

`@` means the domain itself; some interfaces want an empty name instead. If the interface refuses `.` as an MX target, skip the null MX. These records are replaced when a mailbox is added.

### 6.3 Verify

PowerShell (results can take from minutes to a few hours to appear):

```powershell
Resolve-DnsName theaiguestbook.org -Type NS -Server 1.1.1.1
Resolve-DnsName theaiguestbook.org -Type MX -Server 1.1.1.1
Resolve-DnsName theaiguestbook.org -Type TXT -Server 1.1.1.1
Resolve-DnsName _dmarc.theaiguestbook.org -Type TXT -Server 1.1.1.1
Resolve-DnsName theaiguestbook.org -Type DS -Server 1.1.1.1
curl.exe -sL https://rdap.org/domain/theaiguestbook.org
```

Check that:

- the NS records point to OVHcloud's DNS servers;
- the MX, SPF and DMARC answers match what you configured in 6.1 or 6.2;
- a DS record exists, meaning DNSSEC is published at the registry. Also run the domain through <https://dnsviz.net>, which should show no errors;
- the RDAP output shows the `client transfer prohibited` status and an `expiration` event one year out;
- the RDAP output does not show your name, address or phone. If it does, enable OVHcloud's contact-masking option.
- Mail works both ways: send a message from the mailbox to a personal address and back. Then check that the received headers show `dkim=pass`, `spf=pass` and `dmarc=pass`.

## 7. Record and remind

1. **Repository, non-secret facts only.** Create `docs/operations/domain.md` with:
   - the domain, the registrar and the DNS host;
   - the registration date, the expiry date, the period paid and the price paid;
   - whether the free hosting and mailbox are active, and the mailbox address;
   - the lock and DNSSEC status, and the registry-lock answer;
   - which mailbox receives registrar notices.

   Never record passwords, backup codes or account numbers in the repository: it is public.
2. **Password manager:** OVHcloud credentials, 2FA backup codes, the mailbox password, and the invoice.
3. **Succession envelope** (sealed, with a trusted person or with your important papers): the registrar name, the login email, how to reach the password manager, the backup codes, and a note that this domain anchors a public archive. The full succession arrangement is #33.
4. **Calendar reminders:** 90 and 30 days before the first anniversary (check auto-renew and the card, and decide the term), and one month before the payment card expires.
5. **Repository update** (agent task once you report the registration):
   - replace the `<domain>` placeholder in `docs/specs/`;
   - mark ADR 0008 as in effect;
   - record the mailbox decision for #45;
   - close #8.

Beware of scam "renewal" invoices and "domain registration expiring" emails from companies that are not OVHcloud. They target newly registered domains. Renew only through the OVHcloud control panel.

## 8. Later phases

Do each one when its dependency exists. Each one changes DNS, so re-run the checks in 6.3 afterwards.

### 8.1 More mail addresses

The free plan has one mailbox. Role addresses such as `privacy@` and `security@` can come later, as redirections if the plan offers them (not verified) or through a paid mail plan. Until then, `contact@` serves all purposes.

### 8.2 VPS and website (#26)

1. Add `A` and `AAAA` records pointing to the VPS, replacing any placeholder `A` record.
2. Add CAA records (RFC 8659) that allow only the certificate authorities the reverse proxy actually uses. Some proxies use more than one ACME issuer by default; check before restricting, or certificate renewal will fail.
3. Optionally, `www` as a CNAME with a permanent redirect to the bare domain, or the reverse. Choose one canonical host and never change it ([identifiers](../specs/identifiers.md)).

### 8.3 Transactional email (#10)

Add the sending provider to SPF and publish its DKIM key alongside OVHcloud's. Check DMARC alignment: the From domain must match the DKIM or SPF domain.

### 8.4 Public launch

1. **Extend the registration to at least 5 years.** From now on, citations depend on the domain.
2. Add search-engine verification TXT records (SEO is an explicit goal, plan section 38).
3. Submit the BnF legal-deposit suggestion (research 3.7).

## 9. Recurring checks

These go into the operations calendar (#33):

| Frequency | Check |
| --- | --- |
| Monthly | Read DMARC aggregate reports |
| Yearly | RDAP expiry date, auto-renew on (domain and free hosting), card valid, OVHcloud 2FA still works, DNSSEC passes on dnsviz.net |
| On any registrar email about ownership, prices or terms | Re-evaluate the registrar choice |

## 10. Troubleshooting

- **The site or mail stops resolving for some users after a DNSSEC change:** validating resolvers reject broken signatures. Disable DNSSEC in the control panel, which removes the DS record, wait for it to propagate, fix the cause, then re-enable it.
- **Locked out of the OVHcloud account:** use a backup code from the succession envelope. Without one, OVHcloud's identity-document procedure applies [6], which is slow.
- **Domain expired by accident:** renew at once in the control panel. ICANN's Redemption Grace Period gives 30 days after deletion, followed by 5 days of Pending Delete, and restoring a domain costs extra.
- **Mail lands in spam:** check the DKIM indicator, the SPF record and the DMARC record (6.1), then the headers of a test message.

## Sources

- [1] Infomaniak .org prices page, <https://www.infomaniak.com/en/domains/prices/org>, as quoted in search results on 2026-11-15.
- [2] Gandi .org page, <https://www.gandi.net/en/domain/tld/org>, fetched 2026-11-15.
- [3] OVHcloud offer as seen by the owner on 2026-11-15: .org free the first year then EUR 12.99 per year; free DNSSEC option; "Hébergement gratuit" (1 site, 100 MB, 1 mailbox of 15 GB); Starter at EUR 1.59 then EUR 2.59 excl. VAT per month; CDN Basic at EUR 2.19 per month.
- [4] Infomaniak FAQ 2208, <https://www.infomaniak.com/en/support/faq/2208/secure-web-traffic-with-dnssec>, search result summary.
- [5] Infomaniak FAQ 1940, <https://www.infomaniak.com/en/support/faq/1940/enable-two-factor-authentication-2fa>, search result summary.
- [6] OVHcloud, "Sécuriser son compte OVHcloud avec la double authentification", <https://github.com/ovh/docs/blob/develop/pages/account_and_service_management/account_information/secure-ovhcloud-account-with-2fa/guide.fr-fr.md>, search result summary, 2026-11-15.
- [7] OVHcloud, free 100M hosting activation guide, <https://github.com/ovh/docs/blob/develop/pages/web_cloud/web_hosting/activate_start10m/guide.fr-fr.md>, search result summary, 2026-11-15. It covers the prerequisite of no other hosting or MX Plan, the 100 MB of space, the mailbox, the absence of a database and automatic MX setup. The official guide gives the mailbox as 5 GB; the owner's offer page shows 15 GB.
- [8] OVHcloud, DKIM guide, <https://docs.ovhcloud.com/en/guides/web-cloud/domains/dns-zone-dkim>, search result summary, 2026-11-15. DKIM is automatic for the MX Plan included with the free 100M hosting.
- RDAP checks run with curl on 2026-11-15.
- RFC 7505 (null MX), RFC 7208 (SPF), RFC 6376 (DKIM), RFC 9989 (DMARC) and RFC 8659 (CAA), as cited in the domain research.
