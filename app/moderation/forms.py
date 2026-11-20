from django import forms
from django.utils.translation import gettext_lazy as _

from moderation.rules import PublishingRule

RULE_REQUIRED = {"return", "return-and-quarantine", "restrict-account", "remove"}
GUIDANCE_REQUIRED = {"return", "return-and-quarantine"}


class DecisionForm(forms.Form):
    rule = forms.ChoiceField(
        choices=[("", _("Choose a rule")), *PublishingRule.choices],
        required=False,
        label=_("Publishing rule"),
    )
    guidance = forms.CharField(
        max_length=2000,
        required=False,
        widget=forms.Textarea,
        label=_("What the contributor should change"),
    )
    note = forms.CharField(
        max_length=5000,
        required=False,
        widget=forms.Textarea,
        label=_("Private note for the moderation record"),
    )

    def __init__(self, *args, action, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = action

    def clean(self):
        cleaned = super().clean()
        if self.action in RULE_REQUIRED and not cleaned.get("rule"):
            self.add_error("rule", _("Choose the publishing rule that applies."))
        if self.action in GUIDANCE_REQUIRED and not cleaned.get("guidance"):
            self.add_error("guidance", _("Say what the contributor should change."))
        return cleaned
