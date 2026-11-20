import re

import pytest
from django.core import mail

from accounts.models import Account, MagicLink
from testimonies.models import ConsentRecord, Testimony

DRAFT_URL = "/account/testimony/"
SUBMIT_URL = "/account/testimony/submit/"
PARENTAL_URL = "/account/testimony/parental/"


def draft(**overrides):
    values = {
        "language": "en",
        "body": "I wrote this myself.",
        "identity_mode": "anonymous",
        "display_name": "",
        "authorship_category": "none",
        "action": "save",
    }
    values.update(overrides)
    return values


def submission(**overrides):
    values = {"declared_age_band": "16-or-over", "publication_statement": "on"}
    values.update(overrides)
    return values


def save(client, **overrides):
    return client.post(DRAFT_URL, draft(**overrides))


@pytest.mark.django_db
def test_contribution_pages_require_sign_in(client):
    assert client.get(DRAFT_URL).status_code == 302
    assert client.get(SUBMIT_URL).status_code == 302


@pytest.mark.django_db
def test_a_draft_is_saved_and_shown_again(client, contributor):
    response = save(client, body="A *first* draft.")
    assert response.status_code == 302
    testimony = Testimony.objects.get(account=contributor)
    assert testimony.state == "draft"
    assert testimony.revisions.get(sequence=1).body == "A *first* draft."

    page = client.get(DRAFT_URL)
    assert b"A *first* draft." in page.content


@pytest.mark.django_db
def test_saving_again_updates_the_single_draft(client, contributor):
    save(client, body="One.")
    save(client, body="Two.")
    assert Testimony.objects.filter(account=contributor).count() == 1
    assert Testimony.objects.get(account=contributor).revisions.get().body == "Two."


@pytest.mark.django_db
def test_preview_renders_markdown_without_publishing(client, contributor):
    response = client.post(DRAFT_URL, draft(body="Some *emphasis*.", action="preview"))
    assert response.status_code == 200
    assert "<em>emphasis</em>" in response.content.decode()
    assert Testimony.objects.get(account=contributor).state == "draft"


@pytest.mark.django_db
def test_language_is_canonicalized(client, contributor):
    save(client, language="FR-fr")
    assert Testimony.objects.get(account=contributor).language == "fr-FR"


@pytest.mark.django_db
def test_control_characters_are_refused(client, contributor):
    response = save(client, body="Tab\there.")
    assert response.status_code == 200
    assert "Remove control characters" in response.content.decode()
    assert not Testimony.objects.filter(account=contributor).exists()


@pytest.mark.django_db
def test_anonymous_testimonies_have_no_display_name(client, contributor):
    response = save(client, identity_mode="anonymous", display_name="Ada")
    assert response.status_code == 200
    assert "Anonymous testimonies have no display name" in response.content.decode()
    assert not Testimony.objects.filter(account=contributor).exists()


@pytest.mark.django_db
def test_named_testimonies_need_a_display_name(client, contributor):
    response = save(client, identity_mode="named", display_name="")
    assert response.status_code == 200
    assert "Give a display name" in response.content.decode()


@pytest.mark.django_db
def test_ai_details_need_an_ai_category(client, contributor):
    response = save(client, authorship_category="none", provider="Example AI")
    assert response.status_code == 200
    assert "Leave this empty" in response.content.decode()


@pytest.mark.django_db
def test_lists_and_codes_are_stored_as_values(client, contributor):
    save(
        client,
        languages="fr, en,  fr",
        tools_used="Notebook\n\nSpreadsheet",
        relationship_to_ai=["user", "researcher"],
        country="fr",
        ai_use_frequency="weekly",
    )
    revision = Testimony.objects.get(account=contributor).revisions.get()
    assert revision.languages == ["fr", "en"]
    assert revision.tools_used == ["Notebook", "Spreadsheet"]
    assert sorted(revision.relationship_to_ai) == ["researcher", "user"]
    assert revision.country == "FR"
    assert revision.ai_use_frequency == "weekly"


@pytest.mark.django_db
def test_a_prediction_year_needs_a_prediction(client, contributor):
    response = save(client, prediction_horizon=2032)
    assert response.status_code == 200
    assert "Write the prediction" in response.content.decode()


@pytest.mark.django_db
def test_submitting_needs_a_body_and_a_language(client, contributor):
    save(client, body="", language="")
    response = client.post(SUBMIT_URL, submission())
    assert response.status_code == 200
    assert "Write your testimony" in response.content.decode()


@pytest.mark.django_db
def test_publication_statement_is_required(client, contributor):
    save(client)
    response = client.post(SUBMIT_URL, submission(publication_statement=""))
    assert response.status_code == 200
    assert Testimony.objects.get(account=contributor).state == "draft"


