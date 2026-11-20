from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from accounts.models import Account
from moderation.emails import send_statement
from moderation.models import ModerationRecord
from testimonies.models import Testimony
from testimonies.revisions import (
    current_revision,
    make_public,
    new_public_id,
    pending_revisions,
    release_superseded_text,
)
from testimonies.services import awaiting_parental_consent

Decision = ModerationRecord.Decision
State = Testimony.State


class ReviewError(Exception):
    pass


def _record(testimony, revision, decision, moderator, now, **details):
    return ModerationRecord.objects.create(
        testimony=testimony,
        revision=revision,
        decision=decision,
        decided_by=moderator,
        decided_at=now,
        **details,
    )


def _notify(testimony, record, rule, guidance=None):
    account = testimony.account
    if account is None:
        return
    send_statement(account.email, rule, guidance)
    record.statement_sent_at = timezone.now()
    record.save(update_fields=["statement_sent_at"])


@transaction.atomic
def approve(testimony, moderator):
    pending = list(pending_revisions(testimony))
    if not pending:
        raise ReviewError(_("Nothing is waiting for review."))
    if (
        testimony.state == State.QUARANTINED
        and testimony.quarantine_reason == Testimony.QuarantineReason.LEGAL_HOLD
    ):
        raise ReviewError(_("A legal hold must be lifted before approval."))
    if awaiting_parental_consent(testimony):
        raise ReviewError(_("The parent or guardian has not confirmed yet."))

    now = timezone.now()
    latest = pending[-1]
    for revision in pending:
        revision.review_state = revision.ReviewState.APPROVED
        revision.reviewed_at = now
        revision.save(update_fields=["review_state", "reviewed_at"])
    if latest.live_at is None:
        make_public(testimony, latest, now)
    if testimony.public_id is None:
        testimony.public_id = new_public_id()
        testimony.published_at = now
    testimony.public_revision = latest
    testimony.archived_revision = latest
    testimony.state = State.PUBLISHED
    testimony.quarantine_reason = None
    testimony.save()
    release_superseded_text(testimony)
    return _record(testimony, latest, Decision.APPROVE, moderator, now)


@transaction.atomic
def return_revisions(testimony, moderator, *, rule, guidance, quarantine=False):
    pending = list(pending_revisions(testimony))
    if not pending:
        raise ReviewError(_("Nothing is waiting for review."))
    if quarantine and testimony.state != State.PUBLISHED:
        raise ReviewError(
            _("Only a published testimony can be quarantined by a return.")
        )

    now = timezone.now()
    decision = Decision.RETURN_AND_QUARANTINE if quarantine else Decision.RETURN
    record = _record(
        testimony,
        pending[-1],
        decision,
        moderator,
        now,
        rule=rule,
        guidance=guidance,
    )
    for revision in pending:
        revision.review_state = revision.ReviewState.RETURNED
        revision.reviewed_at = now
        revision.review_record = record
        revision.save(update_fields=["review_state", "reviewed_at", "review_record"])

    if quarantine:
        testimony.state = State.QUARANTINED
        testimony.quarantine_reason = Testimony.QuarantineReason.AWAITING_EDIT
        testimony.public_revision = None
    elif testimony.state == State.PUBLISHED:
        testimony.public_revision = testimony.archived_revision
    testimony.save()
    release_superseded_text(testimony)
    _notify(testimony, record, rule, guidance)
    return record


@transaction.atomic
def quarantine_for_legal_hold(testimony, moderator, note=None):
    if testimony.state not in (State.SUBMITTED, State.PUBLISHED):
        raise ReviewError(_("Only a submitted or published testimony can be held."))
    now = timezone.now()
    was_published = testimony.state == State.PUBLISHED
    testimony.state = State.QUARANTINED
    testimony.quarantine_reason = Testimony.QuarantineReason.LEGAL_HOLD
    if was_published:
        testimony.public_revision = None
    testimony.save()
    return _record(
        testimony,
        current_revision(testimony),
        Decision.QUARANTINE,
        moderator,
        now,
        note=note,
    )


@transaction.atomic
def restrict_account(testimony, moderator, *, rule, guidance):
    account = testimony.account
    if account is None:
        raise ReviewError(_("This testimony has no account to restrict."))
    now = timezone.now()
    account.status = Account.Status.RESTRICTED
    account.restriction_reason = rule
    account.save(update_fields=["status", "restriction_reason"])
    record = _record(
        testimony,
        current_revision(testimony),
        Decision.RESTRICT_ACCOUNT,
        moderator,
        now,
        rule=rule,
        guidance=guidance or None,
    )
    _notify(testimony, record, rule, guidance)
    return record
