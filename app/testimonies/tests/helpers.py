from accounts.session import SESSION_KEY
from testimonies import services
from testimonies.models import Testimony
from testimonies.revisions import current_revision


def sign_in(client, account):
    session = client.session
    session[SESSION_KEY] = account.pk
    session.save()


def submit_testimony(account, body="I wrote this myself.", **values):
    declared_age_band = values.pop("declared_age_band", "16-or-over")
    services.save_draft(
        account,
        {
            "language": "en",
            "body": body,
            "identity_mode": "anonymous",
            "display_name": None,
            "authorship_category": "none",
            **values,
        },
    )
    testimony = Testimony.objects.get(account=account)
    services.submit(testimony, declared_age_band)
    return Testimony.objects.get(pk=testimony.pk)


def latest_body(testimony):
    return current_revision(testimony).body
