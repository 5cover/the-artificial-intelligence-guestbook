import pytest
from django.utils import timezone

from accounts.models import Account
from moderation import services
from testimonies.models import ConsentRecord, Revision, Testimony
from testimonies.tests.helpers import submit_testimony

MY_TESTIMONY = "/account/testimony/"
MODERATOR = "custodian@example.org"


def edit(client, **overrides):
    values = {
        "language": "en",
        "body": "Edited text.",
        "identity_mode": "anonymous",
        "display_name": "",
        "authorship_category": "none",
        "publication_statement": "on",
        "action": "send",
    }
    values.update(overrides)
    return client.post(MY_TESTIMONY, values)


@pytest.mark.django_db
def test_a_submitted_testimony_takes_changes_as_a_pending_revision(client, contributor):
    testimony = submit_testimony(contributor, body="Original.")

    response = edit(client)

    assert response.status_code == 302
    edited = Revision.objects.get(testimony=testimony, sequence=2)
    assert edited.body == "Edited text."
    assert edited.review_state == "pending"
    assert edited.live_at is None
    assert ConsentRecord.objects.filter(testimony=testimony).count() == 2


@pytest.mark.django_db
def test_changes_need_the_publication_statement_again(client, contributor):
    testimony = submit_testimony(contributor, body="Original.")
    response = edit(client, publication_statement="")
    assert response.status_code == 200
    assert not Revision.objects.filter(testimony=testimony, sequence=2).exists()


@pytest.mark.django_db
def test_preview_renders_the_changes_without_sending_them(client, contributor):
    testimony = submit_testimony(contributor, body="Original.")
    response = edit(client, action="preview", body="A *new* idea.")
    assert "<em>new</em>" in response.content.decode()
    assert not Revision.objects.filter(testimony=testimony, sequence=2).exists()


@pytest.mark.django_db
def test_a_published_testimony_goes_live_at_once(client, contributor, settings):
    testimony = submit_testimony(contributor, body="Original.")
    services.approve(testimony, MODERATOR)

    edit(client, body="Corrected.", summary="Corrected a word")

    testimony.refresh_from_db()
    live = testimony.public_revision
    assert live.body == "Corrected."
    assert live.revision_number == 2
    assert live.live_at is not None
    assert live.summary == "Corrected a word"
    assert testimony.archived_revision.revision_number == 1


@pytest.mark.django_db
def test_a_minors_edit_to_a_published_testimony_stays_private(client, contributor):
    account = Account.objects.get(pk=contributor.pk)
    testimony = submit_testimony(
        account, body="Original.", declared_age_band="under-16"
    )
    ConsentRecord.objects.filter(testimony=testimony).update(
        parental_consent_at=timezone.now(), parental_method="email-link"
    )
    services.approve(testimony, MODERATOR)
    before = Testimony.objects.get(pk=testimony.pk).public_revision

    edit(client, body="Private change.", identity_mode="anonymous")

    testimony.refresh_from_db()
    assert testimony.public_revision == before
    held = Revision.objects.get(testimony=testimony, body="Private change.")
    assert held.live_at is None
    assert held.revision_number is None


@pytest.mark.django_db
def test_a_quarantined_testimony_takes_an_edit_that_is_not_live(
    client, contributor, settings
):
    settings.MODERATOR_EMAILS = {MODERATOR}
    testimony = submit_testimony(contributor, body="Original.")
    services.approve(testimony, MODERATOR)
    services.quarantine_for_legal_hold(
        Testimony.objects.get(pk=testimony.pk), MODERATOR
    )
    Testimony.objects.filter(pk=testimony.pk).update(quarantine_reason="awaiting-edit")

    edit(client, body="Clean version.")

    edited = Revision.objects.get(testimony=testimony, body="Clean version.")
    assert edited.live_at is None
    assert Testimony.objects.get(pk=testimony.pk).state == "quarantined"
