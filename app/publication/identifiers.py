import re

CANONICAL = re.compile(r"^[0-9a-hjkmnp-tv-z]{8}$")


def normalize(raw):
    # Crockford decoding rules: case, hyphens and spaces are ignored; i and l read
    # as 1, o as 0 (identifiers, section 1.2). None when the result is not an identifier.
    value = raw.lower().replace("-", "").replace(" ", "")
    value = value.replace("i", "1").replace("l", "1").replace("o", "0")
    return value if CANONICAL.match(value) else None
