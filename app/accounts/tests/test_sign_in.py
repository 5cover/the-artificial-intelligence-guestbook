import re
from datetime import timedelta

import pytest
from django.core import mail
from django.utils import timezone

from accounts import proof_of_work
from accounts.models import Account, MagicLink
from accounts.tests.test_proof_of_work import _solve

SIGN_IN = "/sign-in/"
LINK_PATTERN = re.compile(r"https://\S+/sign-in/link/([\w-]+)/")


def request_link(client, email, *, nonce="", remote_addr="198.51.100.1"):
    page = client.get(SIGN_IN)
    challenge = client.session[proof_of_work.SESSION_KEY]
    response = client.post(
        SIGN_IN,
        {"email": email, "pow_challenge": challenge, "pow_nonce": nonce},
        REMOTE_ADDR=remote_addr,
    )
    return response, page


def token_from_outbox():
    return LINK_PATTERN.search(mail.outbox[-1].body).group(1)


@pytest.mark.django_db
def test_sign_in_page_carries_a_challenge_and_a_strict_security_policy(client):
    response = client.get(SIGN_IN)
    assert response.status_code == 200
    assert b'name="pow_challenge"' in response.content
    assert client.session[proof_of_work.SESSION_KEY]
    assert "style-src 'none'" in response["Content-Security-Policy"]
    assert "script-src 'self'" in response["Content-Security-Policy"]


@pytest.mark.django_db
def test_sign_in_sends_one_single_use_link_valid_for_15_minutes(client):
    response, _page = request_link(client, "Contributor@Example.org")
    assert response.status_code == 302
    assert response["Location"] == "/sign-in/sent/"
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["contributor@example.org"]

    link = MagicLink.objects.get()
    assert link.purpose == "sign-in"
    assert link.email == "contributor@example.org"
    assert link.expires_at - link.created_at == timedelta(minutes=15)
    assert bytes(link.token_hash) != token_from_outbox().encode()


@pytest.mark.django_db
def test_known_and_new_addresses_get_the_same_response(client):
    Account.objects.create(email="known@example.org", created_at=timezone.now())
    known, _ = request_link(client, "known@example.org", remote_addr="198.51.100.2")
    new, _ = request_link(client, "new@example.org", remote_addr="198.51.100.3")
    assert known.status_code == new.status_code == 302
    assert known["Location"] == new["Location"]
    assert len(mail.outbox) == 2


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email", ["someone@mailinator.com", "someone@inbox.yopmail.com"]
)
def test_disposable_addresses_are_refused_without_sending(client, email):
    response, _ = request_link(client, email)
    assert response.status_code == 200
    assert "Disposable addresses are not accepted" in response.content.decode()
    assert mail.outbox == []


@pytest.mark.django_db
def test_domain_without_mx_records_is_refused(client, monkeypatch):
    monkeypatch.setattr("accounts.mail_domains.accepts_mail", lambda domain: False)
    response, _ = request_link(client, "someone@example.org")
    assert response.status_code == 200
    assert "does not accept email" in response.content.decode()
    assert mail.outbox == []


@pytest.mark.django_db
def test_invalid_email_is_refused(client):
    response, _ = request_link(client, "not-an-address")
    assert response.status_code == 200
    assert mail.outbox == []


@pytest.mark.django_db
def test_without_javascript_the_network_limit_is_stricter(client):
    for index in range(3):
        response, _ = request_link(
            client, f"person{index}@example.org", remote_addr="198.51.100.9"
        )
        assert response.status_code == 302
    response, _ = request_link(
        client, "person9@example.org", remote_addr="198.51.100.9"
    )
    assert response.status_code == 200
    assert "Too many sign-in requests" in response.content.decode()
    assert len(mail.outbox) == 3


@pytest.mark.django_db
def test_the_address_limit_applies_across_networks(client):
    for index in range(5):
        response, _ = request_link(
            client, "repeat@example.org", remote_addr=f"198.51.100.{index + 20}"
        )
        assert response.status_code == 302
    response, _ = request_link(
        client, "repeat@example.org", remote_addr="198.51.100.99"
    )
    assert "Too many sign-in requests" in response.content.decode()
    assert len(mail.outbox) == 5


