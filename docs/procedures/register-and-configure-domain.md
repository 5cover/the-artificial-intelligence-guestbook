# Register and configure the domain

Status: Ready to run (prices and availability checked 2026-11-15)

Applies to: `theaiguestbook.org` ([ADR 0008](../decisions/0008-canonical-domain.md)), issue #8. Reusable for any future domain of the project.

Background: [domain research](../research/domain-and-persistence.md), section 1; [threat model](../specs/threat-model.md), section 3.8.

The procedure has one part to do now (sections 1 to 7) and later phases to do when their dependency exists (section 8). Every permanent testimony URL depends on this domain, so the priorities are: never lapse, never be hijacked, never be used to spoof the project.

## 0. Choose the registrar

| | Infomaniak | Gandi | OVHcloud |
| --- | --- | --- | --- |
| Country | Switzerland (outside the EU, covered by an EU adequacy decision) | France | France |
| .org first year, excl. VAT | EUR 9.20 [1] | EUR 15.20 regular, EUR 7.99 promotional [2] | Not retrieved; check live [3] |
| .org renewal per year, excl. VAT | EUR 13.70 [1] | EUR 31.98 regular, EUR 28.78 promotional for 2 to 9 years [2] | Not retrieved |
| 10 years, excl. VAT, estimate | about EUR 133 | about EUR 300 | - |
| Registration period | 1 to 10 years [1] | 1 to 10 years [2] | Not verified |
| DNSSEC | On by default for domains registered since 2017 [4] | Available with its LiveDNS [2] | Offered; wording differs between pages [research 1.5] |
| Account 2FA | Authenticator app, TOTP, YubiKey (Yubico OTP), SMS [5] | Not verified; check | Not verified; check |
| Notes | A free email address is included with the domain [1, secondary]. Identity verification through its app may be required at registration [secondary]. | Ownership changed in 2023, followed by price rises and the removal of free mailboxes [research 1.6]. | Large French group. |

Recommendation: Infomaniak, for cost over a decade, DNSSEC by default and hardware-key support. Choosing it means amending ADR 0008 from "EU registrar" to "EU registrar or a registrar in a country with an EU adequacy decision". Gandi or OVHcloud keep ADR 0008 as written.

Prices change: confirm them in the checkout cart before paying, and record what you actually paid in section 7.

Whatever the choice, the registrar must not be the VPS provider (ADR 0002, ADR 0008).

## 1. Prepare

1. **Registrar login email: use a mailbox outside the domain**, for example your personal address. Renewal warnings, transfer confirmations and account recovery go to this address. A mailbox on `theaiguestbook.org` would stop working exactly when the domain has a problem. This corrects the research note (section 1.7), which suggested a mailbox on the canonical domain.
2. A password manager entry for the registrar account, with a unique, generated password.
3. A second factor: a hardware key (YubiKey) if the registrar supports it, otherwise a TOTP app. Avoid SMS when anything better exists.
4. A payment card whose expiry date is at least a year away, or note its expiry for a reminder (section 7).
5. The registrant identity: your legal name, postal address, phone and email. Registrants must give accurate data; inaccurate registrant data can lead to suspension. This data is not published in the mentions légales, and registrars normally redact it from public registration data for individuals (checked in section 6).

## 2. Check that the domain is still free

PowerShell:

