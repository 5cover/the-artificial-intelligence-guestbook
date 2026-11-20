import csv
import io
import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

import bagit
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from jsonschema import Draft202012Validator

from publication import citation, data
from publication.presentation import (
    AUTHORSHIP_ROWS,
    IDENTITY_ROWS,
    STRUCTURED_ROWS,
    rows,
)
from publication.records import public_record
from testimonies.models import Testimony
from testimonies.rendering import render as render_markdown

EDITION_ID = re.compile(r"^([0-9]{4})(\.[0-9]+|-rehearsal\.[0-9]+)$")
SEPARATOR = "=" * 72
LICENCE_TEXT = """Licences of this edition

Testimonies and their public metadata are licensed CC BY 4.0 by their
contributors, with the attribution given in each record (ADR 0009).

The compilation, the context material and the project's translations are
licensed CC BY 4.0 (ADR 0016).

The project's name and logo are not licensed.

Withdrawn testimonies are listed in withdrawals.json. Mirror operators are
asked to apply that list.
"""
README_TEXT = """The Artificial Intelligence Guestbook: edition {edition_id}

This is an edition of The Artificial Intelligence Guestbook, a human time
capsule of the AI era: first-person testimonies about living with AI.

Coverage: testimonies received up to and including {cutoff} (UTC).
Testimonies in this edition: {testimonies}.
Withdrawn testimonies in the withdrawal list: {withdrawals}.

Excluded: testimonies that are not yet published, testimonies that were
returned or removed, withdrawn testimonies (only their identifiers appear, in
withdrawals.json), and all private data: account details, moderation records,
reports, requests and logs.

Licences: see LICENSE.txt.

Dates are Gregorian calendar dates in UTC. Display names are given by the
contributors and are not verified.

Verification: this edition is not yet signed. Checksums are in the manifest
files of the bag. The schemas are in schema/.

Copies downloaded by others cannot be recalled. Withdrawals are listed in
withdrawals.json so that copies can be updated.
"""
SCHEMA_README = """Schema of this edition

testimony.schema.json describes one testimony record in testimonies/. It is
JSON Schema, draft 2020-12, format version 0 (unstable until the first real
edition). Its fields are:
{fields}

withdrawals.schema.json describes withdrawals.json: the testimonies withdrawn
from this edition or an earlier one, with their identifiers only.
"""


class EditionError(Exception):
    pass


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def _csv(rows_):
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\r\n")
    writer.writerows(rows_)
    return buffer.getvalue()


def _labelled(section, labels):
    return "".join(f"{label}: {value}\n" for label, value in rows(section, labels))


def plain_text(record):
    revisions = record["revisions"]
    lines = [
        "The Artificial Intelligence Guestbook",
        f"Testimony {record['public_id']}",
        record["url"],
        "",
        f"Edition: {record['edition_id']}" if "edition_id" in record else "",
        f"Published: {record['published_on']}",
    ]
    if len(revisions) > 1:
        last = revisions[-1]
        summary = f" ({last['summary']})" if last.get("summary") else ""
        lines.append(f"Revised: {last['live_on']}{summary}")
    lines += [
        f"Language: {record['language']}",
        f"By: {citation.attribution(record)}",
        _labelled(record["identity"], IDENTITY_ROWS).rstrip("\n"),
        _labelled(record["authorship"], AUTHORSHIP_ROWS).rstrip("\n"),
        _labelled(record.get("structured", {}), STRUCTURED_ROWS).rstrip("\n"),
        "Licence: CC BY 4.0",
        "",
        "----",
        "",
        record["body"],
        "",
        "----",
        "",
    ]
    return "\n".join(line for line in lines if line is not None).replace(
        "\n\n\n", "\n\n"
    )


def _schema(name):
    return json.loads(data.schema_text(name))


def _validate(record):
    Draft202012Validator(_schema("testimony")).validate(record)


def _source_commit():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(settings.BASE_DIR).parent,
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def _schema_fields():
    schema = _schema("testimony")
    return "\n".join(
        f"- {name}: {details.get('description', details.get('type', 'see the schema'))}"
        for name, details in schema["properties"].items()
    )


