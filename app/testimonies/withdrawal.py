import hmac
import secrets
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from accounts import hashing, magic_links
from accounts.models import Account, MagicLink
from moderation.models import ModerationRecord
from testimonies.emails import send_withdrawal_code, send_withdrawal_confirmation
from testimonies.models import ConsentRecord, Revision, Testimony, WithdrawalRequest
from testimonies.revisions import release_superseded_text
from testimonies.vocabularies import IdentityMode, WithdrawalScope

CODE_ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"
MANUAL_STEPS = (
    "manual:search-engines",
    "manual:web-archives",
    "manual:mirrors",
    "manual:vacuum-due",
)


class WithdrawalError(Exception):
    pass


def new_withdrawal_code():
    # 16 Crockford symbols in four groups. The code proves authorship, so it is shown
    # once and sent by email (deletion lifecycle, section 1).
    raw = "".join(secrets.choice(CODE_ALPHABET) for _ in range(16))
    return "-".join(raw[index : index + 4] for index in range(0, 16, 4))


def normalize_code(text):
    value = text.lower().replace("-", "").replace(" ", "")
    value = value.replace("i", "1").replace("l", "1").replace("o", "0")
    if len(value) != 16 or any(char not in CODE_ALPHABET for char in value):
        return None
    return value


def code_digest(code):
    return hashing.keyed("withdrawal-code", code)


def _erase_on_restore(internal_id):
    if not settings.ERASE_ON_RESTORE_FILE:
        return "erase-on-restore-not-configured"
    with Path(settings.ERASE_ON_RESTORE_FILE).open("a", encoding="utf-8") as listing:
        listing.write(f"{internal_id}\n")
    return "erase-on-restore-listed"


def _purge_content(testimony, keep_moderation_records=False):
    Revision.objects.filter(testimony=testimony).delete()
    ConsentRecord.objects.filter(testimony=testimony).delete()
    if not keep_moderation_records:
        ModerationRecord.objects.filter(testimony=testimony).delete()
    MagicLink.objects.filter(testimony=testimony).delete()


def erase_again(internal_id):
    # Restores bring back deleted rows: the erase-on-restore list is run again (deletion lifecycle, section 6).
    testimony = Testimony.objects.filter(
        pk=internal_id, state=Testimony.State.WITHDRAWN
    ).first()
    if testimony is not None:
        _purge_content(testimony)


def _withdraw_testimony(testimony, now, keep_moderation_records=False):
    testimony.state = Testimony.State.WITHDRAWN
    testimony.withdrawn_at = now
    testimony.public_revision = None
    testimony.archived_revision = None
    testimony.account = None
    testimony.withdrawal_code_hash = None
    testimony.closed_account_email_hmac = None
    testimony.save()
    _purge_content(testimony, keep_moderation_records)
    return [
        "tombstone-set",
        "content-deleted",
        "moderation-records-kept"
        if keep_moderation_records
        else "moderation-records-deleted",
        "account-unlinked",
    ]


def _clear_field(testimony, field_name):
    for revision in testimony.revisions.all():
        if field_name == "display_name":
            revision.identity_mode = IdentityMode.ANONYMOUS
            revision.display_name = None
        else:
            setattr(revision, field_name, None)
        revision.save()
    return [f"field-cleared:{field_name}"]


@transaction.atomic
def execute(request, now=None, keep_moderation_records=False):
    """Run the deletion steps of a verified withdrawal request (deletion lifecycle, section 3)."""
    now = now or timezone.now()
    testimony = request.testimony
    if testimony is None:
        raise WithdrawalError("The request has no testimony to act on.")
    if (
        testimony.state == Testimony.State.QUARANTINED
        and testimony.quarantine_reason == Testimony.QuarantineReason.LEGAL_HOLD
    ):
        # A legal hold postpones the deletion until it ends (data model, section 3, invariant 4).
        request.steps = ["held-by-legal-hold"]
        request.save(update_fields=["steps"])
        return request

    account = testimony.account
    public_id = testimony.public_id
    testimony_pk = testimony.pk
    steps = []
    if request.scope in (WithdrawalScope.TESTIMONY, WithdrawalScope.ACCOUNT):
        steps += _withdraw_testimony(testimony, now, keep_moderation_records)
    elif request.scope == WithdrawalScope.FIELD:
        steps += _clear_field(testimony, request.field_name)
    else:
        release_superseded_text(testimony)
        steps.append("superseded-text-released")
    if request.scope == WithdrawalScope.ACCOUNT and account is not None:
        account.status = Account.Status.CLOSED
        account.closed_at = now
        account.save(update_fields=["status", "closed_at"])
        steps.append("account-closed")

    steps.append(_erase_on_restore(testimony_pk))
    if account is not None:
        send_withdrawal_confirmation(account.email)
        steps.append("confirmation-sent")
    steps += list(MANUAL_STEPS)

    request.steps = steps
    request.public_id = public_id
    request.completed_at = now
    request.testimony = None
    request.save()
    return request


