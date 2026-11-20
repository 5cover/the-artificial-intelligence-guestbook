from django.core import signing

from testimonies.models import Testimony

SALT = "guestbook.moderation.review"


def review_token(testimony):
    # Private views address a testimony by a signed token, so that neither its
    # internal ID nor its public ID appears in a URL (identifiers, section 1).
    return signing.dumps(testimony.pk, salt=SALT)


def testimony_for(token):
    try:
        pk = signing.loads(token, salt=SALT)
    except signing.BadSignature:
        return None
    return Testimony.objects.filter(pk=pk).first()
