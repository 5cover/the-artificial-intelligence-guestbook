# Use the project mailbox and read DMARC reports

Status: Ready to run (facts checked 2026-11-18)

Applies to: `contact@theaiguestbook.org` ([ADR 0012](../decisions/0012-project-mailbox.md)), issue #46. Background: [domain record](../operations/domain.md), [deletion lifecycle](../specs/deletion-lifecycle.md), [retention schedule](../specs/retention.md).

## 1. Reading the mailbox without depending on one vendor

The mailbox is an OVHcloud MX Plan account. It speaks standard protocols, so any mail program can read it, and none of them is required.

| Way | When to use | Lock-in |
| --- | --- | --- |
| A desktop mail client over IMAP, for example Thunderbird (free, open source) | Daily use (recommended) | None: IMAP (RFC 9051) and SMTP are open standards, and the mail stays on OVHcloud's server |
| OVHcloud webmail, from <https://www.ovhcloud.com/fr/mail/> | Occasional use from another computer | None: it is a website, with no account other than the mailbox |
| Redirection to a personal address | Not recommended | Copies contributors' messages into a mailbox outside the project's records and deletion lifecycle |

The "Outlook" interface that the webmail may show is OVHcloud's Outlook Web App webmail, a website, not a Microsoft product to install or subscribe to. OVHcloud is replacing it with Zimbra webmail for MX Plan accounts [1]. The control panel shows which webmail the account uses: "Web Cloud", "MX Plan", the domain, then the "Informations générales" tab [2].

### 1.1 Client settings

From OVHcloud's documentation [2] [3]:

| Direction | Server | Port | Security | Username |
| --- | --- | --- | --- | --- |
| Receive (IMAP) | `imap.mail.ovh.net` (or `ssl0.ovh.net`) | 993 | SSL/TLS | The full address, `contact@theaiguestbook.org` |
| Send (SMTP) | `smtp.mail.ovh.net` (or `ssl0.ovh.net`) | 465 with SSL/TLS, or 587 with STARTTLS | | The same |

Use IMAP, not POP. With IMAP the server remains the single source, and deleting a message deletes it everywhere. POP downloads and scatters copies. The domain publishes `autodiscover` records, so many clients find these settings by themselves from the address alone.

### 1.2 Rules for the custodian's computer

The client keeps a local copy of the mail it syncs, and that mail contains contributors' personal data. So:

1. The computer's disk must be encrypted (BitLocker on Windows, FileVault on macOS, LUKS on Linux).
2. The mailbox password is unique, generated and kept in the password manager. MX Plan has no second factor for the mailbox itself.
3. Delete on the server, through IMAP, when the retention schedule says so (rows 25 and 26). The client then removes its local copy too.
4. No exports, archives or "save as" copies of contributors' messages outside the mailbox (deletion lifecycle, place 12).

### 1.3 Round-trip test (issue #46)

1. From the client, send a message from `contact@` to a personal address at a large provider, for example Gmail.
2. At the personal address, open the message source ("Show original" in Gmail). The `Authentication-Results` header should show `dkim=pass`, `spf=pass` and `dmarc=pass`.
3. Reply, and check that the reply arrives at `contact@`.

## 2. DMARC aggregate reports

### 2.1 What they are

Large mail receivers such as Google, Microsoft and Yahoo send a daily XML report to the address in the DMARC record (`rua=mailto:contact@theaiguestbook.org`). Each report covers the mail they received that claimed to come from `theaiguestbook.org`. It lists the sending IP addresses, message counts, and whether SPF and DKIM passed and aligned. It contains no message content. Reports arrive as compressed attachments (`.xml.gz` or `.zip`).

Volume is tied to the mail the domain sends. Until the site sends magic links, expect very few reports, and none on days without outgoing mail.

### 2.2 How to read them

| Way | Notes |
| --- | --- |
| Open the XML | Fine at today's volume. Decompress the attachment and open it in a browser or text editor. Each `<record>` shows a `source_ip`, a `count`, and `<policy_evaluated>` results for `dkim` and `spf`. |
| parsedmarc, locally (recommended when volume grows) | Open-source parser, Apache-2.0, actively maintained (version 11.3.0 released 2026-11-11) [4]. It turns a folder of report attachments into CSV or JSON, and can also read the mailbox directly over IMAP. Everything stays on the custodian's machine. |
| Hosted DMARC services | Not recommended: they add a processor, often outside the EU, for a job a local tool does. |

### 2.3 What to look for

1. Every source IP belongs to OVHcloud's mail servers today, later also the transactional email provider (#10), with `dkim=pass` and `spf=pass`.
2. Any other source sending as the domain is either spoofing or a legitimate sender that is not configured yet. Investigate before tightening the policy.
3. Record what was checked in the operations log. This is the monthly duty in [recurring duties](../operations/recurring-duties.md).

### 2.4 Tightening the policy

Move from `p=none` to `p=quarantine`, then to `p=reject`, only when both of these hold:

- the reports have been clean for four to six weeks (no earlier than 2026-12-16; domain record);
- the transactional email provider for magic links (#10) is already configured with SPF and DKIM on the domain, and reports show it passing.

Tightening before the second condition would send the site's sign-in emails to spam, or have them rejected.

## Sources

- [1] OVHcloud, Zimbra FAQ for MX Plan, <https://docs.ovhcloud.com/en/guides/web-cloud/email-and-collaborative-solutions/mx-plan/faq-zimbra>, search result summary, 2026-11-18.
- [2] OVHcloud, "Getting started with the MX Plan solution", <https://docs.ovhcloud.com/en/guides/web-cloud/email-and-collaborative-solutions/mx-plan/email-generalities>, fetched 2026-11-18 (webmail login page, IMAP, POP and SMTP settings, redirections).
- [3] OVHcloud, "MX Plan - Setting up your email account on Thunderbird for Windows", <https://docs.ovhcloud.com/en/guides/web-cloud/email-and-collaborative-solutions/mx-plan/how-to-configure-thunderbird-windows>, search result summary, 2026-11-18 (SMTP port 587 with STARTTLS).
- [4] parsedmarc on PyPI and GitHub, <https://pypi.org/project/parsedmarc/>, <https://github.com/domainaware/parsedmarc>, queried 2026-11-18.