def start_by_account(account, testimony, scope, field_name=None):
    consent = testimony.consent_records.order_by("-publication_consent_at").first()
    request = WithdrawalRequest.objects.create(
        scope=scope,
        field_name=field_name,
        testimony=testimony,
        requested_at=timezone.now(),
        minor_at_collection=bool(consent and consent.declared_age_band == "under-16"),
    )
    token = magic_links.issue(
        MagicLink.Purpose.WITHDRAWAL, account.email, testimony=testimony
    )
    return request, token


def confirm_link(token):
    link = magic_links.redeem(MagicLink.Purpose.WITHDRAWAL, token)
    if link is None:
        return None
    request = (
        WithdrawalRequest.objects.filter(
            testimony=link.testimony,
            verified_at__isnull=True,
            completed_at__isnull=True,
        )
        .order_by("-requested_at")
        .first()
    )
    if request is None:
        return None
    request.verified_at = timezone.now()
    request.save(update_fields=["verified_at"])
    return execute(request)


def withdraw_with_code(public_id, code):
    testimony = Testimony.objects.filter(
        public_id=public_id, state=Testimony.State.PUBLISHED
    ).first()
    if testimony is None or testimony.withdrawal_code_hash is None:
        return None
    if not hmac.compare_digest(
        bytes(testimony.withdrawal_code_hash), code_digest(code)
    ):
        return None
    now = timezone.now()
    request = WithdrawalRequest.objects.create(
        scope=WithdrawalScope.TESTIMONY,
        testimony=testimony,
        requested_at=now,
        verified_at=now,
    )
    return execute(request, now)


def start_by_former_email(public_id, email):
    testimony = Testimony.objects.filter(
        public_id=public_id, state=Testimony.State.PUBLISHED
    ).first()
    if testimony is None or testimony.closed_account_email_hmac is None:
        return None
    if not hmac.compare_digest(
        bytes(testimony.closed_account_email_hmac), hashing.email_key(email)
    ):
        return None
    WithdrawalRequest.objects.create(
        scope=WithdrawalScope.TESTIMONY,
        testimony=testimony,
        requested_at=timezone.now(),
    )
    return magic_links.issue(MagicLink.Purpose.WITHDRAWAL, email, testimony=testimony)


def start_closure(account, keep_testimony):
    if keep_testimony:
        return magic_links.issue(MagicLink.Purpose.CLOSURE, account.email)
    testimony = account.testimonies.first()
    if testimony is None:
        raise WithdrawalError("There is no testimony to withdraw.")
    _request, token = start_by_account(account, testimony, WithdrawalScope.ACCOUNT)
    return token


@transaction.atomic
def confirm_closure(token):
    """Keep the testimony published without an account, or close an account with none (retention schedule, section 5)."""
    link = magic_links.redeem(MagicLink.Purpose.CLOSURE, token)
    if link is None:
        return None
    account = (
        Account.objects.exclude(status=Account.Status.CLOSED)
        .filter(email=link.email)
        .first()
    )
    if account is None:
        return None
    now = timezone.now()
    testimony = account.testimonies.first()
    if testimony is None or testimony.state != Testimony.State.PUBLISHED:
        account.status = Account.Status.CLOSED
        account.closed_at = now
        account.save(update_fields=["status", "closed_at"])
        return ""
    code = new_withdrawal_code()
    testimony.account = None
    testimony.withdrawal_code_hash = code_digest(normalize_code(code))
    testimony.closed_account_email_hmac = hashing.email_key(account.email)
    testimony.save()
    account.status = Account.Status.CLOSED
    account.closed_at = now
    account.save(update_fields=["status", "closed_at"])
    send_withdrawal_code(account.email, code)
    return code
