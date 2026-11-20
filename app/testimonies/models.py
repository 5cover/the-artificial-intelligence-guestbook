from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import F, Q
from django.db.models.functions import ExtractYear, Length
from django.db.models.lookups import GreaterThanOrEqual, LessThanOrEqual
from django.utils.translation import gettext_lazy as _

from guestbook.constraints import iff, implies
from testimonies import vocabularies as vocab

PUBLIC_ID_PATTERN = r"^[0-9a-hjkmnp-tv-z]{8}$"
LANGUAGE_PATTERN = r"^[A-Za-z]{2,8}(-[A-Za-z0-9]{1,8})*$"
BODY_MAX_LENGTH = 50000


def enum_check(name, field, choices):
    return models.CheckConstraint(
        name=name,
        condition=Q(**{f"{field}__in": list(choices)})
        | Q(**{f"{field}__isnull": True}),
    )


class Testimony(models.Model):
    class State(models.TextChoices):
        DRAFT = "draft", _("Draft")
        SUBMITTED = "submitted", _("Submitted")
        PUBLISHED = "published", _("Published")
        QUARANTINED = "quarantined", _("Quarantined")
        WITHDRAWN = "withdrawn", _("Withdrawn")

    class QuarantineReason(models.TextChoices):
        AWAITING_EDIT = "awaiting-edit", _("Awaiting an edit")
        LEGAL_HOLD = "legal-hold", _("Legal hold")

    class Licence(models.TextChoices):
        CC_BY_4_0 = "CC-BY-4.0", _("CC BY 4.0")

    internal_id = models.BigAutoField(primary_key=True, db_comment="private | id")
    public_id = models.CharField(
        max_length=8, null=True, unique=True, db_comment="public | public_id?"
    )
    account = models.ForeignKey(
        "accounts.Account",
        null=True,
        on_delete=models.SET_NULL,
        related_name="testimonies",
        db_comment="private | ref(Account)?",
    )
    state = models.CharField(
        max_length=12,
        choices=State,
        default=State.DRAFT,
        db_comment="operational | enum(draft, submitted, published, quarantined, withdrawn)",
    )
    quarantine_reason = models.CharField(
        max_length=14,
        choices=QuarantineReason,
        null=True,
        db_comment="operational | enum(awaiting-edit, legal-hold)?",
    )
    public_revision = models.ForeignKey(
        "Revision",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        db_comment="public | ref(Revision)?",
    )
    archived_revision = models.ForeignKey(
        "Revision",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        db_comment="public | ref(Revision)?",
    )
    language = models.CharField(max_length=35, null=True, db_comment="public | lang?")
    received_at = models.DateTimeField(null=True, db_comment="private | instant?")
    published_at = models.DateTimeField(null=True, db_comment="public | instant?")
    withdrawn_at = models.DateTimeField(null=True, db_comment="private | instant?")
    edition_period = models.PositiveSmallIntegerField(
        null=True, db_comment="public | year?"
    )
    licence = models.CharField(
        max_length=10,
        choices=Licence,
        default=Licence.CC_BY_4_0,
        db_comment="public | enum(CC-BY-4.0)",
    )
    withdrawal_code_hash = models.BinaryField(null=True, db_comment="private | hash?")
    closed_account_email_hmac = models.BinaryField(
        null=True, db_comment="private | hash?"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["account"],
                condition=Q(account__isnull=False),
                name="one_testimony_per_account",
            ),
            models.CheckConstraint(
                name="testimony_public_id_pattern",
                condition=Q(public_id__isnull=True)
                | Q(public_id__regex=PUBLIC_ID_PATTERN),
            ),
            models.CheckConstraint(
                name="testimony_language_is_bcp47",
                condition=Q(language__isnull=True)
                | Q(language__regex=LANGUAGE_PATTERN),
            ),
            models.CheckConstraint(
                name="testimony_edition_period_from_2026",
                condition=Q(edition_period__isnull=True) | Q(edition_period__gte=2026),
            ),
            enum_check(
                "testimony_state_enum",
                "state",
                ["draft", "submitted", "published", "quarantined", "withdrawn"],
            ),
            enum_check(
                "testimony_quarantine_reason_enum",
                "quarantine_reason",
                ["awaiting-edit", "legal-hold"],
            ),
            models.CheckConstraint(
                name="testimony_public_id_iff_published",
                condition=iff(Q(public_id__isnull=True), Q(published_at__isnull=True)),
            ),
            models.CheckConstraint(
                name="testimony_published_states_have_public_id",
                condition=implies(
                    Q(state__in=["published", "withdrawn"]),
                    Q(public_id__isnull=False),
                ),
            ),
            models.CheckConstraint(
                name="testimony_withdrawn_iff_withdrawn_at",
                condition=iff(Q(state="withdrawn"), Q(withdrawn_at__isnull=False)),
            ),
            models.CheckConstraint(
                name="testimony_submitted_has_receipt_language_and_period",
                condition=implies(
                    ~Q(state="draft"),
                    Q(received_at__isnull=False)
                    & Q(language__isnull=False)
                    & Q(edition_period__isnull=False),
                ),
            ),
            models.CheckConstraint(
                name="testimony_period_is_utc_year_of_receipt",
                condition=Q(received_at__isnull=True)
                | Q(edition_period=ExtractYear("received_at")),
            ),
            models.CheckConstraint(
                name="testimony_withdrawn_has_no_account",
                condition=implies(Q(state="withdrawn"), Q(account__isnull=True)),
            ),
            models.CheckConstraint(
                name="testimony_quarantine_iff_reason",
                condition=iff(
                    Q(state="quarantined"), Q(quarantine_reason__isnull=False)
                ),
            ),
            models.CheckConstraint(
                name="testimony_published_has_revisions",
                condition=implies(
                    Q(state="published"),
                    Q(public_revision__isnull=False)
                    & Q(archived_revision__isnull=False),
                ),
            ),
            models.CheckConstraint(
                name="testimony_codes_only_without_account",
                condition=implies(
                    Q(withdrawal_code_hash__isnull=False)
                    | Q(closed_account_email_hmac__isnull=False),
                    Q(account__isnull=True),
                ),
            ),
        ]


