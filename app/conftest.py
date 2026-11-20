from types import SimpleNamespace

import dns.name
import pytest
from django.utils import timezone

from accounts.models import Account
from accounts.session import SESSION_KEY


@pytest.fixture(autouse=True)
def mx_resolution_is_offline(monkeypatch):
    # Keep the suite offline: every domain publishes an MX host. Tests of the
    # MX check replace this stub.
    answers = [SimpleNamespace(exchange=dns.name.from_text("mx.example.test."))]
    monkeypatch.setattr("dns.resolver.resolve", lambda *args, **kwargs: answers)


@pytest.fixture
def contributor(client):
    now = timezone.now()
    account = Account.objects.create(
        email="contributor@example.org",
        created_at=now,
        email_verified_at=now,
        last_sign_in_at=now,
    )
    session = client.session
    session[SESSION_KEY] = account.pk
    session.save()
    return account
