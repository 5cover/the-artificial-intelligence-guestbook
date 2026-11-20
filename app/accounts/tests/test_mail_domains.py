from types import SimpleNamespace

import dns.exception
import dns.name
import dns.resolver
import pytest

from accounts import mail_domains


@pytest.mark.parametrize(
    "domain",
    ["mailinator.com", "inbox.mailinator.com", "YOPMAIL.com"],
)
def test_disposable_domains_and_their_subdomains_are_refused(domain):
    assert mail_domains.is_disposable(domain)


@pytest.mark.parametrize("domain", ["example.org", "mailinator.example.org", "com"])
def test_other_domains_are_accepted(domain):
    assert not mail_domains.is_disposable(domain)


def test_domain_with_mx_hosts_accepts_mail(monkeypatch):
    answers = [SimpleNamespace(exchange=dns.name.from_text("mx.example.org."))]
    monkeypatch.setattr(dns.resolver, "resolve", lambda *args, **kwargs: answers)
    assert mail_domains.accepts_mail("example.org")


def test_null_mx_does_not_accept_mail(monkeypatch):
    answers = [SimpleNamespace(exchange=dns.name.from_text("."))]
    monkeypatch.setattr(dns.resolver, "resolve", lambda *args, **kwargs: answers)
    assert not mail_domains.accepts_mail("example.org")


def test_missing_mx_records_refuse_mail(monkeypatch):
    def no_records(*args, **kwargs):
        raise dns.resolver.NXDOMAIN()

    monkeypatch.setattr(dns.resolver, "resolve", no_records)
    assert not mail_domains.accepts_mail("nowhere.invalid")


def test_dns_timeouts_refuse_mail(monkeypatch):
    def timeout(*args, **kwargs):
        raise dns.exception.Timeout()

    monkeypatch.setattr(dns.resolver, "resolve", timeout)
    assert not mail_domains.accepts_mail("example.org")
