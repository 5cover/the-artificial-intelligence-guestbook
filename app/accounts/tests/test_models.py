from datetime import timedelta

import pytest
from django.db import IntegrityError, transaction
from django.utils import timezone

from accounts.models import Account, MagicLink


def make_account(**overrides):
    values = {"email": "contributor@example.org", "created_at": timezone.now()}
    values.update(overrides)
    return Account.objects.create(**values)


@pytest.mark.django_db
def test_valid_account_states_are_accepted():
    now = timezone.now()
    make_account(
        created_at=now,
        email="a@example.org",
        status="restricted",
        restriction_reason="spam",
    )
    make_account(created_at=now, email="b@example.org", status="closed", closed_at=now)
    make_account(
        created_at=now,
        email="c@example.org",
        email_verified_at=now,
        last_sign_in_at=now,
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "overrides",
    [
        {"email": "Mixed.Case@example.org"},
        {"status": "closed"},
        {"closed_at": timezone.now()},
        {"status": "restricted"},
        {"restriction_reason": "spam"},
        {"email_verified_at": timezone.now() - timedelta(days=1)},
        {"last_sign_in_at": timezone.now() - timedelta(days=1)},
    ],
    ids=[
        "email-not-lowercase",
        "closed-without-closed-at",
        "closed-at-while-active",
        "restricted-without-reason",
        "reason-while-active",
        "verified-before-creation",
        "sign-in-before-creation",
    ],
)
def test_account_rejects_invalid_state(overrides):
    with pytest.raises(IntegrityError), transaction.atomic():
        make_account(**overrides)


@pytest.mark.django_db
def test_email_is_unique():
    make_account(email="same@example.org")
    with pytest.raises(IntegrityError), transaction.atomic():
        make_account(email="same@example.org")


@pytest.mark.django_db
def test_magic_link_expiry_must_follow_creation():
    now = timezone.now()
    with pytest.raises(IntegrityError), transaction.atomic():
        MagicLink.objects.create(
            purpose="sign-in",
            token_hash=b"x" * 32,
            email="a@example.org",
            created_at=now,
            expires_at=now,
        )


@pytest.mark.django_db
@pytest.mark.parametrize("offset", [timedelta(seconds=-1), timedelta(minutes=16)])
def test_magic_link_use_must_lie_within_its_validity(offset):
    now = timezone.now()
    with pytest.raises(IntegrityError), transaction.atomic():
        MagicLink.objects.create(
            purpose="sign-in",
            token_hash=b"y" * 32,
            email="a@example.org",
            created_at=now,
            expires_at=now + timedelta(minutes=15),
            used_at=now + offset,
        )
