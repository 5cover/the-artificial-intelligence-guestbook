import hmac

from accounts import hashing
from testimonies.models import Testimony


def review_token(testimony):
    # A keyed digest of the internal ID, so that neither the internal ID nor its
    # encoding appears in a URL (identifiers, section 1). Lookup scans the
    # testimonies, which is adequate for the scale of the MVP.
    return hashing.keyed("review-token", str(testimony.pk)).hex()[:32]


def testimony_for(token):
    for testimony in Testimony.objects.only("pk"):
        if hmac.compare_digest(review_token(testimony), token):
            return Testimony.objects.get(pk=testimony.pk)
    return None
