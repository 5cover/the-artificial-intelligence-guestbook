from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import MagicLink, RateLimitHit

RETENTION = timedelta(hours=24)


class Command(BaseCommand):
    help = "Delete sign-in links and rate-limit counters older than 24 hours (retention schedule, rows 1 and 19)."

    def handle(self, *args, **options):
        cutoff = timezone.now() - RETENTION
        links, _ = MagicLink.objects.filter(created_at__lt=cutoff).delete()
        hits, _ = RateLimitHit.objects.filter(created_at__lt=cutoff).delete()
        self.stdout.write(
            f"Deleted {links} sign-in links and {hits} rate-limit counters."
        )
