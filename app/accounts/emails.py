from django.core.mail import send_mail
from django.utils.translation import gettext as _


def send_sign_in_link(email, url):
    send_mail(
        subject=_("Your sign-in link"),
        message=_(
            "Open this link to sign in to The Artificial Intelligence Guestbook. "
            "It works once and expires in 15 minutes.\n\n%(url)s\n\n"
            "If you did not ask for it, ignore this message."
        )
        % {"url": url},
        from_email=None,
        recipient_list=[email],
    )
