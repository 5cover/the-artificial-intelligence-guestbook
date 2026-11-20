import re
from datetime import timedelta

import pytest
from django.core import mail
from django.utils import timezone

from accounts.models import Account
from moderation import services
from moderation.keys import review_token
from moderation.models import ModerationRecord
from moderation.services import ReviewError
from testimonies import revisions
from testimonies.models import Revision, Testimony
from testimonies.tests.helpers import latest_body, sign_in, submit_testimony

MODERATOR = "custodian@example.org"


@pytest.fixture
def moderator(client, settings):
    settings.MODERATOR_EMAILS = {MODERATOR}
    now = timezone.now()
    account = Account.objects.create(
        email=MODERATOR, created_at=now, email_verified_at=now
    )
    sign_in(client, account)
    return account


def approve_via_view(client, testimony, action="approve", **data):
    return client.post(
        f"/moderation/review/{review_token(testimony)}/decide/",
        {"action": action, **data},
    )


@pytest.mark.django_db
def test_the_moderation_area_is_hidden_from_other_visitors(
    client, contributor, settings
):
    settings.MODERATOR_EMAILS = {MODERATOR}
    assert client.get("/moderation/").status_code == 404
    sign_in(client, contributor)
    assert client.get("/moderation/").status_code == 404


@pytest.mark.django_db
def test_the_queue_lists_testimonies_waiting_for_review(client, moderator):
    account = Account.objects.create(email="a@example.org", created_at=timezone.now())
    testimony = submit_testimony(account, body="Waiting.")
    response = client.get("/moderation/")
    assert response.status_code == 200
    assert review_token(testimony).encode() in response.content


@pytest.mark.django_db
def test_a_forged_review_token_is_not_found(client, moderator):
    assert client.get("/moderation/review/not-a-token/").status_code == 404


@pytest.mark.django_db
def test_approval_publishes_with_a_public_id_and_revision_one(moderator):
    account = Account.objects.create(email="a@example.org", created_at=timezone.now())
    testimony = submit_testimony(account, body="Published text.")

    services.approve(testimony, MODERATOR)

    testimony.refresh_from_db()
    assert testimony.state == "published"
    assert len(testimony.public_id) == 8
    assert testimony.published_at is not None
    assert testimony.public_revision == testimony.archived_revision
    assert testimony.public_revision.revision_number == 1
    assert testimony.public_revision.review_state == "approved"
    record = ModerationRecord.objects.get(testimony=testimony)
    assert record.decision == "approve"
    assert record.decided_by == MODERATOR


@pytest.mark.django_db
def test_approval_of_nothing_is_refused():
    account = Account.objects.create(email="a@example.org", created_at=timezone.now())
    testimony = submit_testimony(account)
    services.approve(testimony, MODERATOR)
    with pytest.raises(ReviewError):
        services.approve(testimony, MODERATOR)


@pytest.mark.django_db
def test_a_testimony_of_a_minor_waits_for_the_parent_before_approval():
    account = Account.objects.create(email="a@example.org", created_at=timezone.now())
    testimony = submit_testimony(
        account, identity_mode="anonymous", declared_age_band="under-16"
    )
    with pytest.raises(ReviewError):
        services.approve(testimony, MODERATOR)
    assert Testimony.objects.get(pk=testimony.pk).state == "submitted"


@pytest.mark.django_db
def test_return_keeps_the_testimony_unpublished_and_notifies_the_contributor(
    moderator, client
):
    account = Account.objects.create(
        email="writer@example.org", created_at=timezone.now()
    )
    testimony = submit_testimony(account, body="Mentions Jane Doe at a bank.")

    response = approve_via_view(
        client,
        testimony,
        action="return",
        rule="third-party-privacy",
        guidance="Replace the name with a description.",
    )
    assert response.status_code == 302

    testimony.refresh_from_db()
    assert testimony.state == "submitted"
    assert testimony.public_revision is None
    returned = Revision.objects.get(testimony=testimony)
    assert returned.review_state == "returned"
    assert returned.review_record.rule == "third-party-privacy"
    assert returned.body == "Mentions Jane Doe at a bank."
    assert mail.outbox[-1].to == ["writer@example.org"]
    assert "Replace the name" in mail.outbox[-1].body


@pytest.mark.django_db
def test_a_return_needs_a_rule_and_guidance(moderator, client):
    account = Account.objects.create(
        email="writer@example.org", created_at=timezone.now()
    )
    testimony = submit_testimony(account)
    response = approve_via_view(
        client, testimony, action="return", rule="", guidance=""
    )
    assert response.status_code == 302
    assert Revision.objects.get(testimony=testimony).review_state == "pending"
    assert ModerationRecord.objects.count() == 0


@pytest.mark.django_db
def test_an_edit_of_a_published_testimony_goes_live_then_is_reviewed(
    client, contributor, moderator
):
    testimony = submit_testimony(contributor, body="First version.")
    services.approve(testimony, MODERATOR)
    testimony.refresh_from_db()

    revisions.submit_edit(
        testimony,
        {
            "body": "Second version.",
            "summary": "Corrected",
            "publication_statement": "on",
        },
    )

    testimony.refresh_from_db()
    edit = testimony.public_revision
    assert edit.revision_number == 2
    assert edit.live_at is not None
    assert edit.review_state == "pending"
    assert testimony.archived_revision.revision_number == 1

    services.approve(testimony, MODERATOR)
    testimony.refresh_from_db()
    assert testimony.archived_revision == edit
    assert testimony.archived_revision.review_state == "approved"


