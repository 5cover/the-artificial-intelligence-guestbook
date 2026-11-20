import hashlib
import hmac

from django.conf import settings
from django.utils import timezone


def _keyed(label, value):
    message = f"{label}\x00{value}".encode()
    return hmac.new(settings.SECRET_KEY.encode(), message, hashlib.sha256).digest()


def email_key(email):
    return _keyed("email", email.lower())


def address_key(address):
    # The salt is derived from the day, so keys cannot be linked across days.
    salt = _keyed("address-salt", timezone.now().date().isoformat())
    return hmac.new(salt, address.encode(), hashlib.sha256).digest()
