from django.utils import timezone

from accounts.models import RateLimitHit


def within_limit(scope, key, limit, window):
    now = timezone.now()
    recent = RateLimitHit.objects.filter(
        scope=scope, key=key, created_at__gt=now - window
    ).count()
    if recent >= limit:
        return False
    RateLimitHit.objects.create(scope=scope, key=key, created_at=now)
    return True
