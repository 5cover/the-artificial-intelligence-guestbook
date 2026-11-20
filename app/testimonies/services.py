from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from accounts import magic_links
from accounts.models import MagicLink
from testimonies.models import ConsentRecord, Revision, Testimony
from testimonies.revisions import SubmissionError, check_minor_rules
from testimonies.vocabularies import (
    ConsentPath,
    DeclaredAgeBand,
    ParentalMethod,
)

LICENCE_GRANT_VERSION = "draft-2026-11-20"
TERMS_VERSION = "draft-2026-11-20"
PRIVACY_NOTICE_VERSION = "draft-2026-11-20"


def testimony_of(account):
    return Testimony.objects.filter(account=account).first()


@transaction.atomic
def save_draft(account, values):
    now = timezone.now()
    testimony = testimony_of(account)
    if testimony is None:
        testimony = Testimony.objects.create(account=account)
        revision = Revision(testimony=testimony, sequence=1)
    else:
        revision = testimony.revisions.get(sequence=1)
    testimony.language = values["language"] or None
    testimony.save(update_fields=["language"])
    for name, value in values.items():
        if name != "language":
            setattr(revision, name, value or None)
    revision.submitted_at = now
    revision.save()
    return testimony


@transaction.atomic
def submit(testimony, declared_age_band):
    revision = testimony.revisions.get(sequence=1)
    if not revision.body or not testimony.language:
        raise SubmissionError(
            _("Write your testimony and choose its language before submitting.")
        )
    check_minor_rules(revision, declared_age_band)
    now = timezone.now()
    testimony.state = Testimony.State.SUBMITTED
    testimony.received_at = now
    testimony.edition_period = now.year
    testimony.save()
    revision.submitted_at = now
    revision.save(update_fields=["submitted_at"])
    return ConsentRecord.objects.create(
        testimony=testimony,
        revision=revision,
        publication_consent_at=now,
        licence_grant_version=LICENCE_GRANT_VERSION,
        terms_version=TERMS_VERSION,
        privacy_notice_version=PRIVACY_NOTICE_VERSION,
        consent_locale="en",
        declared_age_band=declared_age_band,
        consent_path=(
            ConsentPath.PARENTAL
            if declared_age_band == DeclaredAgeBand.UNDER_16
            else ConsentPath.SELF
        ),
    )


def awaiting_parental_consent(testimony):
    return ConsentRecord.objects.filter(
        testimony=testimony,
        consent_path=ConsentPath.PARENTAL,
        parental_consent_at__isnull=True,
    ).exists()


def request_parental_link(testimony, parent_email):
    return magic_links.issue(
        MagicLink.Purpose.PARENTAL, parent_email, testimony=testimony
    )


@transaction.atomic
def confirm_parental_consent(link):
    now = timezone.now()
    consent = (
        ConsentRecord.objects.filter(
            testimony=link.testimony,
            consent_path=ConsentPath.PARENTAL,
            parental_consent_at__isnull=True,
        )
        .order_by("-publication_consent_at")
        .first()
    )
    if consent is None:
        return False
    consent.parental_consent_at = now
    consent.parental_method = ParentalMethod.EMAIL_LINK
    consent.save(update_fields=["parental_consent_at", "parental_method"])
    # The parent's address is needed only for this confirmation (retention schedule, row 13).
    MagicLink.objects.filter(
        testimony=link.testimony, purpose=MagicLink.Purpose.PARENTAL
    ).delete()
    return True


def public_site_url(path):
    return settings.PUBLIC_BASE_URL.rstrip("/") + path
