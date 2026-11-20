from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from reports import emails
from reports.models import Notice
from testimonies.models import Testimony

Priority = Notice.Priority
Reason = Notice.Reason

# Reason, publishing rule and priority (reports, section 1).
REASON_RULES = {
    Reason.CSAM: ("illegal", Priority.URGENT),
    Reason.THREAT: ("threat", Priority.URGENT),
    Reason.DOXXING: ("third-party-privacy", Priority.URGENT),
    Reason.ABOUT_ME: ("third-party-privacy", Priority.HIGH),
    Reason.IMPERSONATION: ("impersonation", Priority.HIGH),
    Reason.SECRETS: ("secrets", Priority.HIGH),
    Reason.DEFAMATION: ("defamation", Priority.NORMAL),
    Reason.OTHER_ILLEGAL: ("illegal", Priority.NORMAL),
    Reason.HARASSMENT: ("harassment", Priority.NORMAL),
    Reason.SPAM: ("spam", Priority.LOW),
    Reason.OTHER: (None, Priority.LOW),
}
# Only these reasons can hide a testimony automatically (reports, section 3, item 4).
URGENT_REASONS = {Reason.CSAM, Reason.THREAT, Reason.DOXXING}
HIDINGS_PER_REPORTER = 1
HIDINGS_PER_DAY = 3
HIDING_WINDOW = timedelta(days=30)
UNFOUNDED_LIMIT = 3
PRIORITY_RANK = {
    Priority.URGENT: 0,
    Priority.HIGH: 1,
    Priority.NORMAL: 2,
    Priority.LOW: 3,
}


def priority_for(reason, contact):
    priority = REASON_RULES[reason][1]
    if (
        contact
        and Notice.objects.filter(
            notifier_contact=contact, outcome=Notice.Outcome.NO_ACTION
        ).count()
        >= UNFOUNDED_LIMIT
    ):
        return Priority.LOW
    return priority


def already_reported(public_id, contact):
    if not contact:
        return False
    return Notice.objects.filter(
        testimony_public_id=public_id,
        notifier_contact=contact,
        outcome__isnull=True,
    ).exists()


def create_notice(public_id, reason, grounds, contact, channel=Notice.Channel.FORM):
    return Notice.objects.create(
        received_at=timezone.now(),
        channel=channel,
        reason=reason,
        priority=priority_for(reason, contact),
        testimony_public_id=public_id,
        notifier_contact=contact or None,
        grounds=grounds,
    )


def _may_hide(notice, now):
    if notice.reason not in URGENT_REASONS:
        return False
    if notice.notifier_contact:
        recent = Notice.objects.filter(
            notifier_contact=notice.notifier_contact,
            auto_hidden=True,
            received_at__gte=now - HIDING_WINDOW,
        ).count()
        if recent >= HIDINGS_PER_REPORTER:
            return False
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return (
        Notice.objects.filter(auto_hidden=True, received_at__gte=today).count()
        < HIDINGS_PER_DAY
    )


@transaction.atomic
def confirm(notice):
    """Put a confirmed report into the queue, hiding the testimony when the urgent rules allow it."""
    now = timezone.now()
    notice.confirmed_at = now
    notice.save(update_fields=["confirmed_at"])
    if notice.notifier_contact:
        emails.send_acknowledgement(notice.notifier_contact)

    testimony = Testimony.objects.filter(public_id=notice.testimony_public_id).first()
    if testimony is not None and notice.priority == Priority.URGENT:
        if testimony.state in (
            Testimony.State.PUBLISHED,
            Testimony.State.SUBMITTED,
        ) and _may_hide(notice, now):
            testimony.state = Testimony.State.QUARANTINED
            testimony.quarantine_reason = Testimony.QuarantineReason.LEGAL_HOLD
            testimony.public_revision = None
            testimony.save()
            notice.auto_hidden = True
            notice.save(update_fields=["auto_hidden"])
    if notice.priority == Priority.URGENT:
        emails.alert_moderators("An urgent report is waiting for review.")
    return notice


@transaction.atomic
def close_notices(public_id, outcome):
    """Record the outcome on the open reports of a testimony and tell the reporters."""
    now = timezone.now()
    for notice in Notice.objects.filter(
        testimony_public_id=public_id, outcome__isnull=True
    ):
        notice.outcome = outcome
        notice.outcome_at = now
        notice.save(update_fields=["outcome", "outcome_at"])
        if notice.notifier_contact:
            emails.send_outcome(notice.notifier_contact, outcome)


def lift_automatic_hiding(testimony):
    """Undo an automatic hiding whose report was found unfounded (reports, section 3, item 4)."""
    if testimony.quarantine_reason != Testimony.QuarantineReason.LEGAL_HOLD:
        return False
    if not Notice.objects.filter(
        testimony_public_id=testimony.public_id, auto_hidden=True
    ).exists():
        return False
    testimony.state = (
        Testimony.State.PUBLISHED
        if testimony.archived_revision
        else Testimony.State.SUBMITTED
    )
    testimony.quarantine_reason = None
    testimony.public_revision = testimony.archived_revision
    testimony.save()
    return True


def open_notices(public_id):
    return Notice.objects.filter(
        testimony_public_id=public_id,
        confirmed_at__isnull=False,
        outcome__isnull=True,
    ).order_by("received_at")
