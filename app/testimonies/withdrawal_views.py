from datetime import timedelta

from django import forms
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from accounts import hashing, limits, magic_links
from accounts.decorators import signed_in_required
from accounts.models import MagicLink
from accounts.session import current_account, sign_out
from publication import identifiers
from testimonies import withdrawal
from testimonies.emails import send_action_link
from testimonies.models import Testimony
from testimonies.vocabularies import WithdrawableField, WithdrawalScope

DAY = timedelta(days=1)
REQUESTS_PER_DAY = 5


class WithdrawForm(forms.Form):
    scope = forms.ChoiceField(
        choices=[
            (WithdrawalScope.TESTIMONY, gettext_lazy("Withdraw the whole testimony")),
            (WithdrawalScope.FIELD, gettext_lazy("Withdraw one detail about me")),
        ],
        widget=forms.RadioSelect,
        label=gettext_lazy("What to withdraw"),
    )
    field_name = forms.ChoiceField(
        choices=[("", gettext_lazy("Choose a detail")), *WithdrawableField.choices],
        required=False,
        label=gettext_lazy("Detail"),
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("scope") == WithdrawalScope.FIELD and not cleaned.get(
            "field_name"
        ):
            self.add_error("field_name", _("Choose the detail to withdraw."))
        return cleaned


class PublicWithdrawForm(forms.Form):
    public_id = forms.CharField(
        max_length=20, label=gettext_lazy("Testimony identifier")
    )
    code = forms.CharField(
        max_length=40,
        required=False,
        label=gettext_lazy("Withdrawal code"),
        help_text=gettext_lazy("Given when your account was closed."),
    )
    email = forms.EmailField(
        max_length=254,
        required=False,
        label=gettext_lazy("Email address used for the testimony"),
        help_text=gettext_lazy("We send a link to this address only if it matches."),
    )

    def clean(self):
        cleaned = super().clean()
        if bool(cleaned.get("code")) == bool(cleaned.get("email")):
            raise forms.ValidationError(
                _("Give either the withdrawal code or the email address.")
            )
        return cleaned


class ClosureForm(forms.Form):
    choice = forms.ChoiceField(
        choices=[
            ("withdraw", gettext_lazy("Withdraw my testimony and close my account")),
            (
                "keep",
                gettext_lazy(
                    "Keep my testimony published without an account and close my account"
                ),
            ),
        ],
        widget=forms.RadioSelect,
        label=gettext_lazy("What should happen?"),
        help_text=gettext_lazy("Choose one. Neither option is selected for you."),
    )


def _link(path):
    return settings.PUBLIC_BASE_URL.rstrip("/") + path


@signed_in_required
def account_withdraw(request):
    account = current_account(request)
    testimony = account.testimonies.filter(state=Testimony.State.PUBLISHED).first()
    if testimony is None:
        messages.info(request, _("You have no published testimony to withdraw."))
        return redirect("accounts:account")

    if request.method == "POST":
        form = WithdrawForm(request.POST)
        if form.is_valid():
            if limits.within_limit(
                "withdrawal-request",
                hashing.email_key(account.email),
                REQUESTS_PER_DAY,
                DAY,
            ):
                scope = form.cleaned_data["scope"]
                field_name = form.cleaned_data["field_name"] or None
                _request, token = withdrawal.start_by_account(
                    account, testimony, scope, field_name
                )
                send_action_link(
                    account.email,
                    _link(reverse("testimonies:withdraw-confirm", args=[token])),
                    _("Confirm the withdrawal"),
                )
            messages.info(
                request,
                _(
                    "If the request can be sent, a confirmation link is on its way by email."
                ),
            )
            return redirect("accounts:account")
    else:
        form = WithdrawForm(initial={"scope": WithdrawalScope.TESTIMONY})
    return render(request, "testimonies/withdraw_request.html", {"form": form})


def withdraw_confirm(request, token):
    if magic_links.peek(MagicLink.Purpose.WITHDRAWAL, token) is None:
        return render(request, "testimonies/link_invalid.html", status=404)
    if request.method == "POST":
        request_done = withdrawal.confirm_link(token)
        if request_done is None:
            return render(request, "testimonies/link_invalid.html", status=404)
        return render(
            request,
            "testimonies/withdraw_done.html",
            {"steps": _describe(request_done)},
        )
    return render(request, "testimonies/withdraw_confirm.html", {"token": token})


def public_withdraw(request):
    if request.method == "POST":
        form = PublicWithdrawForm(request.POST)
        if form.is_valid():
            public_id = identifiers.normalize(form.cleaned_data["public_id"])
            code = form.cleaned_data["code"]
            if code:
                normalized = withdrawal.normalize_code(code)
                done = (
                    withdrawal.withdraw_with_code(public_id, normalized)
                    if public_id and normalized
                    else None
                )
                if done is None:
                    form.add_error(
                        None, _("These details do not match a published testimony.")
                    )
                else:
                    return render(
                        request,
                        "testimonies/withdraw_done.html",
                        {"steps": _describe(done)},
                    )
            elif public_id and limits.within_limit(
                "withdrawal-by-email",
                hashing.email_key(form.cleaned_data["email"]),
                REQUESTS_PER_DAY,
                DAY,
            ):
                token = withdrawal.start_by_former_email(
                    public_id, form.cleaned_data["email"]
                )
                if token is not None:
                    send_action_link(
                        form.cleaned_data["email"],
                        _link(reverse("testimonies:withdraw-confirm", args=[token])),
                        _("Confirm the withdrawal"),
                    )
                return render(request, "testimonies/withdraw_sent.html")
            else:
                return render(request, "testimonies/withdraw_sent.html")
    else:
        form = PublicWithdrawForm()
    return render(request, "testimonies/withdraw_public.html", {"form": form})


@signed_in_required
def account_close(request):
    account = current_account(request)
    testimony = account.testimonies.filter(state=Testimony.State.PUBLISHED).first()
    if request.method == "POST":
        form = ClosureForm(request.POST)
        if form.is_valid():
            keep = form.cleaned_data["choice"] == "keep"
            pending = account.testimonies.exclude(
                state=Testimony.State.PUBLISHED
            ).exists()
            if keep and pending:
                form.add_error(
                    None, _("Only a published testimony can stay without an account.")
                )
            else:
                withdraw_testimony = not keep and testimony is not None
                token = withdrawal.start_closure(
                    account, keep_testimony=not withdraw_testimony
                )
                name = "withdraw-confirm" if withdraw_testimony else "close-confirm"
                send_action_link(
                    account.email,
                    _link(reverse(f"testimonies:{name}", args=[token])),
                    _("Confirm the closure of your account"),
                )
                return render(request, "testimonies/close_sent.html")
    else:
        form = ClosureForm()
    return render(
        request,
        "testimonies/close_account.html",
        {"form": form, "testimony": testimony},
    )


def closure_confirm(request, token):
    if magic_links.peek(MagicLink.Purpose.CLOSURE, token) is None:
        return render(request, "testimonies/link_invalid.html", status=404)
    if request.method == "POST":
        code = withdrawal.confirm_closure(token)
        if code is None:
            return render(request, "testimonies/link_invalid.html", status=404)
        sign_out(request)
        return render(request, "testimonies/closure_done.html", {"code": code})
    return render(request, "testimonies/closure_confirm.html", {"token": token})


MANUAL_TEXT = {
    "manual:search-engines": gettext_lazy(
        "Copies cached by search engines may remain until they update. Removal requests can be sent to them."
    ),
    "manual:web-archives": gettext_lazy(
        "Captures held by web archives may remain. Exclusion can be requested where the archive offers it."
    ),
    "manual:mirrors": gettext_lazy(
        "Copies kept by others, such as mirrors and downloads, cannot be recalled."
    ),
    "manual:vacuum-due": gettext_lazy(
        "Deleted data is physically removed from the database storage by the scheduled maintenance."
    ),
}


def _describe(request_done):
    return [MANUAL_TEXT[step] for step in request_done.steps if step in MANUAL_TEXT]
