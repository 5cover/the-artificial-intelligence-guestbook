import secrets

from django.db import transaction
from django.db.models import Max
from django.utils import timezone
from django.utils.translation import gettext as _

from testimonies.models import ConsentRecord, Revision, Testimony
from testimonies.vocabularies import DeclaredAgeBand, IdentityMode

PUBLIC_ID_ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"

# Optional content of a revision. Enumerations and dates stay: only the text
# and the details a contributor gave are removed from superseded revisions.
CONTENT_FIELDS = (
    "body",
    "display_name",
    "age_range",
    "country",
    "region",
    "languages",
    "profession",
    "field",
    "field_note",
    "organization",
    "organization_type",
    "organization_type_note",
    "relationship_to_ai",
    "relationship_to_ai_note",
    "link",
    "provider",
    "product",
    "model",
    "model_version",
    "mode_or_setting",
    "inputs",
    "workflow",
    "changes_after",
    "comment",
    "ai_use_frequency",
    "tools_used",
    "attitude",
    "attitude_note",
    "prediction",
    "prediction_horizon",
)

# Under 16, a testimony shows no age, link, region or organization (data model, section 2.4).
MINOR_RESTRICTED_FIELDS = (
    "age_range",
    "region",
    "link",
    "organization",
    "organization_type",
)


class SubmissionError(Exception):
    pass


def new_public_id():
    while True:
        candidate = "".join(secrets.choice(PUBLIC_ID_ALPHABET) for _ in range(8))
        if not Testimony.objects.filter(public_id=candidate).exists():
            return candidate


def current_revision(testimony):
    return testimony.revisions.order_by("-sequence").first()


def pending_revisions(testimony):
    return testimony.revisions.filter(
        review_state=Revision.ReviewState.PENDING
    ).order_by("sequence")


def apply_content(revision, values):
    for name, value in values.items():
        if name not in ("language", "publication_statement"):
            setattr(revision, name, value or None)


def check_minor_rules(revision, declared_age_band):
    if declared_age_band != DeclaredAgeBand.UNDER_16:
        return
    if revision.identity_mode == IdentityMode.NAMED:
        raise SubmissionError(
            _(
                "Someone under 16 can publish anonymously or under a pseudonym, not under their name."
            )
        )
    if any(getattr(revision, name) for name in MINOR_RESTRICTED_FIELDS):
        raise SubmissionError(
            _("Someone under 16 cannot give their age, region, organization or a link.")
        )


def make_public(testimony, revision, now):
    highest = testimony.revisions.aggregate(highest=Max("revision_number"))["highest"]
    revision.revision_number = (highest or 0) + 1
    revision.live_at = now
    revision.save(update_fields=["revision_number", "live_at"])


def release_superseded_text(testimony):
    # Keep only what the rules need: the public and archived revisions, pending
    # revisions, and the latest returned one (data model, section 2.5, rule 7).
    keep = {testimony.public_revision_id, testimony.archived_revision_id}
    keep.update(pending_revisions(testimony).values_list("pk", flat=True))
    latest_returned = (
        testimony.revisions.filter(review_state=Revision.ReviewState.RETURNED)
        .order_by("-sequence")
        .first()
    )
    if latest_returned is not None:
        keep.add(latest_returned.pk)
    for revision in testimony.revisions.exclude(pk__in=keep):
        for name in CONTENT_FIELDS:
            setattr(revision, name, None)
        revision.identity_mode = IdentityMode.ANONYMOUS
        revision.save()


@transaction.atomic
def submit_edit(testimony, values, now=None):
    now = now or timezone.now()
    latest = current_revision(testimony)
    consent = testimony.consent_records.order_by("-publication_consent_at").first()
    revision = Revision(
        testimony=testimony, sequence=latest.sequence + 1, submitted_at=now
    )
    apply_content(revision, values)
    if not revision.body:
        raise SubmissionError(_("Write your testimony before sending changes."))
    check_minor_rules(revision, consent.declared_age_band)
    revision.save()

    under_16 = consent.declared_age_band == DeclaredAgeBand.UNDER_16
    if testimony.state == Testimony.State.PUBLISHED and not under_16:
        make_public(testimony, revision, now)
        testimony.public_revision = revision
        testimony.save(update_fields=["public_revision"])

    ConsentRecord.objects.create(
        testimony=testimony,
        revision=revision,
        publication_consent_at=now,
        licence_grant_version=consent.licence_grant_version,
        terms_version=consent.terms_version,
        privacy_notice_version=consent.privacy_notice_version,
        consent_locale=consent.consent_locale,
        declared_age_band=consent.declared_age_band,
        consent_path=consent.consent_path,
        parental_consent_at=consent.parental_consent_at,
        parental_method=consent.parental_method,
    )
    release_superseded_text(testimony)
    return revision
