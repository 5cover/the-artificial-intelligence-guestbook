from datetime import timedelta

import pytest
from django.core.management import call_command
from django.utils import timezone

from accounts.models import MagicLink, RateLimitHit


@pytest.mark.django_db
def test_purge_keeps_recent_rows_and_deletes_rows_older_than_a_day():
    now = timezone.now()
    old = now - timedelta(hours=25)
    MagicLink.objects.create(
        purpose="sign-in",
        token_hash=b"o" * 32,
        email="old@example.org",
        created_at=old,
        expires_at=old + timedelta(minutes=15),
    )
    MagicLink.objects.create(
        purpose="sign-in",
        token_hash=b"r" * 32,
        email="recent@example.org",
        created_at=now,
        expires_at=now + timedelta(minutes=15),
    )
    RateLimitHit.objects.create(scope="sign-in-email", key=b"k", created_at=old)
    RateLimitHit.objects.create(scope="sign-in-email", key=b"k", created_at=now)

    call_command("purge_expired")

    assert list(MagicLink.objects.values_list("email", flat=True)) == [
        "recent@example.org"
    ]
    assert RateLimitHit.objects.count() == 1
