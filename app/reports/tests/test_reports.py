import re

import pytest
from django.core import mail
from django.db import IntegrityError, transaction
from django.utils import timezone

from accounts.models import Account
from moderation import services as moderation
from moderation.models import ModerationRecord
from reports import services
from reports.models import Notice
from testimonies import revisions
from testimonies.models import Testimony
from testimonies.tests.helpers import sign_in, submit_testimony

MODERATOR = "custodian@example.org"
CONFIRM = re.compile(r"/reports/confirm/([\w-]+)/")


def published(account, **values):
    testimony = submit_testimony(account, **values)
    moderation.approve(testimony, MODERATOR)
    return Testimony.objects.get(pk=testimony.pk)


def report(client, public_id, reason="spam", email="reporter@example.org", **extra):
    values = {
        "reason": reason,
        "grounds": "Why.",
        "good_faith": "on",
        "email": email,
        **extra,
    }
    return client.post(
        f"/testimonies/{public_id}/report/", values, REMOTE_ADDR="192.0.2.1"
    )


def confirm_all(client):
    for message in mail.outbox:
        match = CONFIRM.search(message.body)
        if match:
            client.post(f"/reports/confirm/{match.group(1)}/")


@pytest.fixture
def moderator(client, settings):
    settings.MODERATOR_EMAILS = {MODERATOR}
    now = timezone.now()
    account = Account.objects.create(
        email=MODERATOR, created_at=now, email_verified_at=now
    )
    sign_in(client, account)
    return account


@pytest.mark.django_db
def test_a_report_waits_for_its_confirmation_link(client, contributor):
    testimony = published(contributor, body="Visible.")
    assert report(client, testimony.public_id).status_code == 200
    notice = Notice.objects.get()
    assert notice.confirmed_at is None
    assert notice.priority == "low"
    assert services.open_notices(testimony.public_id).count() == 0

    link = CONFIRM.search(mail.outbox[-1].body).group(1)
    assert client.get(f"/reports/confirm/{link}/").status_code == 200
    assert Notice.objects.get().confirmed_at is None

    confirm_all(client)
    assert Notice.objects.get().confirmed_at is not None
    assert any(message.subject == "Your report was received" for message in mail.outbox)


@pytest.mark.django_db
def test_only_published_testimonies_can_be_reported(client, contributor):
    submit_testimony(contributor, body="Not yet.")
    assert client.get("/testimonies/zzzzzzzz/report/").status_code == 404


@pytest.mark.django_db
def test_a_report_is_reachable_from_the_testimony_page(client, contributor):
    testimony = published(contributor, body="Visible.")
    page = client.get(f"/testimonies/{testimony.public_id}").content.decode()
    assert f"/testimonies/{testimony.public_id}/report/" in page


@pytest.mark.django_db
def test_a_repeated_report_is_merged_into_the_first(client, contributor):
    testimony = published(contributor, body="Visible.")
    report(client, testimony.public_id)
    report(client, testimony.public_id)
    assert Notice.objects.count() == 1


@pytest.mark.django_db
def test_one_reporter_is_limited_to_three_reports_a_day(client, contributor):
    testimonies = [
        published(
            Account.objects.create(
                email=f"t{index}@example.org", created_at=timezone.now()
            ),
            body=f"Text {index}.",
        )
        for index in range(4)
    ]
    for testimony in testimonies:
        report(client, testimony.public_id, email="busy@example.org")
    assert Notice.objects.count() == 3


@pytest.mark.django_db
def test_without_proof_of_work_the_network_limit_is_three(client, contributor):
    testimony = published(contributor, body="Visible.")
    for index in range(4):
        report(client, testimony.public_id, email=f"n{index}@example.org")
    assert Notice.objects.count() == 3


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("reason", "priority"),
    [
        ("csam", "urgent"),
        ("doxxing", "urgent"),
        ("about-me", "high"),
        ("secrets", "high"),
        ("defamation", "normal"),
        ("harassment", "normal"),
        ("spam", "low"),
        ("other", "low"),
    ],
)
def test_each_reason_has_its_priority(reason, priority):
    assert services.REASON_RULES[reason][1] == priority


@pytest.mark.django_db
def test_a_csam_report_without_an_email_enters_the_queue_at_once(client, contributor):
    testimony = published(contributor, body="Visible.")
    report(client, testimony.public_id, reason="csam", email="")
    notice = Notice.objects.get()
    assert notice.confirmed_at is not None
    assert notice.priority == "urgent"


