from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from accounts import mail_domains, proof_of_work


class SignInForm(forms.Form):
    email = forms.EmailField(max_length=254, label=_("Email address"))
    pow_challenge = forms.CharField(required=False, widget=forms.HiddenInput)
    pow_nonce = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, expected_challenge=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_challenge = expected_challenge
        self.proof_verified = False

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        domain = email.rpartition("@")[2]
        if mail_domains.is_disposable(domain):
            raise ValidationError(
                gettext(
                    "Use a permanent email address. Disposable addresses are not accepted."
                )
            )
        if not mail_domains.accepts_mail(domain):
            raise ValidationError(gettext("This domain does not accept email."))
        return email

    def clean(self):
        cleaned = super().clean()
        nonce = cleaned.get("pow_nonce")
        if nonce:
            self.proof_verified = proof_of_work.verify(
                self.expected_challenge, cleaned.get("pow_challenge"), nonce
            )
            if not self.proof_verified:
                raise ValidationError(
                    gettext("The browser check did not verify. Try again.")
                )
        return cleaned
