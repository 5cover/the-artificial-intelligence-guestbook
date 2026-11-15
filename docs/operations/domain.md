# Domain

Status: Living record (last checked 2026-11-15)

Non-secret facts about the project's domain. Credentials, backup codes and account numbers are never recorded here: they live in the custodian's password manager and the succession envelope ([procedure](../procedures/register-and-configure-domain.md), section 7). Decision: [ADR 0008](../decisions/0008-canonical-domain.md).

| Fact | Value |
| --- | --- |
| Domain | `theaiguestbook.org` |
| Registrar | OVHcloud (RDAP: "OVH sas") |
| Registrant | Raphaël Bardini, private individual |
| DNS host | OVHcloud |
| Registered | 2026-11-15 (RDAP registration event) |
| Expires | 2027-11-15 (RDAP expiration event) |
| Term paid | 1 year, first year free with the offer; renewal EUR 12.99 per year (VAT status to confirm from the invoice) |
| Auto-renew | To confirm in the control panel |
| Transfer lock | On (RDAP status `client transfer prohibited`; also `client delete prohibited`) |
| DNSSEC | Not yet delegated (RDAP `delegationSigned: false` on 2026-11-15); enable "DNS sécurisé" and recheck |
| Registry lock | Not asked yet |
| Free hosting and mailbox | To confirm (procedure section 6.1, #45) |
| Registrar notices go to | The owner's personal mailbox (outside the domain) |
| Term policy | Extend to at least 5 years at public launch (ADR 0008, #34) |

## Pending configuration

Tracked in #46: enable DNSSEC and confirm the DS record, confirm auto-renew, activate the mailbox and DKIM, add SPF and DMARC, run the checks of procedure section 6.3, and ask about registry lock.
