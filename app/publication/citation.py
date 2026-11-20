import json

from django.utils.translation import gettext as _

PUBLISHER = "The Artificial Intelligence Guestbook"


def attribution(record):
    if record["identity"]["mode"] == "anonymous":
        return _("Anonymous")
    return record["identity"]["display_name"]


def _current(record):
    # The last public revision is the one shown, and the one cited.
    return record["revisions"][-1]


def plain(record, edition_id=None):
    revision = _current(record)
    text = (
        f"{attribution(record)}, testimony {record['public_id']}, revision {revision['revision_number']}, "
        f"{PUBLISHER}, {revision['live_on']}. {record['url']}"
    )
    if edition_id:
        text += f" Time capsule {edition_id}."
    return text


def bibtex(record):
    revision = _current(record)
    author = attribution(record).replace("{", "").replace("}", "")
    return "\n".join(
        [
            f"@misc{{aiguestbook-{record['public_id']},",
            f"  author       = {{{{{author}}}}},",
            f"  title        = {{Testimony {record['public_id']}}},",
            f"  howpublished = {{{PUBLISHER}}},",
            f"  date         = {{{revision['live_on']}}},",
            f"  version      = {{{revision['revision_number']}}},",
            f"  url          = {{{record['url']}}}",
            "}",
        ]
    )


def hayagriva(record):
    # JSON strings are valid YAML double-quoted scalars, so json.dumps quotes values safely.
    revision = _current(record)
    lines = [
        f"aiguestbook-{record['public_id']}:",
        "  type: Web",
        f"  title: {json.dumps(f'Testimony {record["public_id"]}')}",
        f"  author: {json.dumps(attribution(record))}",
        f"  date: {json.dumps(revision['live_on'])}",
        f"  publisher: {json.dumps(PUBLISHER)}",
        f"  url: {json.dumps(record['url'])}",
        "  serial-number:",
        f"    serial: {json.dumps(record['public_id'])}",
    ]
    return "\n".join(lines)