@pytest.mark.django_db
def test_an_adult_submission_records_consent_and_waits_for_review(client, contributor):
    save(client, body="Written by hand.")
    response = client.post(SUBMIT_URL, submission())
    assert response.status_code == 302
    assert response["Location"] == DRAFT_URL

    testimony = Testimony.objects.get(account=contributor)
    assert testimony.state == "submitted"
    assert testimony.received_at is not None
    assert testimony.edition_period == testimony.received_at.year
    assert testimony.revisions.get().submitted_at == testimony.received_at

    consent = ConsentRecord.objects.get(testimony=testimony)
    assert consent.consent_path == "self"
    assert consent.declared_age_band == "16-or-over"
    assert consent.parental_consent_at is None
    assert consent.publication_consent_at == testimony.received_at

    status = client.get(DRAFT_URL)
    assert "awaiting review" in status.content.decode()


@pytest.mark.django_db
def test_submitted_testimonies_are_no_longer_edited_as_drafts(client, contributor):
    save(client)
    client.post(SUBMIT_URL, submission())
    response = save(client, body="Changed my mind.")
    assert response.status_code == 200
    assert (
        Testimony.objects.get(account=contributor).revisions.get().body
        == "I wrote this myself."
    )


@pytest.mark.django_db
def test_under_16_testimonies_must_be_anonymous_or_pseudonymous(client, contributor):
    save(client, identity_mode="named", display_name="Ada")
    response = client.post(SUBMIT_URL, submission(declared_age_band="under-16"))
    assert response.status_code == 200
    assert "not under their name" in response.content.decode()
    assert Testimony.objects.get(account=contributor).state == "draft"


@pytest.mark.django_db
def test_under_16_testimonies_cannot_show_age_region_link_or_organization(
    client, contributor
):
    save(client, age_range="18-24", region="Lyon")
    response = client.post(SUBMIT_URL, submission(declared_age_band="under-16"))
    assert "cannot give their age" in response.content.decode()


@pytest.mark.django_db
def test_under_16_submission_goes_through_the_parental_path(client, contributor):
    save(client, identity_mode="pseudonymous", display_name="Sky")
    response = client.post(SUBMIT_URL, submission(declared_age_band="under-16"))
    assert response["Location"] == PARENTAL_URL

    consent = ConsentRecord.objects.get(testimony__account=contributor)
    assert consent.consent_path == "parental"
    assert consent.parental_consent_at is None
    assert Testimony.objects.get(account=contributor).state == "submitted"


@pytest.mark.django_db
def test_a_parent_receives_one_link_and_confirms_consent(client, contributor):
    save(client, identity_mode="anonymous", body="A story about my first job.")
    client.post(SUBMIT_URL, submission(declared_age_band="under-16"))

    response = client.post(PARENTAL_URL, {"parent_email": "parent@example.org"})
    assert response.status_code == 302
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["parent@example.org"]
    token = re.search(r"/parental/([\w-]+)/", mail.outbox[0].body).group(1)

    page = client.get(f"/parental/{token}/")
    assert page.status_code == 200
    assert "A story about my first job." in page.content.decode()
    assert client.post(f"/parental/{token}/", {}).status_code == 200
    assert ConsentRecord.objects.get().parental_consent_at is None

    done = client.post(f"/parental/{token}/", {"parental_statement": "on"})
    assert done.status_code == 200
    consent = ConsentRecord.objects.get()
    assert consent.parental_consent_at is not None
    assert consent.parental_method == "email-link"
    assert not MagicLink.objects.filter(purpose="parental").exists()
    assert Testimony.objects.get(account=contributor).state == "submitted"

    assert (
        client.post(f"/parental/{token}/", {"parental_statement": "on"}).status_code
        == 404
    )


@pytest.mark.django_db
def test_parental_links_are_single_use_and_invalid_ones_are_refused(
    client, contributor
):
    save(client)
    client.post(SUBMIT_URL, submission(declared_age_band="under-16"))
    client.post(PARENTAL_URL, {"parent_email": "parent@example.org"})
    assert client.get("/parental/not-a-real-token/").status_code == 404


@pytest.mark.django_db
def test_parental_requests_are_limited_per_parent_address(client, contributor):
    save(client)
    client.post(SUBMIT_URL, submission(declared_age_band="under-16"))
    for _ in range(4):
        client.post(PARENTAL_URL, {"parent_email": "busy@example.org"})
    assert len(mail.outbox) == 3


@pytest.mark.django_db
def test_restricted_accounts_cannot_submit(client, contributor):
    Account.objects.filter(pk=contributor.pk).update(
        status="restricted", restriction_reason="spam"
    )
    save(client)
    response = client.post(SUBMIT_URL, submission(), follow=True)
    assert "cannot submit testimonies" in response.content.decode()
    assert Testimony.objects.get(account=contributor).state == "draft"
