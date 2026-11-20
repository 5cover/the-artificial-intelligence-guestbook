import hashlib

from accounts import proof_of_work


def test_leading_zero_bits_counts_across_bytes():
    assert proof_of_work.leading_zero_bits(b"\x00\x00\x80") == 16
    assert proof_of_work.leading_zero_bits(b"\x01") == 7
    assert proof_of_work.leading_zero_bits(b"\x80") == 0
    assert proof_of_work.leading_zero_bits(b"\x00\x0f") == 12


def _solve(challenge, bits):
    nonce = 0
    while True:
        digest = hashlib.sha256(f"{challenge}:{nonce}".encode()).digest()
        if proof_of_work.leading_zero_bits(digest) >= bits:
            return str(nonce)
        nonce += 1


def test_verify_accepts_a_solution_for_the_issued_challenge(settings):
    settings.POW_DIFFICULTY_BITS = 8
    assert proof_of_work.verify("abc", "abc", _solve("abc", 8))


def test_verify_rejects_another_challenge_or_a_missing_one(settings):
    settings.POW_DIFFICULTY_BITS = 8
    nonce = _solve("abc", 8)
    assert not proof_of_work.verify("abc", "xyz", nonce)
    assert not proof_of_work.verify("abc", "", nonce)
    assert not proof_of_work.verify(None, "abc", nonce)


def test_verify_rejects_a_nonce_that_is_not_a_solution(settings):
    settings.POW_DIFFICULTY_BITS = 24
    assert not proof_of_work.verify("abc", "abc", "0")
