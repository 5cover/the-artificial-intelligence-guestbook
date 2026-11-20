import os

os.environ.setdefault(
    "GUESTBOOK_SECRET_KEY", "tests-only-secret-key-not-used-anywhere-else"
)

from guestbook.settings import *  # noqa: E402, F403