```powershell
curl.exe -sL -o NUL -w "%{http_code}`n" https://rdap.org/domain/theaiguestbook.org
```

`404` means unregistered. `200` means someone holds it: stop and reconsider. On 2026-11-15 the result was 404, served by the .org registry's RDAP (`rdap.publicinterestregistry.org`), while the control `wikipedia.org` returned 200.

Registration is first come, first served. Do not search for the name at registrars you will not use, or in random "availability checker" sites, before buying.

## 3. Create the registrar account

1. Sign up with the email from step 1.1.
2. Enable two-factor authentication immediately, before buying anything.
3. Store the backup or recovery codes in the password manager **and** on paper in the succession envelope (section 7). At Infomaniak, support cannot disable 2FA for you once it is on [5], so losing both factors and codes locks the account.
4. Complete any identity verification the registrar requires.

## 4. Register

1. Search `theaiguestbook.org` in the registrar's own search and add it to the cart.
2. **Period:** 10 years if the budget allows, otherwise at least 5. A long prepaid term is the strongest protection against an accidental lapse.
3. **Registrant (holder):** you, as a private individual, with accurate data. Not a pseudonym and not a company. A later transfer to an association or institution is a change of registrant, not a problem.
4. **Auto-renew:** on.
5. **Nameservers:** keep the registrar's own DNS service. One provider for both registration and DNS is simpler for one custodian and lets the registrar manage DNSSEC automatically.
6. **Decline upsells:** website builders, hosting, SSL certificates (TLS will come free from the VPS setup), SEO packages, and extra TLDs (ADR 0008 decided against defensive domains). Paid "privacy" add-ons are only worth it if section 6 shows that your data is published.
7. Pay, then keep the invoice.

## 5. Secure the domain

1. **Registrar transfer lock:** on. It appears as `client transfer prohibited` in registration data.
2. **DNSSEC:** on. It may already be on by default (Infomaniak).
3. **Notifications:** make sure renewal, expiry and security notices go to the email from step 1.1.
4. **Registry lock:** ask the registrar's support whether a registry lock is available for `.org` and at what price. It is stronger than the registrar lock, but optional at this scale. Record the answer.

## 6. Protective DNS records while nothing is hosted

Until mail and the website exist, publish records that say "this domain sends no mail", so nobody can send convincing phishing as `@theaiguestbook.org`:

| Name | Type | Value | Meaning |
| --- | --- | --- | --- |
| `@` | MX | `0 .` | Null MX (RFC 7505): the domain accepts no mail |
| `@` | TXT | `v=spf1 -all` | No server may send mail for the domain |
| `_dmarc` | TXT | `v=DMARC1; p=reject` | Receivers should reject mail that fails authentication |

`@` means the domain itself; some interfaces want an empty name instead. If the interface refuses `.` as an MX target, skip the null MX: the SPF and DMARC records do most of the work. These records are replaced in phase 8.1.

Then verify, in PowerShell (results can take from minutes to a few hours to appear):

```powershell
Resolve-DnsName theaiguestbook.org -Type NS -Server 1.1.1.1
Resolve-DnsName theaiguestbook.org -Type TXT -Server 1.1.1.1
Resolve-DnsName _dmarc.theaiguestbook.org -Type TXT -Server 1.1.1.1
Resolve-DnsName theaiguestbook.org -Type MX -Server 1.1.1.1
Resolve-DnsName theaiguestbook.org -Type DS -Server 1.1.1.1
curl.exe -sL https://rdap.org/domain/theaiguestbook.org
```

Check that:

- the NS records point to the registrar's DNS;
- the TXT, DMARC and MX answers match the table;
- a DS record exists, meaning DNSSEC is published at the registry. Also run the domain through https://dnsviz.net, which should show no errors;
- the RDAP output shows the `client transfer prohibited` status and an `expiration` event with the expected date;
- the RDAP output does not show your name, address or phone. If it does, enable the registrar's privacy or redaction option.

## 7. Record and remind

1. **Repository, non-secret facts only.** Create `docs/operations/domain.md` with: the domain, registrar, DNS host, registration date, expiry date, period paid, price paid, lock and DNSSEC status, registry-lock answer, and which mailbox receives registrar notices. Never record passwords, recovery codes or account numbers in the repository: it is public.
2. **Password manager:** registrar credentials, 2FA recovery codes, and the invoice.
3. **Succession envelope** (sealed, with a trusted person or with your important papers): registrar name, login email, how to reach the password manager, recovery codes, and a note that this domain anchors a public archive. The full succession arrangement is #33.
4. **Calendar reminders:** 90 and 30 days before expiry (check auto-renew and the card), and one month before the payment card expires.
5. **Repository update** (agent task once you report the registration):
   - replace the `<domain>` placeholder in `docs/specs/`;
   - mark ADR 0008 as in effect, amending its registrar wording if needed;
   - close #8.

Beware of scam "renewal" invoices and "domain registration expiring" emails from companies that are not your registrar. They target newly registered domains. Renew only through the registrar's own site.

## 8. Later phases

Do each one when its dependency exists. Each one changes DNS, so re-run the checks in section 6 afterwards.

### 8.1 Project mailbox (contact, privacy and legal notices)

Needed before launch: ADR 0004 requires a project contact address. The provider is not decided yet (#45). Once it is chosen:

1. Replace the null MX with the provider's MX records.
2. Replace `v=spf1 -all` with the provider's SPF include, ending in `-all`.
3. Publish the provider's DKIM record, using a 2048-bit key.
4. Change DMARC to `v=DMARC1; p=none; rua=mailto:<reports address>`, then move to `p=quarantine` and finally `p=reject` after four to six weeks of clean reports (research 1.8).
5. Create role addresses as needed, such as `contact@`, `privacy@` and `security@`. They are not the registrar login (step 1.1).

### 8.2 VPS and website (#26)

1. Add `A` and `AAAA` records pointing to the VPS.
2. Add CAA records (RFC 8659) that allow only the certificate authorities the reverse proxy actually uses. Some proxies use more than one ACME issuer by default; check before restricting, or certificate renewal will fail.
3. Optionally, `www` as a CNAME with a permanent redirect to the bare domain, or the reverse. Choose one canonical host and never change it ([identifiers](../specs/identifiers.md)).

### 8.3 Transactional email (#10)

Add the sending provider to SPF and publish its DKIM key. Check DMARC alignment: the From domain must match the DKIM or SPF domain.

### 8.4 Public launch

Search-engine verification TXT records (SEO is an explicit goal, plan section 38) and the BnF legal-deposit suggestion (research 3.7).

## 9. Recurring checks

These go into the operations calendar (#33):

| Frequency | Check |
| --- | --- |
| Monthly | Read DMARC aggregate reports, once a mailbox exists |
| Yearly | RDAP expiry date, auto-renew on, card valid, registrar 2FA still works, DNSSEC passes on dnsviz.net |
| On any registrar email about ownership, prices or terms | Re-evaluate the registrar choice |

## 10. Troubleshooting

- **The site or mail stops resolving for some users after a DNSSEC change:** validating resolvers reject broken signatures. Disable DNSSEC at the registrar, which removes the DS record, wait for it to propagate, fix the cause, then re-enable it.
- **Locked out of the registrar account:** use the recovery codes from the succession envelope. Without them, the registrar's identity procedure applies, which is slow, so keep the codes safe.
- **Domain expired by accident:** renew at once through the registrar. ICANN's Redemption Grace Period gives 30 days after deletion, followed by 5 days of Pending Delete, and restoring costs extra (Infomaniak lists EUR 105.05 for restoration [1]).

## Sources

- [1] Infomaniak .org prices page, https://www.infomaniak.com/en/domains/prices/org, as quoted in search results on 2026-11-15 (the page itself did not render fully when fetched).
- [2] Gandi .org page, https://www.gandi.net/en/domain/tld/org, fetched 2026-11-15.
- [3] OVHcloud .org and pricing pages, https://www.ovhcloud.com/fr/domains/tld/org/ and https://www.ovhcloud.com/fr/domains/tld/, fetched 2026-11-15; the price rows were truncated.
- [4] Infomaniak FAQ 2208, https://www.infomaniak.com/en/support/faq/2208/secure-web-traffic-with-dnssec, search result summary.
- [5] Infomaniak FAQ 1940, https://www.infomaniak.com/en/support/faq/1940/enable-two-factor-authentication-2fa, search result summary.
- RDAP checks run with curl on 2026-11-15.
- RFC 7505 (null MX), RFC 7208 (SPF), RFC 6376 (DKIM), RFC 9989 (DMARC) and RFC 8659 (CAA), as cited in the domain research.
