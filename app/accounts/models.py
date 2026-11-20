from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from guestbook.constraints import iff, implies, not_earlier_than


class Account(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        RESTRICTED = "restricted", _("Restricted")
        CLOSED = "closed", _("Closed")

    class Locale(models.TextChoices):
        ENGLISH = "en", _("English")
        FRENCH = "fr", _("French")

    internal_id = models.BigAutoField(primary_key=True, db_comment="private | id")
    email = models.EmailField(max_length=254, unique=True, db_comment="private | email")
    email_verified_at = models.DateTimeField(null=True, db_comment="private | instant?")
    created_at = models.DateTimeField(db_comment="private | instant")
    last_sign_in_at = models.DateTimeField(null=True, db_comment="private | instant?")
    interface_locale = models.CharField(
        max_length=2,
        choices=Locale,
        default=Locale.ENGLISH,
        db_comment="private | enum(en, fr)",
    )
    status = models.CharField(
        max_length=12,
        choices=Status,
        default=Status.ACTIVE,
        db_comment="operational | enum(active, restricted, closed)",
    )
    restriction_reason = models.CharField(
        max_length=200, null=True, db_comment="operational | line(200)?"
    )
    closed_at = models.DateTimeField(null=True, db_comment="private | instant?")

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="account_email_is_lowercase",
                condition=Q(email__regex=r"^[^A-Z]+$"),
            ),
            models.CheckConstraint(
                name="account_closed_iff_closed_at",
                condition=iff(Q(status="closed"), Q(closed_at__isnull=False)),
            ),
            models.CheckConstraint(
                name="account_restricted_iff_reason",
                condition=iff(
                    Q(status="restricted"), Q(restriction_reason__isnull=False)
                ),
            ),
            models.CheckConstraint(
                name="account_dates_follow_creation",
                condition=(
                    not_earlier_than("email_verified_at", "created_at")
                    & not_earlier_than("last_sign_in_at", "created_at")
                    & not_earlier_than("closed_at", "created_at")
                ),
            ),
        ]


class MagicLink(models.Model):
    class Purpose(models.TextChoices):
        SIGN_IN = "sign-in", _("Sign in")
        WITHDRAWAL = "withdrawal", _("Withdrawal")
        PARENTAL = "parental", _("Parental consent")
        REPORT = "report", _("Report confirmation")

    internal_id = models.BigAutoField(primary_key=True, db_comment="operational | id")
    purpose = models.CharField(
        max_length=12,
        choices=Purpose,
        db_comment="operational | enum(sign-in, withdrawal, parental, report)",
    )
    token_hash = models.BinaryField(unique=True, db_comment="operational | hash")
    email = models.EmailField(max_length=254, db_comment="operational | email")
    created_at = models.DateTimeField(db_comment="operational | instant")
    expires_at = models.DateTimeField(db_comment="operational | instant")
    used_at = models.DateTimeField(null=True, db_comment="operational | instant?")
    testimony = models.ForeignKey(
        "testimonies.Testimony",
        null=True,
        on_delete=models.CASCADE,
        related_name="magic_links",
        db_comment="operational | ref(Testimony)?",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="magic_link_expires_after_creation",
                condition=Q(expires_at__gt=models.F("created_at")),
            ),
            models.CheckConstraint(
                name="magic_link_parental_has_testimony",
                condition=implies(Q(purpose="parental"), Q(testimony__isnull=False)),
            ),
            models.CheckConstraint(
                name="magic_link_used_within_validity",
                condition=Q(used_at__isnull=True)
                | (
                    Q(used_at__gte=models.F("created_at"))
                    & Q(used_at__lte=models.F("expires_at"))
                ),
            ),
        ]


class RateLimitHit(models.Model):
    internal_id = models.BigAutoField(primary_key=True, db_comment="operational | id")
    scope = models.CharField(max_length=40, db_comment="operational | line(40)")
    key = models.BinaryField(db_comment="operational | hash")
    created_at = models.DateTimeField(db_comment="operational | instant")

    class Meta:
        indexes = [
            models.Index(
                fields=["scope", "key", "created_at"], name="ratelimit_lookup"
            ),
        ]
