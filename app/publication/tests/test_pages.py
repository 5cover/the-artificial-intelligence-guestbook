import pytest
from django.utils import timezone

from accounts.models import Account
from moderation import services
from moderation.models import ModerationRecord
from testimonies.models import ConsentRecord, Testimony
from testimonies.tests.helpers import submit_testimony

MODERATOR = "custodian@example.org"
SECRET_EMAIL = "secret-address@example.org"
SECRET_NOTE = "moderator-only-note-7731"


@pytest.fixture
def published():
    account = Account.objects.create(email=SECRET_EMAIL, created_at=timezone.now())
    testimony = submit_testimony(
        account,
        body="# Heading\n\nA plain *first* paragraph.\n\n[link](https://example.org/page)",
        identity_mode="named",
        display_name="Ada Writer",
        region="Lyon",
        authorship_category="assisted-language",
        provider="Example AI",
        ai_use_frequency="weekly",
    )
    services.approve(testimony, MODERATOR)
    ModerationRecord.objects.create(
        decision="approve",
        decided_by=MODERATOR,
        decided_at=timezone.now(),
        note=SECRET_NOTE,
    )
    return Testimony.objects.get(pk=testimony.pk)


@pytest.mark.django_db
def test_a_published_testimony_is_shown_with_its_public_id(client, published):
    response = client.get(f"/testimonies/{published.public_id}")
    assert response.status_code == 200
    html = response.content.decode()
    assert "<em>first</em>" in html
    assert "Ada Writer" in html
    assert 'href="https://example.org/page" rel="ugc nofollow noopener"' in html
    assert "not verified" in html


@pytest.mark.django_db
def test_private_fields_never_reach_a_page(client, published):
    testimony_page = client.get(f"/testimonies/{published.public_id}").content.decode()
    listing = client.get("/testimonies/").content.decode()
    for page in (testimony_page, listing):
        assert SECRET_EMAIL not in page
        assert SECRET_NOTE not in page
        assert "withdrawal_code" not in page
        assert "parental" not in page.lower()


@pytest.mark.django_db
def test_an_anonymous_testimony_shows_no_name(client, published):
    revision = published.public_revision
    revision.identity_mode = "anonymous"
    revision.display_name = None
    revision.save()
    html = client.get(f"/testimonies/{published.public_id}").content.decode()
    assert "By Anonymous" in html
    assert "Ada Writer" not in html
    assert "not verified" not in html


@pytest.mark.django_db
def test_non_canonical_identifiers_redirect_permanently(client, published):
    response = client.get(f"/testimonies/{published.public_id.upper()}")
    assert response.status_code == 301
    assert response["Location"] == f"/testimonies/{published.public_id}"


@pytest.mark.django_db
def test_unknown_or_malformed_identifiers_are_not_found(client):
    assert client.get("/testimonies/zzzzzzzz").status_code == 404
    assert client.get("/testimonies/abc").status_code == 404
    assert client.get("/testimonies/uuuuuuuu").status_code == 404


@pytest.mark.django_db
def test_a_quarantined_testimony_is_not_found(client, published):
    services.quarantine_for_legal_hold(published, MODERATOR)
    assert client.get(f"/testimonies/{published.public_id}").status_code == 404


@pytest.mark.django_db
def test_a_withdrawn_testimony_is_gone_with_a_content_free_tombstone(client, published):
    Testimony.objects.filter(pk=published.pk).update(
        state="withdrawn", withdrawn_at=timezone.now(), account=None
    )
    ConsentRecord.objects.filter(testimony=published).delete()
    response = client.get(f"/testimonies/{published.public_id}")
    assert response.status_code == 410
    html = response.content.decode()
    assert published.public_id in html
    assert "first paragraph" not in html
    assert "Ada Writer" not in html


@pytest.mark.django_db
def test_listing_shows_published_testimonies_only(client, published, contributor):
    submit_testimony(contributor, body="Still waiting for review.")
    html = client.get("/testimonies/").content.decode()
    assert published.public_id in html
    assert "Still waiting" not in html
    assert 'name="robots"' not in html


@pytest.mark.django_db
def test_filter_and_search_pages_are_not_indexed(client, published):
    assert 'name="robots"' in client.get("/testimonies/?q=first").content.decode()
    assert 'name="robots"' in client.get("/testimonies/?ai_use=weekly").content.decode()


@pytest.mark.django_db
def test_filters_offer_only_values_that_exist(client, published):
    options = client.get("/testimonies/").context["options"]
    assert [value for value, *_rest in options["ai_use"]["choices"]] == ["weekly"]
    assert options["country"]["choices"] == []


@pytest.mark.django_db
def test_a_filter_narrows_the_listing(client, published, contributor):
    other = submit_testimony(contributor, body="Another one.", ai_use_frequency="daily")
    services.approve(other, MODERATOR)
    html = client.get("/testimonies/?ai_use=weekly").content.decode()
    assert published.public_id in html
    assert other.public_id not in html


@pytest.mark.django_db
def test_search_finds_words_in_the_public_text(client, published):
    assert (
        published.public_id in client.get("/testimonies/?q=paragraph").content.decode()
    )
    assert (
        published.public_id
        not in client.get("/testimonies/?q=elephant").content.decode()
    )


@pytest.mark.django_db
def test_placeholder_pages_exist(client):
    for path in [
        "/context/",
        "/references/",
        "/methodology/",
        "/privacy/",
        "/terms/",
        "/publishing-rules/",
    ]:
        response = client.get(path)
        assert response.status_code == 200
        assert "Draft placeholder" in response.content.decode()
