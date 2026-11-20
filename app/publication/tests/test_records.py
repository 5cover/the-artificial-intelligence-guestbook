import pytest
from django.utils import timezone

from moderation import services
from moderation.models import ModerationRecord
from publication import citation, identifiers
from publication.records import public_record
from testimonies.models import Revision, Testimony
from testimonies.tests.helpers import submit_testimony

MODERATOR = "custodian@example.org"
PUBLIC_KEYS = {
    "format_version",
    "public_id",
    "url",
    "language",
    "published_on",
    "edition_period",
    "licence",
    "citation",
    "body_format",
    "body",
    "revisions",
    "identity",
    "authorship",
    "structured",
}


def published(account, **values):
    testimony = submit_testimony(account, **values)
    services.approve(testimony, MODERATOR)
    return Testimony.objects.select_related("public_revision").get(pk=testimony.pk)


@pytest.mark.django_db
def test_the_record_holds_only_public_keys(contributor):
    testimony = published(
        contributor, body="Text.", region="Lyon", ai_use_frequency="daily"
    )
    record = public_record(testimony)
    assert set(record) <= PUBLIC_KEYS
    assert record["identity"]["region"] == "Lyon"
    assert record["structured"] == {"ai_use_frequency": "daily"}
    assert "email" not in str(record).lower()


@pytest.mark.django_db
def test_an_anonymous_record_has_no_display_name(contributor):
    record = public_record(published(contributor, body="Text."))
    assert record["identity"] == {"mode": "anonymous"}
    assert record["citation"].startswith("Anonymous, testimony ")


@pytest.mark.django_db
def test_dates_are_utc_days_and_the_timeline_lists_public_revisions(contributor):
    testimony = published(contributor, body="Text.")
    record = public_record(testimony)
    assert record["published_on"] == testimony.published_at.date().isoformat()
    assert record["revisions"] == [
        {"revision_number": 1, "live_on": testimony.published_at.date().isoformat()}
    ]


@pytest.mark.django_db
def test_returned_revisions_do_not_appear_in_the_timeline(contributor):
    testimony = published(contributor, body="Text.")
    record = ModerationRecord.objects.create(
        decision="return",
        rule="spam",
        guidance="Remove the links.",
        decided_by=MODERATOR,
        decided_at=timezone.now(),
    )
    Revision.objects.create(
        testimony=testimony,
        sequence=2,
        submitted_at=timezone.now(),
        review_state="returned",
        revision_number=2,
        live_at=timezone.now(),
        reviewed_at=timezone.now(),
        review_record=record,
    )
    assert [
        entry["revision_number"] for entry in public_record(testimony)["revisions"]
    ] == [1]


@pytest.mark.django_db
def test_a_named_citation_uses_the_display_name(contributor):
    testimony = published(
        contributor, body="Text.", identity_mode="named", display_name="Ada Writer"
    )
    text = citation.plain(public_record(testimony))
    assert text.startswith("Ada Writer, testimony ")
    assert text.endswith(
        f"https://theaiguestbook.org/testimonies/{testimony.public_id}"
    )


def test_bibtex_keeps_names_in_double_braces_and_drops_stray_braces():
    record = {
        "public_id": "7q4km2xd",
        "url": "https://theaiguestbook.org/testimonies/7q4km2xd",
        "identity": {"mode": "named", "display_name": "Ada {Writer}"},
        "revisions": [{"revision_number": 3, "live_on": "2027-05-02"}],
    }
    bibtex = citation.bibtex(record)
    assert "author       = {{Ada Writer}}," in bibtex
    assert "version      = {3}," in bibtex
    assert bibtex.startswith("@misc{aiguestbook-7q4km2xd,")


def test_hayagriva_quotes_values_as_json_strings():
    record = {
        "public_id": "7q4km2xd",
        "url": "https://theaiguestbook.org/testimonies/7q4km2xd",
        "identity": {"mode": "named", "display_name": 'Ada "Writer"'},
        "revisions": [{"revision_number": 1, "live_on": "2027-05-02"}],
    }
    hayagriva = citation.hayagriva(record)
    assert '  author: "Ada \\"Writer\\""' in hayagriva
    assert '    serial: "7q4km2xd"' in hayagriva


def test_identifiers_are_normalized_like_crockford_base32():
    assert identifiers.normalize("7Q4-KM 2XD") == "7q4km2xd"
    assert identifiers.normalize("7q4kml2xd") is None
    assert identifiers.normalize("io4kmo2o") == "104km020"