class Revision(models.Model):
    class ReviewState(models.TextChoices):
        PENDING = "pending", _("Pending")
        APPROVED = "approved", _("Approved")
        RETURNED = "returned", _("Returned")

    internal_id = models.BigAutoField(primary_key=True, db_comment="private | id")
    testimony = models.ForeignKey(
        Testimony,
        on_delete=models.CASCADE,
        related_name="revisions",
        db_comment="operational | ref(Testimony)",
    )
    sequence = models.PositiveIntegerField(db_comment="operational | pos")
    revision_number = models.PositiveIntegerField(null=True, db_comment="public | pos?")
    review_state = models.CharField(
        max_length=8,
        choices=ReviewState,
        default=ReviewState.PENDING,
        db_comment="operational | enum(pending, approved, returned)",
    )
    body = models.TextField(null=True, db_comment="public | markdown(50000)?")
    summary = models.CharField(
        max_length=200, null=True, db_comment="public | line(200)?"
    )
    submitted_at = models.DateTimeField(db_comment="private | instant")
    live_at = models.DateTimeField(null=True, db_comment="public | instant?")
    reviewed_at = models.DateTimeField(null=True, db_comment="operational | instant?")
    review_record = models.ForeignKey(
        "moderation.ModerationRecord",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        db_comment="operational | ref(ModerationRecord)?",
    )

    # Public identity (data model, section 2.4). Values belong to the revision,
    # because identity edits go through the same review as text (section 2.5, rule 11).
    identity_mode = models.CharField(
        max_length=12,
        choices=vocab.IdentityMode,
        default=vocab.IdentityMode.ANONYMOUS,
        db_comment="public | enum(IdentityMode)",
    )
    display_name = models.CharField(
        max_length=100, null=True, db_comment="public | line(100)?"
    )
    age_range = models.CharField(
        max_length=8,
        choices=vocab.AgeRange,
        null=True,
        db_comment="public | enum(AgeRange)?",
    )
    country = models.CharField(max_length=2, null=True, db_comment="public | country?")
    region = models.CharField(
        max_length=100, null=True, db_comment="public | line(100)?"
    )
    languages = models.JSONField(null=True, db_comment="public | list(lang)?")
    profession = models.CharField(
        max_length=100, null=True, db_comment="public | line(100)?"
    )
    field = models.CharField(
        max_length=20,
        choices=vocab.Field,
        null=True,
        db_comment="public | enum(Field)?",
    )
    field_note = models.CharField(
        max_length=200, null=True, db_comment="public | line(200)?"
    )
    organization = models.CharField(
        max_length=200, null=True, db_comment="public | line(200)?"
    )
    organization_type = models.CharField(
        max_length=14,
        choices=vocab.OrganizationType,
        null=True,
        db_comment="public | enum(OrganizationType)?",
    )
    organization_type_note = models.CharField(
        max_length=200, null=True, db_comment="public | line(200)?"
    )
    relationship_to_ai = ArrayField(
        models.CharField(max_length=20, choices=vocab.RelationshipToAI),
        null=True,
        db_comment="public | set(enum(RelationshipToAI))?",
    )
    relationship_to_ai_note = models.CharField(
        max_length=200, null=True, db_comment="public | line(200)?"
    )
    link = models.URLField(max_length=2000, null=True, db_comment="public | url?")

    # Authorship disclosure (data model, section 2.6).
    authorship_category = models.CharField(
        max_length=24,
        choices=vocab.AuthorshipCategory,
        default=vocab.AuthorshipCategory.UNDISCLOSED,
        db_comment="public | enum(AuthorshipCategory)",
    )
    provider = models.CharField(
        max_length=100, null=True, db_comment="public | line(100)?"
    )
    product = models.CharField(
        max_length=100, null=True, db_comment="public | line(100)?"
    )
    model = models.CharField(
        max_length=100, null=True, db_comment="public | line(100)?"
    )
    model_version = models.CharField(
        max_length=100, null=True, db_comment="public | line(100)?"
    )
    mode_or_setting = models.CharField(
        max_length=200, null=True, db_comment="public | line(200)?"
    )
    inputs = models.TextField(
        max_length=1000, null=True, db_comment="public | markdown(1000)?"
    )
    workflow = models.TextField(
        max_length=1000, null=True, db_comment="public | markdown(1000)?"
    )
    changes_after = models.TextField(
        max_length=1000, null=True, db_comment="public | markdown(1000)?"
    )
    comment = models.TextField(
        max_length=1000, null=True, db_comment="public | markdown(1000)?"
    )

    # Structured testimony fields (data model, section 2.7).
    ai_use_frequency = models.CharField(
        max_length=12,
        choices=vocab.AIUseFrequency,
        null=True,
        db_comment="public | enum(AIUseFrequency)?",
    )
    tools_used = models.JSONField(null=True, db_comment="public | list(line(100))?")
    attitude = models.CharField(
        max_length=12,
        choices=vocab.Attitude,
        null=True,
        db_comment="public | enum(Attitude)?",
    )
    attitude_note = models.CharField(
        max_length=200, null=True, db_comment="public | line(200)?"
    )
    prediction = models.TextField(
        max_length=2000, null=True, db_comment="public | text(2000)?"
    )
    prediction_horizon = models.PositiveSmallIntegerField(
        null=True, db_comment="public | year?"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["testimony", "sequence"], name="revision_sequence_unique"
            ),
            models.UniqueConstraint(
                fields=["testimony", "revision_number"],
                name="revision_number_unique",
            ),
            models.CheckConstraint(
                name="revision_number_iff_live",
                condition=iff(Q(revision_number__isnull=True), Q(live_at__isnull=True)),
            ),
            models.CheckConstraint(
                name="revision_reviewed_iff_not_pending",
                condition=iff(Q(review_state="pending"), Q(reviewed_at__isnull=True)),
            ),
            models.CheckConstraint(
                name="revision_returned_has_record",
                condition=implies(
                    Q(review_state="returned"), Q(review_record__isnull=False)
                ),
            ),
            models.CheckConstraint(
                name="revision_body_length",
                condition=Q(body__isnull=True)
                | (
                    Q(GreaterThanOrEqual(Length("body"), 1))
                    & Q(LessThanOrEqual(Length("body"), BODY_MAX_LENGTH))
                ),
            ),
            models.CheckConstraint(
                name="revision_identity_mode_enum",
                condition=Q(identity_mode__in=vocab.IdentityMode.values),
            ),
            models.CheckConstraint(
                name="revision_anonymous_iff_no_display_name",
                condition=iff(
                    Q(identity_mode="anonymous"), Q(display_name__isnull=True)
                ),
            ),
            enum_check("revision_age_range_enum", "age_range", vocab.AgeRange.values),
            enum_check(
                "revision_organization_type_enum",
                "organization_type",
                vocab.OrganizationType.values,
            ),
            enum_check("revision_field_enum", "field", vocab.Field.values),
            enum_check(
                "revision_ai_use_frequency_enum",
                "ai_use_frequency",
                vocab.AIUseFrequency.values,
            ),
            enum_check("revision_attitude_enum", "attitude", vocab.Attitude.values),
            models.CheckConstraint(
                name="revision_authorship_category_enum",
                condition=Q(authorship_category__in=vocab.AuthorshipCategory.values),
            ),
            models.CheckConstraint(
                name="revision_country_is_iso_alpha2",
                condition=Q(country__isnull=True) | Q(country__regex=r"^[A-Z]{2}$"),
            ),
            models.CheckConstraint(
                name="revision_relationship_to_ai_codes",
                condition=Q(relationship_to_ai__isnull=True)
                | Q(relationship_to_ai__contained_by=vocab.RelationshipToAI.values),
            ),
            models.CheckConstraint(
                name="revision_relationship_to_ai_is_a_set",
                condition=Q(relationship_to_ai__isnull=True)
                | models.Func(
                    F("relationship_to_ai"),
                    function="guestbook_is_distinct",
                    output_field=models.BooleanField(),
                ),
            ),
            models.CheckConstraint(
                name="revision_no_authorship_details_without_ai",
                condition=implies(
                    Q(authorship_category__in=["none", "undisclosed"]),
                    Q(provider__isnull=True)
                    & Q(product__isnull=True)
                    & Q(model__isnull=True)
                    & Q(model_version__isnull=True)
                    & Q(mode_or_setting__isnull=True)
                    & Q(inputs__isnull=True)
                    & Q(workflow__isnull=True),
                ),
            ),
            models.CheckConstraint(
                name="revision_horizon_needs_prediction",
                condition=implies(
                    Q(prediction_horizon__isnull=False),
                    Q(prediction__isnull=False),
                ),
            ),
        ]


