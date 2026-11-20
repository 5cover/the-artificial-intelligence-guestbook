from django.core.mail import send_mail
from django.utils.translation import gettext as _


def send_parental_link(email, url):
    send_mail(
        subject=_("Confirm consent for a testimony"),
        message=_(
            "A young person has asked to publish a testimony in The Artificial Intelligence "
            "Guestbook and named you as their parent or legal guardian. Nothing is published "
            "unless you confirm. Open this link to read the testimony and to confirm, within "
            "15 minutes:\n\n%(url)s\n\nIf you do not recognize this request, ignore this message."
        )
        % {"url": url},
        from_email=None,
        recipient_list=[email],
    )


def send_withdrawal_confirmation(email):
    send_mail(
        subject=_("Your testimony was withdrawn"),
        message=_(
            "The testimony you asked us to withdraw has been removed from everything the "
            "project controls. Copies that others made, such as downloads, mirrors, search "
            "engines and web archives, may remain: the project cannot recall them."
        ),
        from_email=None,
        recipient_list=[email],
    )


def send_action_link(email, url, subject):
    send_mail(
        subject=subject,
        message=_(
            "Open this link within 15 minutes to confirm. It works once.\n\n%(url)s\n\n"
            "If you did not ask for this, ignore this message."
        )
        % {"url": url},
        from_email=None,
        recipient_list=[email],
    )
