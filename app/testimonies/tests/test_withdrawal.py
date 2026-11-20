import re
from datetime import timedelta

import pytest
from django.core import mail
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.utils import timezone

from accounts.models import Account
from moderation import services
from testimonies import withdrawal
from testimonies.models import ConsentRecord, Revision, Testimony, WithdrawalRequest
from testimonies.tests.helpers import sign_in, submit_testimony

MODERATOR = "custodian@example.org"
ACCOUNT_LINK = re.compile(r"https://\S+/(withdraw/link|close/link)/([\w-]+)/")


def published(account, **values):
    testimony = submit_testimony(account, **values)
    services.approve(testimony, MODERATOR)
    return Testimony.objects.get(pk=testimony.pk)


def link_from_outbox(index=-1):
    return ACCOUNT_LINK.search(mail.outbox[index].body).group(2)


@pytest.fixture
def erase_file(tmp_path, settings):
    path = tmp_path / "erase-on-restore.txt"
    settings.ERASE_ON_RESTORE_FILE = str(path)
    return path


@pytest.mark.django_db
def test_a_withdrawal_waits_for_the_confirmation_link(client, contributor):
    testimony = published(contributor, body="Withdraw me.")
    sign_in(client, contributor)

    client.post("/account/withdraw/", {"scope": "testimony"})
    token = link_from_outbox()
    assert client.get(f"/withdraw/link/{token}/").status_code == 200
    assert Testimony.objects.get(pk=testimony.pk).state == "published"


@pytest.mark.django_db
def test_withdrawing_the_testimony_removes_it_from_the_project(
    client, contributor, erase_file
):
    testimony = published(
        contributor, body="Withdraw me.", identity_mode="named", display_name="Ada"
    )
    sign_in(client, contributor)
    client.post("/account/withdraw/", {"scope": "testimony"})

    response = client.post(f"/withdraw/link/{link_from_outbox()}/")

    assert response.status_code == 200
    testimony.refresh_from_db()
    assert testimony.state == "withdrawn"
    assert testimony.account is None
    assert testimony.public_revision is None
    assert not Revision.objects.filter(testimony=testimony).exists()
    assert not ConsentRecord.objects.filter(testimony=testimony).exists()
    assert client.get(f"/testimonies/{testimony.public_id}").status_code == 410
    request = WithdrawalRequest.objects.get()
    assert request.testimony is None
    assert request.public_id == testimony.public_id
    assert request.completed_at is not None
    assert "content-deleted" in request.steps
    assert "manual:mirrors" in request.steps
    assert str(testimony.pk) in erase_file.read_text(encoding="utf-8").split()
    assert mail.outbox[-1].to == [contributor.email]


@pytest.mark.django_db
def test_withdrawing_a_name_keeps_the_testimony_anonymous_and_public(
    client, contributor
):
    testimony = published(
        contributor, body="Named once.", identity_mode="named", display_name="Ada"
    )
    sign_in(client, contributor)
    client.post("/account/withdraw/", {"scope": "field", "field_name": "display_name"})
    client.post(f"/withdraw/link/{link_from_outbox()}/")

    testimony.refresh_from_db()
    assert testimony.state == "published"
    assert testimony.public_revision.identity_mode == "anonymous"
    page = client.get(f"/testimonies/{testimony.public_id}").content.decode()
    assert "Ada" not in page
    assert "Named once." in page


@pytest.mark.django_db
def test_a_field_withdrawal_needs_the_field(client, contributor):
    published(contributor, body="Text.")
    sign_in(client, contributor)
    response = client.post("/account/withdraw/", {"scope": "field", "field_name": ""})
    assert response.status_code == 200
    assert not mail.outbox


@pytest.mark.django_db
def test_closing_the_account_keeps_the_testimony_with_a_code_shown_once(
    client, contributor, erase_file
):
    testimony = published(contributor, body="Keep me published.")
    sign_in(client, contributor)
    client.post("/account/close/", {"choice": "keep"})
    token = link_from_outbox()

    assert client.get(f"/close/link/{token}/").status_code == 200
    response = client.post(f"/close/link/{token}/")

    assert response.status_code == 200
    code = re.search(r"<code>([\w-]+)</code>", response.content.decode()).group(1)
    testimony.refresh_from_db()
    assert testimony.account is None
    assert testimony.withdrawal_code_hash is not None
    assert testimony.closed_account_email_hmac is not None
    assert testimony.state == "published"
    assert Account.objects.get(pk=contributor.pk).status == "closed"
    assert client.get(f"/testimonies/{testimony.public_id}").status_code == 200
    assert (
        code not in client.get(f"/testimonies/{testimony.public_id}").content.decode()
    )

    response = client.post(
        "/withdraw/", {"public_id": testimony.public_id, "code": code}
    )
    assert response.status_code == 200
    assert (
        "This testimony was withdrawn" in response.content.decode()
        or "withdrawal is done" in response.content.decode()
    )
    assert client.get(f"/testimonies/{testimony.public_id}").status_code == 410