class ConsentRecord(models.Model):
    internal_id = models.BigAutoField(primary_key=True, db_comment="evidence | id")
    testimony = models.ForeignKey(
        Testimony,
        on_delete=models.CASCADE,
        related_name="consent_records",
        db_comment="evidence | ref(Testimony)",
    )
    revision = models.ForeignKey(
        Revision,
        on_delete=models.CASCADE,
        related_name="consent_records",
        db_comment="evidence | ref(Revision)",
    )
    publication_consent_at = models.DateTimeField(db_comment="evidence | instant")
    licence_grant_version = models.CharField(
        max_length=20, db_comment="evidence | line(20)"
    )
    terms_version = models.CharField(max_length=20, db_comment="evidence | line(20)")
    privacy_notice_version = models.CharField(
        max_length=20, db_comment="evidence | line(20)"
    )
    consent_locale = models.CharField(
        max_length=2,
        choices=vocab.ConsentLocale,
        db_comment="evidence | enum(en, fr)",
    )
    declared_age_band = models.CharField(
        max_length=12,
        choices=vocab.DeclaredAgeBand,
        db_comment="evidence | enum(under-16, 16-or-over)",
    )
    consent_path = models.CharField(
        max_length=10,
        choices=vocab.ConsentPath,
        db_comment="evidence | enum(self, parental)",
    )
    parental_consent_at = models.DateTimeField(
        null=True, db_comment="evidence | instant?"
    )
    parental_method = models.CharField(
        max_length=10,
        choices=vocab.ParentalMethod,
        null=True,
        db_comment="evidence | enum(email-link)?",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="consent_parental_path_iff_under_16",
                condition=iff(
                    Q(consent_path="parental"), Q(declared_age_band="under-16")
                ),
            ),
            models.CheckConstraint(
                name="consent_parental_consent_needs_parental_path",
                condition=implies(
                    Q(parental_consent_at__isnull=False),
                    Q(consent_path="parental"),
                ),
            ),
            models.CheckConstraint(
                name="consent_parental_method_iff_consent",
                condition=iff(
                    Q(parental_consent_at__isnull=True),
                    Q(parental_method__isnull=True),
                ),
            ),
        ]
