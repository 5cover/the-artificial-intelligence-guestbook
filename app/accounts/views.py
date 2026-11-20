from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from accounts import hashing, limits, magic_links, proof_of_work
from accounts.emails import send_sign_in_link
from accounts.forms import SignInForm
from accounts.models import Account, MagicLink
from accounts.session import current_account, sign_in, sign_out

HOUR = timedelta(hours=1)
SIGN_IN_PER_ADDRESS = 5
SIGN_IN_PER_NETWORK_WITH_PROOF = 20
SIGN_IN_PER_NETWORK_WITHOUT_PROOF = 3


def _render_sign_in(request, form):
    challenge = proof_of_work.issue_challenge(request)
    form.data = form.data.copy()
    form.data["pow_challenge"] = challenge
    form.data["pow_nonce"] = ""
    return render(
        request,
        "accounts/sign_in.html",
        {"form": form, "pow_difficulty": settings.POW_DIFFICULTY_BITS},
    )


def sign_in_request(request):
    if request.method == "POST":
        expected = proof_of_work.take_challenge(request)
        form = SignInForm(request.POST, expected_challenge=expected)
        if not form.is_valid():
            return _render_sign_in(request, form)
        email = form.cleaned_data["email"]
        network_limit = (
            SIGN_IN_PER_NETWORK_WITH_PROOF
            if form.proof_verified
            else SIGN_IN_PER_NETWORK_WITHOUT_PROOF
        )
        allowed = limits.within_limit(
            "sign-in-email", hashing.email_key(email), SIGN_IN_PER_ADDRESS, HOUR
        ) and limits.within_limit(
            "sign-in-network",
            hashing.address_key(request.META.get("REMOTE_ADDR", "")),
            network_limit,
            HOUR,
        )
        if not allowed:
            form.add_error(None, _("Too many sign-in requests. Try again later."))
            return _render_sign_in(request, form)
        token = magic_links.issue(MagicLink.Purpose.SIGN_IN, email)
        send_sign_in_link(
            email,
            settings.PUBLIC_BASE_URL + reverse("accounts:sign-in-link", args=[token]),
        )
        return redirect("accounts:sign-in-sent")

    challenge = proof_of_work.issue_challenge(request)
    form = SignInForm(initial={"pow_challenge": challenge})
    return render(
        request,
        "accounts/sign_in.html",
        {"form": form, "pow_difficulty": settings.POW_DIFFICULTY_BITS},
    )


def sign_in_link(request, token):
    if request.method == "POST":
        link = magic_links.redeem(MagicLink.Purpose.SIGN_IN, token)
        if link is None:
            return render(request, "accounts/sign_in_link_invalid.html", status=404)
        now = timezone.now()
        account, _created = Account.objects.get_or_create(
            email=link.email, defaults={"created_at": now}
        )
        if account.status == Account.Status.CLOSED:
            return render(request, "accounts/sign_in_closed.html", status=403)
        account.email_verified_at = account.email_verified_at or now
        account.last_sign_in_at = now
        account.save(update_fields=["email_verified_at", "last_sign_in_at"])
        sign_in(request, account)
        return redirect("accounts:account")

    if magic_links.peek(MagicLink.Purpose.SIGN_IN, token) is None:
        return render(request, "accounts/sign_in_link_invalid.html", status=404)
    return render(request, "accounts/sign_in_link.html", {"token": token})


@require_POST
def sign_out_request(request):
    sign_out(request)
    messages.info(request, _("You are signed out."))
    return redirect("accounts:sign-in")


def account_home(request):
    account = current_account(request)
    if account is None:
        return redirect("accounts:sign-in")
    return render(request, "accounts/account.html")
