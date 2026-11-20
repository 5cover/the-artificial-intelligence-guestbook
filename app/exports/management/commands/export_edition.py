from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from exports.edition import EditionError, build


class Command(BaseCommand):
    help = "Write an unsigned edition bag of public data (archive format, sections 1 to 5, 7 to 9)."

    def add_arguments(self, parser):
        parser.add_argument("edition_id", help="for example 2027.0 or 2026-rehearsal.1")
        parser.add_argument(
            "output", help="an existing directory; the bag is written inside it"
        )

    def handle(self, *args, **options):
        output = Path(options["output"])
        if not output.is_dir():
            raise CommandError(f"{output} is not a directory.")
        try:
            bag, testimonies, withdrawals = build(options["edition_id"], output)
        except EditionError as error:
            raise CommandError(str(error)) from error
        self.stdout.write(
            f"Wrote {bag}: {testimonies} testimonies, {withdrawals} withdrawals. Not signed yet."
        )
