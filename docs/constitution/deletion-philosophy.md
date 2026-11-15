# Deletion philosophy

Status: Draft, awaiting owner ratification

An archive wants to keep things. A person has the right to take back what they shared. When the two conflict, the contributor's valid privacy rights win.

## Principles

1. **Withdrawal is a practical right.** A contributor can request removal of their entry through a simple, localized process, authenticated through their private account email. They do not need to justify it.
2. **Deletion propagates.** Removing an entry reaches every copy under the project's control: live pages, database, search index, translations, caches, moderation interfaces, generated files, hosted editions, and backups within a defined and published expiry window.
3. **Designed for deletion.** The data model knows every place a piece of personal data lives, so deletion is a procedure rather than an investigation.
4. **Tombstones carry no personal data.** The archive may keep a content-free record that an identifier once existed and was withdrawn, so that citations and editions stay consistent. A tombstone never retains the content, the public identity or metadata that could identify the contributor.
5. **Editions are revised, not frozen.** Hosted editions containing withdrawn material are superseded by a privacy revision. Future editions exclude it.
6. **Honesty about copies.** Contributors are told before submitting that editions may be downloaded and kept by others, and that the project cannot recall independent copies. The project informs mirrors through a machine-readable withdrawal list and asks them to honour it.
7. **Minimal records of the request.** The project keeps only what it needs to show that a request was received and handled, for as long as the law requires, without retaining the deleted content.
8. **Redaction is not deletion.** Moderation redaction alters the public representation of an entry while preserving the original privately. Withdrawal removes both.
9. **Deletion is tested.** The deletion procedure is verified end to end before launch and periodically afterwards, like backup restores.
