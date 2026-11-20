from types import SimpleNamespace

import dns.name
import pytest


@pytest.fixture(autouse=True)
def mx_resolution_is_offline(monkeypatch):
    # Keep the suite offline: every domain publishes an MX host. Tests of the
    # MX check replace this stub.
    answers = [SimpleNamespace(exchange=dns.name.from_text("mx.example.test."))]
    monkeypatch.setattr("dns.resolver.resolve", lambda *args, **kwargs: answers)
