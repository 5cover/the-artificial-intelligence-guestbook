# Procedures

Status: Living index

Repeatable, step-by-step guides for operations the custodian performs: one-time setups that may need to be redone (new domain, new server, provider change) and occasional tasks. Recurring duties and incident runbooks live in `docs/operations/`. Procedures say how to do something; operations documents say what exists and when it must be done.

Each procedure states its status and the date its external facts (prices, interfaces) were last checked, and ends with sources.

| Procedure | Purpose |
| --- | --- |
| [Register and configure the domain](register-and-configure-domain.md) | Buy, secure and configure DNS for `theaiguestbook.org`, with later phases for mail, the VPS and launch |
| [Use the project mailbox and read DMARC reports](project-mailbox-and-dmarc.md) | Read `contact@` over IMAP or webmail without vendor lock-in, rules for the custodian's computer, the round-trip test, and reading and acting on DMARC reports |