def build(edition_id, output_dir, built_at=None):
    match = EDITION_ID.match(edition_id)
    if match is None:
        raise EditionError(f"{edition_id!r} is not an edition identifier.")
    year = int(match.group(1))
    cutoff = date(year, 12, 31)
    built_on = (built_at or timezone.now()).date()
    if built_on <= cutoff:
        raise EditionError(
            f"The edition is built after its cutoff, {cutoff}, not before."
        )

    waiting = Testimony.objects.filter(
        edition_period__lte=year, revisions__review_state="pending"
    ).distinct()
    if waiting.exists():
        raise EditionError(
            f"{waiting.count()} testimonies of this period have a pending revision. "
            "Review them before building the edition."
        )

    testimonies = list(
        Testimony.objects.filter(
            state=Testimony.State.PUBLISHED, edition_period__lte=year
        )
        .select_related("archived_revision")
        .order_by("public_id")
    )
    withdrawn = list(
        Testimony.objects.filter(state=Testimony.State.WITHDRAWN)
        .exclude(public_id=None)
        .order_by("public_id")
    )
    records = [
        public_record(
            testimony, revision=testimony.archived_revision, edition_id=edition_id
        )
        for testimony in testimonies
    ]
    for record in records:
        _validate(record)

    bag_name = f"the-ai-guestbook-{edition_id}"
    output = Path(output_dir)
    if (output / bag_name).exists():
        raise EditionError(f"{output / bag_name} already exists.")
    staging = output / f".staging-{bag_name}"
    if staging.exists():
        shutil.rmtree(staging)
    payload = staging
    payload.mkdir(parents=True)

    _write(
        payload / "README.txt",
        README_TEXT.format(
            edition_id=edition_id,
            cutoff=cutoff.isoformat(),
            testimonies=len(records),
            withdrawals=len(withdrawn),
        ),
    )
    _write(payload / "LICENSE.txt", LICENCE_TEXT)
    _write(
        payload / "CHANGELOG.txt",
        f"{edition_id}: first build, {built_on.isoformat()}, {len(records)} testimonies.\n",
    )
    _write(
        payload / "schema" / "README.txt", SCHEMA_README.format(fields=_schema_fields())
    )
    for name in data.SCHEMA_NAMES:
        _write(payload / "schema" / f"{name}.schema.json", data.schema_text(name))

    texts = []
    path_rows = [["public_id", "path"]]
    for record in records:
        public_id = record["public_id"]
        _write(payload / "testimonies" / f"{public_id}.json", data.dumps(record))
        text = plain_text(record)
        _write(payload / "testimonies" / f"{public_id}.txt", text)
        texts.append(text)
        path_rows.append([public_id, f"testimonies/{public_id}.json"])
    for testimony in withdrawn:
        path_rows.append([testimony.public_id, "withdrawn"])
    _write(
        payload / "all-testimonies.txt",
        "".join(f"{SEPARATOR}\n{text}" for text in texts) + f"{SEPARATOR}\n",
    )
    _write(payload / "paths.csv", _csv(path_rows))

    index_rows = [
        [
            "public_id",
            "url",
            "language",
            "published_on",
            "edition_period",
            "identity_mode",
        ]
    ]
    index_items = []
    for record in records:
        item = [
            record["public_id"],
            record["url"],
            record["language"],
            record["published_on"],
            record["edition_period"],
            record["identity"]["mode"],
        ]
        index_rows.append(item)
        index_items.append(dict(zip(index_rows[0], item, strict=True)))
    _write(
        payload / "index.json",
        data.dumps(
            {"format_version": 0, "edition_id": edition_id, "testimonies": index_items}
        ),
    )
    _write(payload / "index.csv", _csv(index_rows))

    withdrawal_items = [
        {"public_id": testimony.public_id, "editions": [edition_id]}
        for testimony in withdrawn
    ]
    _write(
        payload / "withdrawals.json",
        data.dumps(
            {
                "format_version": 0,
                "generated_on": built_on.isoformat(),
                "withdrawals": withdrawal_items,
            }
        ),
    )
    _write(
        payload / "withdrawals.csv",
        _csv(
            [["public_id", "editions"]]
            + [[item["public_id"], edition_id] for item in withdrawal_items]
        ),
    )

    html_root = payload / "html"
    _write(
        html_root / "index.html",
        render_to_string(
            "exports/index.html",
            {"records": records, "withdrawn": withdrawn, "edition_id": edition_id},
        ),
    )
    for record in records:
        body_html = render_markdown(record["body"], heading_base=1)
        _write(
            html_root / "testimonies" / f"{record['public_id']}.html",
            render_to_string(
                "exports/testimony.html",
                {
                    "record": record,
                    "body_html": body_html,
                    "attribution": citation.attribution(record),
                    "identity_rows": rows(record["identity"], IDENTITY_ROWS),
                    "authorship_rows": rows(record["authorship"], AUTHORSHIP_ROWS),
                    "structured_rows": rows(
                        record.get("structured", {}), STRUCTURED_ROWS
                    ),
                },
            ),
        )
    for testimony in withdrawn:
        _write(
            html_root / "testimonies" / f"{testimony.public_id}.html",
            render_to_string(
                "exports/tombstone.html", {"public_id": testimony.public_id}
            ),
        )

    _write(
        payload / "provenance.json",
        data.dumps(
            {
                "format_version": 0,
                "edition_id": edition_id,
                "built_on": built_on.isoformat(),
                "source_commit": _source_commit(),
                "counts": {
                    "testimonies": len(records),
                    "translations": 0,
                    "withdrawals": len(withdrawn),
                },
            }
        ),
    )

    bag_info = {
        "Source-Organization": "The Artificial Intelligence Guestbook",
        "Contact-Email": settings.DEFAULT_FROM_EMAIL,
        "External-Identifier": bag_name,
        "External-Description": "Annual edition (time capsule) of The Artificial Intelligence Guestbook, a human time capsule of the AI era.",
        "Bagging-Date": built_on.isoformat(),
        "Bag-Group-Identifier": "the-ai-guestbook",
        "Edition-Id": edition_id,
        "Edition-Cutoff": cutoff.isoformat(),
        "Edition-Supersedes": "none",
        "Format-Version": "0",
    }
    bagit.make_bag(
        str(payload), bag_info=bag_info, processes=1, checksums=["sha512", "sha256"]
    )
    final = output / bag_name
    shutil.move(str(payload), str(final))
    bagit.Bag(str(final)).validate()
    return final, len(records), len(withdrawn)
