from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from guestbook.constraints import iff

PUBLIC_ID_PATTERN = r"^[0-9a-hjkmnp-tv-z]{8}$"


class Notice(models.Model):
    class Reason(models.TextChoices):
        CSAM = "csam", _("Child sexual abuse material")
        THREAT = "threat", _("A threat to someone's life or safety")
        DOXXING = (
            "doxxing",
            _(
                "It exposes someone's address, contact details or other identifying information"
            ),
        )
        ABOUT_ME = (
            "about-me",
            _("It is about me, or names me, and exposes my private life"),
        )
        IMPERSONATION = (
            "impersonation",
            _(
                "Someone is publishing under my name, or under the name of a person I represent"
            ),
        )
        SECRETS = "secrets", _("It contains a password, key or other secret")
        DEFAMATION = (
            "defamation",
            _("It makes false or damaging accusations against an identifiable person"),
        )
        OTHER_ILLEGAL = "other-illegal", _("Other illegal content: hatred, terrorism")
        HARASSMENT = "harassment", _("Harassment")
        SPAM = "spam", _("Spam, advertising, or not a testimony")
        OTHER = "other", _("Something else")

    class Channel(models.TextChoices):
        FORM = "form", _("Form")
        EMAIL = "email", _("Email")
        POST = "post", _("Post")
        AUTHORITY = "authority", _("Authority")

    class Priority(models.TextChoices):
        URGENT = "urgent", _("Urgent")
        HIGH = "high", _("High")
        NORMAL = "normal", _("Normal")
        LOW = "low", _("Low")

    class Outcome(models.TextChoices):
        NO_ACTION = "no-action", _("No action")
        RETURNED = "returned", _("Returned to the contributor")
        REMOVED = "removed", _("Removed")
        QUARANTINED = "quarantined", _("Quarantined")
        REFERRED = "referred", _("Referred")

    internal_id = models.BigAutoField(primary_key=True, db_comment="private | id")
    received_at = models.DateTimeField(db_comment="operational | instant")
    channel = models.CharField(
        max_length=10,
        choices=Channel,
        default=Channel.FORM,
        db_comment="operational | enum(form, email, post, authority)",
    )
    reason = models.CharField(
        max_length=14,
        choices=Reason,
        db_comment="operational | enum(csam, threat, doxxing, about-me, impersonation, secrets, defamation, other-illegal, harassment, spam, other)",
    )
    priority = models.CharField(
        max_length=7,
        choices=Priority,
        db_comment="operational | enum(urgent, high, normal, low)",
    )
    confirmed_at = models.DateTimeField(null=True, db_comment="operational | instant?")
    auto_hidden = models.BooleanField(default=False, db_comment="operational | bool")
    testimony_public_id = models.CharField(
        max_length=8, db_comment="operational | public_id"
    )
    notifier_contact = models.TextField(
        max_length=1000, null=True, db_comment="operational | text(1000)?"
    )
    grounds = models.TextField(max_length=5000, db_comment="operational | text(5000)")
    outcome = models.CharField(
        max_length=12,
        choices=Outcome,
        null=True,
        db_comment="operational | enum(no-action, returned, removed, quarantined, referred)?",
    )
    outcome_at = models.DateTimeField(null=True, db_comment="operational | instant?")

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="notice_public_id_pattern",
                condition=Q(testimony_public_id__regex=PUBLIC_ID_PATTERN),
            ),
            models.CheckConstraint(
                name="notice_outcome_iff_outcome_at",
                condition=iff(Q(outcome__isnull=True), Q(outcome_at__isnull=True)),
            ),
            models.CheckConstraint(
                name="notice_reason_enum",
                condition=Q(
                    reason__in=[
                        "csam",
                        "threat",
                        "doxxing",
                        "about-me",
                        "impersonation",
                        "secrets",
                        "defamation",
                        "other-illegal",
                        "harassment",
                        "spam",
                        "other",
                    ]
                ),
            ),
            models.CheckConstraint(
                name="notice_priority_enum",
                condition=Q(priority__in=["urgent", "high", "normal", "low"]),
            ),
        ]
