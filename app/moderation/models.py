from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from guestbook.constraints import implies


class ModerationRecord(models.Model):
    class Decision(models.TextChoices):
        APPROVE = "approve", _("Approve")
        RETURN = "return", _("Return")
        RETURN_AND_QUARANTINE = "return-and-quarantine", _("Return and quarantine")
        REMOVE = "remove", _("Remove")
        QUARANTINE = "quarantine", _("Quarantine")
        RESTRICT_ACCOUNT = "restrict-account", _("Restrict account")

    internal_id = models.BigAutoField(primary_key=True, db_comment="operational | id")
    testimony = models.ForeignKey(
        "testimonies.Testimony",
        null=True,
        on_delete=models.SET_NULL,
        related_name="moderation_records",
        db_comment="operational | ref(Testimony)?",
    )
    revision = models.ForeignKey(
        "testimonies.Revision",
        null=True,
        on_delete=models.SET_NULL,
        related_name="moderation_records",
        db_comment="operational | ref(Revision)?",
    )
    decision = models.CharField(
        max_length=24,
        choices=Decision,
        db_comment="operational | enum(approve, return, return-and-quarantine, remove, quarantine, restrict-account)",
    )
    guidance = models.TextField(
        max_length=2000, null=True, db_comment="operational | text(2000)?"
    )
    rule = models.CharField(
        max_length=50, null=True, db_comment="operational | line(50)?"
    )
    note = models.TextField(
        max_length=5000, null=True, db_comment="operational | text(5000)?"
    )
    decided_by = models.CharField(max_length=100, db_comment="operational | line(100)")
    decided_at = models.DateTimeField(db_comment="operational | instant")
    statement_sent_at = models.DateTimeField(
        null=True, db_comment="operational | instant?"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="moderation_returns_cite_a_rule",
                condition=implies(
                    Q(
                        decision__in=[
                            "return",
                            "return-and-quarantine",
                            "remove",
                            "restrict-account",
                        ]
                    ),
                    Q(rule__isnull=False),
                ),
            ),
            models.CheckConstraint(
                name="moderation_returns_give_guidance",
                condition=implies(
                    Q(decision__in=["return", "return-and-quarantine"]),
                    Q(guidance__isnull=False),
                ),
            ),
        ]
