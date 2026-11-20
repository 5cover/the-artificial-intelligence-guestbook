import json
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from publication.records import public_record
from testimonies.models import Testimony

SCHEMA_DIR = Path(settings.BASE_DIR).parent / "archive" / "schema"
SCHEMA_NAMES = ("testimony", "withdrawals")


def dumps(document):
    return json.dumps(document, ensure_ascii=False, indent=2) + "\n"


def published():
    return Testimony.objects.filter(state=Testimony.State.PUBLISHED).select_related(
        "public_revision"
    )


def index_document():
    today = timezone.localdate().isoformat()
    items = []
    for testimony in published().order_by("public_id"):
        record = public_record(testimony)
        items.append(
            {
                "public_id": record["public_id"],
                "url": record["url"],
                "language": record["language"],
                "published_on": record["published_on"],
                "edition_period": record["edition_period"],
                "identity_mode": record["identity"]["mode"],
            }
        )
    return {"format_version": 0, "generated_on": today, "testimonies": items}


def withdrawals_document():
    today = timezone.localdate().isoformat()
    withdrawn = Testimony.objects.filter(state=Testimony.State.WITHDRAWN).exclude(
        public_id=None
    )
    return {
        "format_version": 0,
        "generated_on": today,
        "withdrawals": [
            {"public_id": testimony.public_id, "editions": []}
            for testimony in withdrawn.order_by("public_id")
        ],
    }


def registry_document():
    # Editions are not published yet, so the registry lists none (archive format, section 6).
    return {"format_version": 0, "editions": []}


def schema_text(name):
    return (SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8")


def llms_text():
    base = settings.PUBLIC_BASE_URL.rstrip("/")
    return "\n".join(
        [
            "# The Artificial Intelligence Guestbook",
            "",
            "> A human time capsule of the AI era: first-person testimonies about living with AI, "
            "archived as dated editions. This file is an index of the machine-readable data.",
            "",
            "## Data",
            "",
            f"- [Testimony index]({base}/data/testimonies.json): every published testimony with its summary fields.",
            f"- [Testimony record]({base}/data/testimonies/{{public-id}}.json): one testimony, for example `{base}/data/testimonies/7q4km2xd.json`.",
            f"- [Withdrawal list]({base}/data/withdrawals.json): testimonies withdrawn from the archive, with no content.",
            f"- [Editions registry]({base}/data/time-capsules.json): every edition published.",
            f"- [Testimony record schema]({base}/data/schema/0/testimony.schema.json)",
            f"- [Withdrawal list schema]({base}/data/schema/0/withdrawals.schema.json)",
            "",
        ]
    )


def robots_text():
    return "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /account/",
            "Disallow: /sign-in/",
            "Disallow: /sign-out/",
            "Disallow: /withdraw/",
            "Disallow: /close/",
            "Disallow: /parental/",
            "Disallow: /reports/",
            "Disallow: /moderation/",
            "Disallow: /testimonies/*/report/",
            "",
        ]
    )