@pytest.mark.django_db
def test_an_urgent_confirmed_report_hides_the_testimony(client, contributor):
    testimony = published(contributor, body="Visible.")
    report(client, testimony.public_id, reason="threat", email="same@example.org")
    confirm_all(client)

    testimony.refresh_from_db()
    assert testimony.state == "quarantined"
    assert testimony.quarantine_reason == "legal-hold"
    assert Notice.objects.get().auto_hidden is True


@pytest.mark.django_db
def test_automatic_hiding_is_capped_per_day_and_alerts_the_custodian(
    contributor, settings
):
    settings.MODERATOR_EMAILS = {MODERATOR}
    testimonies = [
        published(
            Account.objects.create(
                email=f"w{index}@example.org", created_at=timezone.now()
            ),
            body=f"Text {index}.",
        )
        for index in range(4)
    ]
    for index, testimony in enumerate(testimonies):
        services.confirm(
            services.create_notice(
                testimony.public_id, "csam", "Text.", f"c{index}@example.org"
            )
        )

    assert Testimony.objects.filter(state="quarantined").count() == 3
    assert any(
        message.to == [MODERATOR] and "attention" in message.subject.lower()
        for message in mail.outbox
    )


@pytest.mark.django_db
def test_an_unfounded_reporter_is_moved_to_the_bottom(contributor):
    testimony = published(contributor, body="Visible.")
    for _index in range(3):
        old = services.create_notice(
            testimony.public_id, "spam", "No.", "crank@example.org"
        )
        old.outcome = "no-action"
        old.outcome_at = timezone.now()
        old.save()
    assert services.priority_for("threat", "crank@example.org") == "low"


@pytest.mark.django_db
def test_dismissing_reports_lifts_the_automatic_hiding(contributor):
    testimony = published(contributor, body="Visible.")
    services.confirm(
        services.create_notice(
            testimony.public_id, "threat", "Fear.", "fear@example.org"
        )
    )
    testimony.refresh_from_db()
    assert testimony.state == "quarantined"

    moderation.dismiss_reports(testimony, MODERATOR)

    testimony.refresh_from_db()
    assert testimony.state == "published"
    assert Notice.objects.get().outcome == "no-action"
    assert mail.outbox[-1].to == ["fear@example.org"]


@pytest.mark.django_db
def test_approval_closes_the_open_reports_and_tells_the_reporter(contributor):
    testimony = published(contributor, body="Visible.")
    revisions.submit_edit(testimony, {"body": "Edited.", "publication_statement": "on"})
    notice = services.create_notice(
        testimony.public_id, "spam", "Spam.", "s@example.org"
    )
    services.confirm(notice)

    moderation.approve(testimony, MODERATOR)

    notice.refresh_from_db()
    assert notice.outcome == "no-action"
    assert mail.outbox[-1].to == ["s@example.org"]


@pytest.mark.django_db
def test_removal_withdraws_the_testimony_and_keeps_the_cause(contributor):
    testimony = published(contributor, body="Removed.")
    services.confirm(
        services.create_notice(
            testimony.public_id, "defamation", "False.", "d@example.org"
        )
    )

    moderation.remove_testimony(testimony, MODERATOR, rule="defamation", guidance="")

    testimony.refresh_from_db()
    assert testimony.state == "withdrawn"
    record = ModerationRecord.objects.get(decision="remove")
    assert record.rule == "defamation"
    assert Notice.objects.get().outcome == "removed"


@pytest.mark.django_db
def test_the_queue_lists_reported_testimonies_urgent_first(
    client, contributor, moderator
):
    calm = published(contributor, body="Calm.")
    other = Account.objects.create(email="other@example.org", created_at=timezone.now())
    urgent = published(other, body="Urgent.")
    services.confirm(
        services.create_notice(calm.public_id, "spam", "Spam.", "a@example.org")
    )
    services.confirm(
        services.create_notice(urgent.public_id, "threat", "Threat.", "b@example.org")
    )

    items = client.get("/moderation/").context["items"]
    assert items[0]["testimony"].pk == urgent.pk


@pytest.mark.django_db
def test_a_notice_keeps_its_outcome_and_its_time_together():
    with pytest.raises(IntegrityError), transaction.atomic():
        Notice.objects.create(
            received_at=timezone.now(),
            reason="spam",
            priority="low",
            testimony_public_id="7q4km2xd",
            grounds="x",
            outcome="no-action",
        )
