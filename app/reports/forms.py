from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from accounts import proof_of_work
from reports.models import Notice


class ReportForm(forms.Form):
    reason = forms.ChoiceField(
        choices=Notice.Reason.choices,
        widget=forms.RadioSelect,
        label=_("Why are you reporting this testimony?"),
    )
    passage = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea,
        label=_("The exact passage, if relevant"),
    )
    grounds = forms.CharField(
        max_length=5000,
        widget=forms.Textarea,
        label=_("Explain what is wrong"),
    )
    good_faith = forms.BooleanField(
        required=True,
        label=_("I make this report in good faith."),
        help_text=_("A knowingly false report is an offence."),
    )
    email = forms.EmailField(
        max_length=254,
        required=False,
        label=_("Your email address"),
        help_text=_(
            "We send a link to confirm the report, and write to you with the outcome. "
            "Not required for reports of child sexual abuse material."
        ),
    )
    pow_challenge = forms.CharField(required=False, widget=forms.HiddenInput)
    pow_nonce = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, expected_challenge=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_challenge = expected_challenge

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("reason") != Notice.Reason.CSAM and not cleaned.get("email"):
            self.add_error(
                "email", _("Give an email address so that we can confirm the report.")
            )
        nonce = cleaned.get("pow_nonce")
        if nonce and not proof_of_work.verify(
            self.expected_challenge, cleaned.get("pow_challenge"), nonce
        ):
            raise ValidationError(_("The browser check did not verify. Try again."))
        if not nonce:
            self.proof_verified = False
        else:
            self.proof_verified = True
        return cleaned