@pytest.mark.django_db
def test_returning_a_live_edit_restores_the_previous_version_and_keeps_numbers(
    client, contributor, moderator
):
    testimony = submit_testimony(contributor, body="Approved text.")
    services.approve(testimony, MODERATOR)
    testimony.refresh_from_db()
    revisions.submit_edit(
        testimony, {"body": "Edited text.", "publication_statement": "on"}
    )

    approve_via_view(
        client, testimony, action="return", rule="spam", guidance="Remove the links."
    )

    testimony.refresh_from_db()
    assert testimony.state == "published"
    assert testimony.public_revision.revision_number == 1
    returned = Revision.objects.get(testimony=testimony, sequence=2)
    assert returned.review_state == "returned"
    assert returned.revision_number == 2


@pytest.mark.django_db
def test_return_and_quarantine_hides_the_testimony_until_an_edit_is_approved(
    client, contributor, moderator
):
    testimony = submit_testimony(contributor, body="Approved text.")
    services.approve(testimony, MODERATOR)
    testimony.refresh_from_db()
    revisions.submit_edit(
        testimony, {"body": "Edited text.", "publication_statement": "on"}
    )

    approve_via_view(
        client,
        testimony,
        action="return-and-quarantine",
        rule="secrets",
        guidance="Remove the password.",
    )

    testimony.refresh_from_db()
    assert testimony.state == "quarantined"
    assert testimony.quarantine_reason == "awaiting-edit"
    assert testimony.public_revision is None
    assert testimony.archived_revision.body == "Approved text."

    revisions.submit_edit(
        testimony, {"body": "Clean text.", "publication_statement": "on"}
    )
    services.approve(testimony, MODERATOR)
    testimony.refresh_from_db()
    assert testimony.state == "published"
    assert latest_body(testimony) == "Clean text."


@pytest.mark.django_db
def test_under_16_edits_stay_private_until_approved(client, moderator):
    account = Account.objects.create(
        email="young@example.org", created_at=timezone.now()
    )
    testimony = submit_testimony(account, body="First.", declared_age_band="under-16")
    from testimonies.models import ConsentRecord

    ConsentRecord.objects.filter(testimony=testimony).update(
        parental_consent_at=timezone.now(), parental_method="email-link"
    )
    services.approve(testimony, MODERATOR)
    testimony.refresh_from_db()
    first = testimony.public_revision

    revisions.submit_edit(testimony, {"body": "Second.", "publication_statement": "on"})
    testimony.refresh_from_db()
    held = Revision.objects.get(testimony=testimony, sequence=2)
    assert held.live_at is None and held.revision_number is None
    assert testimony.public_revision == first

    services.approve(testimony, MODERATOR)
    testimony.refresh_from_db()
    held.refresh_from_db()
    assert testimony.public_revision == held
    assert held.revision_number == 2


@pytest.mark.django_db
def test_superseded_text_is_removed_once_reviewed(contributor, moderator):
    testimony = submit_testimony(contributor, body="Text one.")
    services.approve(testimony, MODERATOR)
    testimony.refresh_from_db()
    first = testimony.public_revision
    revisions.submit_edit(
        testimony, {"body": "Text two.", "publication_statement": "on"}
    )
    testimony.refresh_from_db()
    services.approve(testimony, MODERATOR)

    first.refresh_from_db()
    assert first.body is None
    assert latest_body(testimony) == "Text two."


@pytest.mark.django_db
def test_legal_hold_quarantines_without_a_statement(client, contributor, moderator):
    testimony = submit_testimony(contributor)
    before = len(mail.outbox)

    approve_via_view(
        client, testimony, action="quarantine", note="Reported to the authorities."
    )

    testimony.refresh_from_db()
    assert testimony.state == "quarantined"
    assert testimony.quarantine_reason == "legal-hold"
    assert len(mail.outbox) == before
    assert (
        ModerationRecord.objects.get(testimony=testimony).note
        == "Reported to the authorities."
    )


@pytest.mark.django_db
def test_restricting_an_account_stops_its_submissions(client, contributor, moderator):
    testimony = submit_testimony(contributor)
    approve_via_view(
        client,
        testimony,
        action="restrict-account",
        rule="spam",
        guidance="Repeated spam.",
    )
    contributor.refresh_from_db()
    assert contributor.status == "restricted"
    assert contributor.restriction_reason == "spam"
    assert (
        ModerationRecord.objects.get(testimony=testimony).decision == "restrict-account"
    )


@pytest.mark.django_db
def test_the_review_page_shows_word_level_changes(client, contributor, moderator):
    testimony = submit_testimony(contributor, body="The quick brown fox.")
    services.approve(testimony, MODERATOR)
    revisions.submit_edit(
        testimony, {"body": "The quick red fox.", "publication_statement": "on"}
    )

    page = client.get(f"/moderation/review/{review_token(testimony)}/")
    html = page.content.decode()
    assert "<del>brown</del><ins>red</ins>" in html
    assert "Revision" in html


@pytest.mark.django_db
def test_revision_timestamps_are_shown_in_utc(client, contributor, moderator):
    testimony = submit_testimony(contributor)
    revision = Revision.objects.get(testimony=testimony)
    page = client.get(f"/moderation/review/{review_token(testimony)}/")
    stamp = revision.submitted_at.strftime("%Y-%m-%d %H:%M")
    assert re.search(re.escape(stamp), page.content.decode())
    assert timezone.now() - revision.submitted_at < timedelta(minutes=5)