@pytest.mark.django_db
def test_a_valid_proof_of_work_is_accepted(client, settings):
    settings.POW_DIFFICULTY_BITS = 8
    client.get(SIGN_IN)
    challenge = client.session[proof_of_work.SESSION_KEY]
    response = client.post(
        SIGN_IN,
        {
            "email": "proved@example.org",
            "pow_challenge": challenge,
            "pow_nonce": _solve(challenge, 8),
        },
        REMOTE_ADDR="198.51.100.40",
    )
    assert response.status_code == 302
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_an_invalid_proof_of_work_is_refused(client, settings):
    settings.POW_DIFFICULTY_BITS = 24
    client.get(SIGN_IN)
    challenge = client.session[proof_of_work.SESSION_KEY]
    response = client.post(
        SIGN_IN,
        {"email": "guess@example.org", "pow_challenge": challenge, "pow_nonce": "1"},
    )
    assert response.status_code == 200
    assert "browser check did not verify" in response.content.decode()
    assert mail.outbox == []


@pytest.mark.django_db
def test_a_proof_of_work_cannot_be_replayed(client, settings):
    settings.POW_DIFFICULTY_BITS = 8
    client.get(SIGN_IN)
    challenge = client.session[proof_of_work.SESSION_KEY]
    nonce = _solve(challenge, 8)
    data = {"email": "once@example.org", "pow_challenge": challenge, "pow_nonce": nonce}
    assert client.post(SIGN_IN, data).status_code == 302
    replay = client.post(SIGN_IN, {**data, "email": "again@example.org"})
    assert replay.status_code == 200
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_opening_the_link_does_not_consume_it(client):
    request_link(client, "scanner@example.org")
    token = token_from_outbox()

    assert client.get(f"/sign-in/link/{token}/").status_code == 200
    assert client.get(f"/sign-in/link/{token}/").status_code == 200
    assert "account_id" not in client.session
    assert MagicLink.objects.get().used_at is None


@pytest.mark.django_db
def test_confirming_the_link_signs_in_once(client):
    request_link(client, "member@example.org")
    token = token_from_outbox()

    response = client.post(f"/sign-in/link/{token}/")
    assert response.status_code == 302
    assert response["Location"] == "/account/"
    account = Account.objects.get(email="member@example.org")
    assert account.email_verified_at is not None
    assert account.last_sign_in_at is not None
    assert client.get("/account/").status_code == 200

    assert client.post(f"/sign-in/link/{token}/").status_code == 404


@pytest.mark.django_db
def test_an_expired_link_is_refused(client):
    request_link(client, "late@example.org")
    token = token_from_outbox()
    past = timezone.now() - timedelta(minutes=30)
    MagicLink.objects.update(created_at=past, expires_at=past + timedelta(minutes=15))

    assert client.get(f"/sign-in/link/{token}/").status_code == 404
    assert client.post(f"/sign-in/link/{token}/").status_code == 404
    assert not Account.objects.exists()


@pytest.mark.django_db
def test_a_closed_account_cannot_sign_in(client):
    now = timezone.now()
    Account.objects.create(
        email="gone@example.org", created_at=now, status="closed", closed_at=now
    )
    request_link(client, "gone@example.org")
    token = token_from_outbox()

    assert client.post(f"/sign-in/link/{token}/").status_code == 403
    assert "account_id" not in client.session


@pytest.mark.django_db
def test_sign_out_requires_post_and_forgets_the_account(client):
    request_link(client, "leaving@example.org")
    client.post(f"/sign-in/link/{token_from_outbox()}/")

    assert client.get("/sign-out/").status_code == 405
    assert client.post("/sign-out/").status_code == 302
    assert client.get("/account/").status_code == 302


@pytest.mark.django_db
def test_account_page_requires_sign_in(client):
    response = client.get("/account/")
    assert response.status_code == 302
    assert response["Location"] == "/sign-in/"
