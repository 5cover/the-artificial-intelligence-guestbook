import hashlib
import secrets
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from accounts.models import MagicLink

LIFETIME = timedelta(minutes=15)


def _digest(token):
    return hashlib.sha256(token.encode()).digest()


def _valid(purpose, token):
    return MagicLink.objects.filter(
        token_hash=_digest(token),
        purpose=purpose,
        used_at__isnull=True,
        expires_at__gt=timezone.now(),
    )


def issue(purpose, email, **subject):
    token = secrets.token_urlsafe(32)
    now = timezone.now()
    MagicLink.objects.create(
        purpose=purpose,
        token_hash=_digest(token),
        email=email,
        created_at=now,
        expires_at=now + LIFETIME,
        **subject,
    )
    return token


def peek(purpose, token):
    return _valid(purpose, token).first()


def redeem(purpose, token):
    with transaction.atomic():
        link = _valid(purpose, token).select_for_update().first()
        if link is None:
            return None
        link.used_at = timezone.now()
        link.save(update_fields=["used_at"])
    return link
