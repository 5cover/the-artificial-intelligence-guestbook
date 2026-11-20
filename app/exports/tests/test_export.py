import csv
import json
from datetime import UTC, datetime

import bagit
import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone
from jsonschema import Draft202012Validator

from accounts.models import Account
from exports.edition import EditionError, build
from moderation import services
from moderation.models import ModerationRecord
from publication import data
from testimonies import revisions
from testimonies.models import Testimony
from testimonies.tests.helpers import submit_testimony
from testimonies.withdrawal import execute as execute_withdrawal
from testimonies.withdrawal import start_by_account

MODERATOR = "custodian@example.org"
pytestmark = pytest.mark.django_db
PRIVATE_NAMES = [
    "internal_id",
    "notifier_contact",
    "decided_by",
    "closed_account",
    "withdrawal_code",
    "token_hash",
    "parental_consent",
    "declared_age_band",
    "publication_consent_at",
    "licence_grant_version",
    "secret-address",
    "moderator-only",
]


def _year():
    return timezone.now().year


def _built_at():
    return datetime(_year() + 1, 1, 5, tzinfo=UTC)


def _published(account, **values):
    testimony = submit_testimony(account, **values)
    services.approve(testimony, MODERATOR)
    return Testimony.objects.get(pk=testimony.pk)


@pytest.fixture
def edition(contributor, tmp_path):
    published = _published(
        contributor,
        body="# Heading\n\nFirst *testimony*.",
        identity_mode="named",
        display_name="Ada",
    )
    other = _published(
        Account.objects.create(
            email="secret-address@example.org", created_at=timezone.now()
        ),
        body="Second.",
    )
    gone = _published(
        Account.objects.create(email="gone@example.org", created_at=timezone.now()),
        body="Gone.",
    )
    withdrawn_id = gone.public_id
    request, _token = start_by_account(gone.account, gone, "testimony")
    execute_withdrawal(request)
    ModerationRecord.objects.create(
        testimony=other,
        decision="approve",
        decided_by=MODERATOR,
        decided_at=timezone.now(),
        note="moderator-only note",
    )
    edition_id = f"{_year()}.0"
    bag, testimonies, withdrawals = build(edition_id, tmp_path, built_at=_built_at())
    return {
        "bag": bag,
        "edition_id": edition_id,
        "published": published,
        "withdrawn_id": withdrawn_id,
        "testimonies": testimonies,
        "withdrawals": withdrawals,
    }


def test_the_bag_is_complete_and_valid(edition):
    bag = edition["bag"]
    assert bag.name == f"the-ai-guestbook-{edition['edition_id']}"
    for name in [
        "bagit.txt",
        "bag-info.txt",
        "manifest-sha512.txt",
        "manifest-sha256.txt",
        "tagmanifest-sha512.txt",
    ]:
        assert (bag / name).is_file()
    bagit.Bag(str(bag)).validate()
    assert edition["testimonies"] == 2
    assert edition["withdrawals"] == 1


def test_every_record_validates_and_carries_the_edition(edition):
    schema = json.loads(data.schema_text("testimony"))
    records = sorted((edition["bag"] / "data" / "testimonies").glob("*.json"))
    assert len(records) == 2
    for path in records:
        record = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(record)
        assert record["edition_id"] == edition["edition_id"]
        assert record["citation"].endswith(f"Time capsule {edition['edition_id']}.")


def test_the_withdrawal_list_names_identifiers_only(edition):
    bag = edition["bag"]
    withdrawals = json.loads(
        (bag / "data" / "withdrawals.json").read_text(encoding="utf-8")
    )
    assert withdrawals["withdrawals"] == [
        {"public_id": edition["withdrawn_id"], "editions": [edition["edition_id"]]}
    ]
    with (bag / "data" / "paths.csv").open(encoding="utf-8", newline="") as handle:
        paths = {row["public_id"]: row["path"] for row in csv.DictReader(handle)}
    assert paths[edition["withdrawn_id"]] == "withdrawn"
    assert (
        paths[edition["published"].public_id]
        == f"testimonies/{edition['published'].public_id}.json"
    )


def test_the_plain_text_and_the_whole_edition_text_are_readable(edition):
    bag = edition["bag"]
    public_id = edition["published"].public_id
    text = (bag / "data" / "testimonies" / f"{public_id}.txt").read_text(
        encoding="utf-8"
    )
    assert f"Testimony {public_id}" in text
    assert "By: Ada" in text
    assert "First *testimony*." in text
    everything = (bag / "data" / "all-testimonies.txt").read_text(encoding="utf-8")
    assert everything.count("=" * 72) == 3
    assert f"Testimony {public_id}" in everything


def test_the_static_pages_have_no_scripts_or_styles(edition):
    pages = list((edition["bag"] / "data" / "html").rglob("*.html"))
    assert len(pages) >= 3
    for page in pages:
        html = page.read_text(encoding="utf-8")
        assert "<script" not in html
        assert "stylesheet" not in html


def test_a_withdrawn_testimony_has_a_tombstone_page(edition):
    page = (
        edition["bag"]
        / "data"
        / "html"
        / "testimonies"
        / f"{edition['withdrawn_id']}.html"
    )
    assert "This testimony was withdrawn" in page.read_text(encoding="utf-8")


def test_no_private_name_appears_in_the_package(edition):
    for path in edition["bag"].rglob("*"):
        if path.is_file():
            content = path.read_text(encoding="utf-8", errors="ignore")
            for name in PRIVATE_NAMES:
                assert name not in content, f"{name} found in {path.name}"


def test_a_pending_revision_in_the_period_stops_the_build(contributor, tmp_path):
    testimony = _published(contributor, body="Approved.")
    revisions.submit_edit(
        testimony, {"body": "Waiting.", "publication_statement": "on"}
    )
    with pytest.raises(EditionError, match="pending revision"):
        build(f"{_year()}.0", tmp_path, built_at=_built_at())


def test_an_edition_is_built_after_its_cutoff_only(tmp_path):
    with pytest.raises(EditionError, match="after its cutoff"):
        build(f"{_year()}.0", tmp_path, built_at=datetime(_year(), 6, 1, tzinfo=UTC))


def test_an_invalid_edition_identifier_is_refused(tmp_path):
    with pytest.raises(EditionError, match="edition identifier"):
        build("2027.x", tmp_path, built_at=_built_at())


def test_an_existing_bag_is_never_overwritten(edition):
    with pytest.raises(EditionError, match="already exists"):
        build(edition["edition_id"], edition["bag"].parent, built_at=_built_at())


def test_the_command_writes_a_bag_for_a_past_edition(tmp_path):
    past = f"{_year() - 1}.0"
    call_command("export_edition", past, str(tmp_path))
    assert (tmp_path / f"the-ai-guestbook-{past}" / "bagit.txt").is_file()


def test_the_command_refuses_a_missing_directory(tmp_path):
    with pytest.raises(CommandError, match="is not a directory"):
        call_command("export_edition", f"{_year() - 1}.0", str(tmp_path / "missing"))


def test_provenance_records_the_build_date_and_counts(edition):
    provenance = json.loads(
        (edition["bag"] / "data" / "provenance.json").read_text(encoding="utf-8")
    )
    assert provenance["built_on"] == _built_at().date().isoformat()
    assert provenance["counts"] == {
        "testimonies": 2,
        "translations": 0,
        "withdrawals": 1,
    }


def test_the_schema_is_documented_for_an_independent_reader(edition):
    readme = (edition["bag"] / "data" / "schema" / "README.txt").read_text(
        encoding="utf-8"
    )
    assert "- public_id:" in readme
    assert "- body:" in readme
