from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext as _

from reports.models import Notice

OUTCOME_TEXT = {
    Notice.Outcome.NO_ACTION: _("No action was taken on the testimony."),
    Notice.Outcome.RETURNED: _(
        "The testimony was returned to its contributor for changes."
    ),
    Notice.Outcome.REMOVED: _("The testimony was removed."),
    Notice.Outcome.QUARANTINED: _("The testimony is held while it is reviewed."),
    Notice.Outcome.REFERRED: _(
        "The matter was referred to the authorities where the law requires it."
    ),
}


def send_confirmation_link(email, url):
    send_mail(
        subject=_("Confirm your report"),
        message=_(
            "Open this link within 15 minutes to confirm your report. Reports are read only "
            "after they are confirmed. A report does not hide a testimony by itself.\n\n%(url)s"
        )
        % {"url": url},
        from_email=None,
        recipient_list=[email],
    )


def send_acknowledgement(email):
    send_mail(
        subject=_("Your report was received"),
        message=_(
            "Thank you. Your report is in the moderation queue and will be read. "
            "We will write to you with the outcome."
        ),
        from_email=None,
        recipient_list=[email],
    )


def send_outcome(email, outcome):
    send_mail(
        subject=_("The outcome of your report"),
        message=_(
            "%(outcome)s You can ask for a review within 30 days by replying to this email."
        )
        % {"outcome": OUTCOME_TEXT.get(outcome, "")},
        from_email=None,
        recipient_list=[email],
    )


def alert_moderators(message):
    if settings.MODERATOR_EMAILS:
        send_mail(
            subject=_("Guestbook: attention needed"),
            message=message,
            from_email=None,
            recipient_list=sorted(settings.MODERATOR_EMAILS),
        )