@pytest.mark.django_db
def test_a_wrong_withdrawal_code_changes_nothing(client, contributor):
    testimony = published(contributor, body="Keep me.")
    sign_in(client, contributor)
    client.post("/account/close/", {"choice": "keep"})
    client.post(f"/close/link/{link_from_outbox()}/")

    response = client.post(
        "/withdraw/", {"public_id": testimony.public_id, "code": "aaaa-bbbb-cccc-dddd"}
    )

    assert response.status_code == 200
    assert "do not match" in response.content.decode()
    assert Testimony.objects.get(pk=testimony.pk).state == "published"


@pytest.mark.django_db
def test_the_former_email_sends_a_link_only_when_it_matches(client, contributor):
    testimony = published(contributor, body="Keep me.")
    sign_in(client, contributor)
    client.post("/account/close/", {"choice": "keep"})
    client.post(f"/close/link/{link_from_outbox()}/")
    sent = len(mail.outbox)

    client.post(
        "/withdraw/",
        {"public_id": testimony.public_id, "email": "stranger@example.org"},
    )
    assert len(mail.outbox) == sent

    client.post(
        "/withdraw/", {"public_id": testimony.public_id, "email": contributor.email}
    )
    assert len(mail.outbox) == sent + 1
    client.post(f"/withdraw/link/{link_from_outbox()}/")
    assert client.get(f"/testimonies/{testimony.public_id}").status_code == 410


@pytest.mark.django_db
def test_keeping_a_testimony_needs_it_to_be_published(client, contributor):
    submit_testimony(contributor, body="Not yet published.")
    sign_in(client, contributor)
    response = client.post("/account/close/", {"choice": "keep"})
    assert response.status_code == 200
    assert "Only a published testimony" in response.content.decode()
    assert not mail.outbox


@pytest.mark.django_db
def test_closing_an_account_without_a_testimony_closes_it(client, contributor):
    sign_in(client, contributor)
    client.post("/account/close/", {"choice": "withdraw"})
    response = client.post(f"/close/link/{link_from_outbox()}/")
    assert response.status_code == 200
    assert "account is closed" in response.content.decode()
    assert Account.objects.get(pk=contributor.pk).status == "closed"


@pytest.mark.django_db
def test_a_legal_hold_postpones_the_withdrawal(client, contributor):
    testimony = published(contributor, body="Held.")
    services.quarantine_for_legal_hold(testimony, MODERATOR)
    _request, token = withdrawal.start_by_account(contributor, testimony, "testimony")
    client.post(f"/withdraw/link/{token}/")

    testimony.refresh_from_db()
    assert testimony.state == "quarantined"
    assert testimony.account is not None
    assert WithdrawalRequest.objects.get().steps == ["held-by-legal-hold"]


@pytest.mark.django_db
def test_a_minor_withdrawal_is_flagged_as_such(contributor):
    testimony = submit_testimony(
        contributor, body="Young.", declared_age_band="under-16"
    )
    ConsentRecord.objects.filter(testimony=testimony).update(
        parental_consent_at=timezone.now(), parental_method="email-link"
    )
    services.approve(testimony, MODERATOR)
    request, _token = withdrawal.start_by_account(contributor, testimony, "testimony")
    assert request.minor_at_collection is True


@pytest.mark.django_db
def test_erase_on_restore_deletes_again_what_a_restore_brought_back(
    contributor, erase_file
):
    testimony = published(contributor, body="Restored by accident.")
    request, _token = withdrawal.start_by_account(contributor, testimony, "testimony")
    withdrawal.execute(request)
    Revision.objects.create(
        testimony=testimony, sequence=9, submitted_at=timezone.now(), body="Back again."
    )

    call_command("erase_on_restore")

    assert not Revision.objects.filter(testimony=testimony).exists()


@pytest.mark.django_db
def test_a_withdrawal_request_refuses_inconsistent_states(contributor):
    now = timezone.now()
    with pytest.raises(IntegrityError), transaction.atomic():
        WithdrawalRequest.objects.create(scope="field", requested_at=now)
    with pytest.raises(IntegrityError), transaction.atomic():
        WithdrawalRequest.objects.create(
            scope="testimony", requested_at=now, verified_at=now - timedelta(days=1)
        )
    testimony = Testimony.objects.create()
    with pytest.raises(IntegrityError), transaction.atomic():
        WithdrawalRequest.objects.create(
            scope="testimony",
            requested_at=now,
            verified_at=now,
            completed_at=now,
            testimony=testimony,
        )
