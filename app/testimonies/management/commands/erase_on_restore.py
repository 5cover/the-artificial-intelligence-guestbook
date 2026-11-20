from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from testimonies import withdrawal


class Command(BaseCommand):
    help = "Run the deletion again for every testimony on the erase-on-restore list (deletion lifecycle, section 6)."

    def handle(self, *args, **options):
        if not settings.ERASE_ON_RESTORE_FILE:
            raise CommandError("GUESTBOOK_ERASE_ON_RESTORE_FILE is not set.")
        path = Path(settings.ERASE_ON_RESTORE_FILE)
        if not path.exists():
            self.stdout.write("The erase-on-restore list is empty.")
            return
        identifiers = [int(line) for line in path.read_text(encoding="utf-8").split()]
        for internal_id in identifiers:
            withdrawal.erase_again(internal_id)
        self.stdout.write(f"Erased again {len(identifiers)} testimonies from the list.")
