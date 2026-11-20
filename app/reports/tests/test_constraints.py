import pytest
from django.db import IntegrityError, transaction
from django.utils import timezone

from reports.models import Notice


def notice(**overrides):
    values = {
        "received_at": timezone.now(),
        "reason": "spam",
        "priority": "low",
        "testimony_public_id": "7q4km2xd",
        "grounds": "Spam.",
    }
    values.update(overrides)
    return Notice.objects.create(**values)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("constraint", "overrides"),
    [
        ("notice_public_id_pattern", {"testimony_public_id": "7Q4KM2XD"}),
        ("notice_reason_enum", {"reason": "bogus"}),
        ("notice_priority_enum", {"priority": "bogus"}),
        ("notice_outcome_iff_outcome_at", {"outcome": "no-action"}),
    ],
)
def test_notice_rejects_invalid_states(constraint, overrides):
    with pytest.raises(IntegrityError) as error, transaction.atomic():
        notice(**overrides)
    assert constraint in str(error.value)


@pytest.mark.django_db
def test_a_complete_notice_is_accepted():
    now = timezone.now()
    notice(outcome="no-action", outcome_at=now)
