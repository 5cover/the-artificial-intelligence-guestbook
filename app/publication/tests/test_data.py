import json
from pathlib import Path

import pytest
from django.conf import settings
from django.utils import timezone
from jsonschema import Draft202012Validator

from accounts.models import Account
from moderation import services
from moderation.models import ModerationRecord
from testimonies.models import Testimony
from testimonies.tests.helpers import submit_testimony

MODERATOR = "custodian@example.org"
SCHEMA_DIR = Path(settings.BASE_DIR).parent / "archive" / "schema"
SECRET_EMAIL = "secret-address@example.org"
SECRET_NOTE = "moderator-only-note-5521"


def schema(name):
    return json.loads((SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8"))


def validate(document, name):
    Draft202012Validator(schema(name)).validate(document)


def published(account, **values):
    testimony = submit_testimony(account, **values)
    services.approve(testimony, MODERATOR)
    return Testimony.objects.get(pk=testimony.pk)


@pytest.fixture
def named(contributor):
    return published(
        contributor,
        body="# Title\n\nA *full* record with [a link](https://example.org).",
        identity_mode="named",
        display_name="Ada Writer",
        country="FR",
        languages=["fr", "en"],
        relationship_to_ai=["user", "researcher"],
        link="https://example.org/ada",
        authorship_category="assisted-language",
        provider="Example AI",
        ai_use_frequency="weekly",
        tools_used=["Notebook", "Spreadsheet"],
        prediction="Five years from now.",
        prediction_horizon=2032,
    )


@pytest.mark.django_db
def test_a_testimony_record_validates_against_the_schema(client, named):
    response = client.get(f"/data/testimonies/{named.public_id}.json")
    assert response.status_code == 200
    assert response["Content-Type"].startswith("application/json")
    assert response["Access-Control-Allow-Origin"] == "*"
    document = response.json()
    validate(document, "testimony")
    assert "edition_id" not in document
    assert document["identity"]["display_name"] == "Ada Writer"


@pytest.mark.django_db
def test_an_anonymous_record_validates_and_says_anonymous(client, contributor):
    testimony = published(contributor, body="Anonymous words.")
    document = client.get(f"/data/testimonies/{testimony.public_id}.json").json()
    validate(document, "testimony")
    assert document["identity"] == {"mode": "anonymous"}
    assert document["citation"].startswith("Anonymous, testimony ")


@pytest.mark.django_db
def test_a_withdrawn_testimony_answers_410_with_no_content(client, named):
    Testimony.objects.filter(pk=named.pk).update(
        state="withdrawn", withdrawn_at=timezone.now(), account=None
    )
    response = client.get(f"/data/testimonies/{named.public_id}.json")
    assert response.status_code == 410
    assert response.json() == {"public_id": named.public_id, "status": "withdrawn"}


@pytest.mark.django_db
def test_a_quarantined_testimony_answers_404(client, named):
    services.quarantine_for_legal_hold(named, MODERATOR)
    assert client.get(f"/data/testimonies/{named.public_id}.json").status_code == 404


@pytest.mark.django_db
def test_a_non_canonical_identifier_redirects(client, named):
    response = client.get(f"/data/testimonies/{named.public_id.upper()}.json")
    assert response.status_code == 301
    assert response["Location"].endswith(f"/data/testimonies/{named.public_id}.json")


@pytest.mark.django_db
def test_the_index_lists_published_testimonies_and_validates_as_json(
    client, named, contributor
):
    other = Account.objects.create(email="other@example.org", created_at=timezone.now())
    published(other, body="Second.")
    testimony_draft = submit_testimony(
        Account.objects.create(email="d@example.org", created_at=timezone.now()),
        body="Waiting.",
    )
    response = client.get("/data/testimonies.json")
    document = response.json()
    ids = [item["public_id"] for item in document["testimonies"]]
    assert named.public_id in ids
    assert testimony_draft.public_id is None
    assert document["format_version"] == 0
    assert all(
        set(item)
        == {
            "public_id",
            "url",
            "language",
            "published_on",
            "edition_period",
            "identity_mode",
        }
        for item in document["testimonies"]
    )


@pytest.mark.django_db
def test_the_withdrawal_list_validates_and_names_only_identifiers(client, named):
    Testimony.objects.filter(pk=named.pk).update(
        state="withdrawn", withdrawn_at=timezone.now(), account=None
    )
    document = client.get("/data/withdrawals.json").json()
    validate(document, "withdrawals")
    assert document["withdrawals"] == [{"public_id": named.public_id, "editions": []}]


@pytest.mark.django_db
def test_the_registry_lists_no_editions_yet(client):
    assert client.get("/data/time-capsules.json").json() == {
        "format_version": 0,
        "editions": [],
    }


@pytest.mark.django_db
def test_the_schemas_are_served_from_their_identifiers(client):
    response = client.get("/data/schema/0/testimony.schema.json")
    assert response.status_code == 200
    assert (
        json.loads(response.content)["$id"]
        == "https://theaiguestbook.org/data/schema/0/testimony.schema.json"
    )
    assert client.get("/data/schema/1/testimony.schema.json").status_code == 404


@pytest.mark.django_db
def test_the_markdown_view_is_the_source_text(client, named):
    response = client.get(f"/testimonies/{named.public_id}.md")
    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/markdown")
    assert response.content.decode().startswith("# Title\n\nA *full* record")


@pytest.mark.django_db
def test_data_responses_never_carry_private_fields(client, named):
    Account.objects.filter(pk=named.account_id).update(email=SECRET_EMAIL)
    ModerationRecord.objects.create(
        testimony=named,
        decision="approve",
        decided_by=MODERATOR,
        decided_at=timezone.now(),
        note=SECRET_NOTE,
    )
    for path in [
        f"/data/testimonies/{named.public_id}.json",
        "/data/testimonies.json",
        "/data/withdrawals.json",
        f"/testimonies/{named.public_id}.md",
    ]:
        body = client.get(path).content.decode()
        assert SECRET_EMAIL not in body
        assert SECRET_NOTE not in body
        assert "withdrawal_code" not in body
        assert "parental" not in body


@pytest.mark.django_db
def test_llms_txt_links_to_the_data_urls(client):
    response = client.get("/llms.txt")
    assert response["Content-Type"].startswith("text/plain")
    text = response.content.decode()
    assert text.startswith("# The Artificial Intelligence Guestbook")
    assert "https://theaiguestbook.org/data/testimonies.json" in text
    assert "https://theaiguestbook.org/data/schema/0/testimony.schema.json" in text


@pytest.mark.django_db
def test_robots_txt_allows_the_site_and_hides_private_paths(client):
    text = client.get("/robots.txt").content.decode()
    assert "User-agent: *" in text
    assert "Allow: /" in text
    for path in ["/account/", "/sign-in/", "/moderation/", "/reports/"]:
        assert f"Disallow: {path}" in text


@pytest.mark.django_db
def test_testimony_pages_point_to_their_data_forms(client, named):
    html = client.get(f"/testimonies/{named.public_id}").content.decode()
    assert f'href="/data/testimonies/{named.public_id}.json"' in html
    assert f'href="/testimonies/{named.public_id}.md"' in html
