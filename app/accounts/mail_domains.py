from functools import cache
from pathlib import Path

import dns.exception
import dns.resolver

BLOCKLIST = Path(__file__).resolve().parent / "data" / "disposable-domains.txt"


@cache
def disposable_domains():
    lines = BLOCKLIST.read_text(encoding="utf-8").splitlines()
    return frozenset(
        line.strip().lower()
        for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    )


def is_disposable(domain):
    labels = domain.lower().split(".")
    return any(
        ".".join(labels[index:]) in disposable_domains()
        for index in range(len(labels) - 1)
    )


def accepts_mail(domain):
    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=5)
    except dns.exception.DNSException:
        return False
    return any(str(answer.exchange) != "." for answer in answers)
