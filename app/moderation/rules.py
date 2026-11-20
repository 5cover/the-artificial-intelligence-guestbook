from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class PublishingRule(TextChoices):
    # Codes of the publishing rules (docs/legal/publishing-rules.md). Each code
    # is stored with the decision it justifies.
    ILLEGAL = "illegal", _("Illegal content")
    DEFAMATION = "defamation", _("Defamation of an identifiable person")
    THREAT = "threat", _("Threat")
    HARASSMENT = "harassment", _("Harassment")
    THIRD_PARTY_PRIVACY = (
        "third-party-privacy",
        _("Private information about another person"),
    )
    SECRETS = "secrets", _("Passwords, keys or other secrets")
    SPAM = "spam", _("Spam or repeated submission")
    ADVERTISING = "advertising", _("Advertising or links for search engines")
    NOT_TESTIMONY = "not-testimony", _("Not a testimony")
    IMPERSONATION = "impersonation", _("Impersonation")
    FALSE_DISCLOSURE = "false-disclosure", _("False answer about AI use")
