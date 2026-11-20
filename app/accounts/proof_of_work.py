import hashlib
import hmac
import secrets

from django.conf import settings

SESSION_KEY = "proof_of_work_challenge"


def leading_zero_bits(digest):
    bits = 0
    for byte in digest:
        if byte == 0:
            bits += 8
            continue
        return bits + 8 - byte.bit_length()
    return bits


def is_solution(challenge, nonce):
    digest = hashlib.sha256(f"{challenge}:{nonce}".encode()).digest()
    return leading_zero_bits(digest) >= settings.POW_DIFFICULTY_BITS


def issue_challenge(request):
    challenge = secrets.token_hex(16)
    request.session[SESSION_KEY] = challenge
    return challenge


def take_challenge(request):
    # A challenge is single-use: taking it removes it from the session.
    return request.session.pop(SESSION_KEY, None)


def verify(expected, submitted, nonce):
    if not expected or not submitted:
        return False
    same = hmac.compare_digest(expected.encode(), submitted.encode())
    return same and is_solution(expected, nonce)
