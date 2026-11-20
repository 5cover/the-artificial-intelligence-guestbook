from django.core.mail import send_mail
from django.utils.translation import gettext as _

from moderation.rules import PublishingRule


def send_statement(email, rule, guidance=None):
    # Statement of reasons (DSA art. 17): the decision, its ground and the way to ask for a review.
    label = PublishingRule(rule).label if rule else _("Not applicable")
    lines = [
        _("We have decided on your testimony under this publishing rule: %(rule)s.")
        % {"rule": label},
    ]
    if guidance:
        lines.append(_("What to change: %(guidance)s") % {"guidance": guidance})
    lines.append(
        _(
            "Most changes are about accidents made in good faith. You can ask for a review "
            "within 30 days by replying to this email."
        )
    )
    send_mail(
        subject=_("About your testimony"),
        message="\n\n".join(lines),
        from_email=None,
        recipient_list=[email],
    )
