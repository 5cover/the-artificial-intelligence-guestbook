from datetime import timedelta

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from accounts import hashing, limits, magic_links
from accounts.decorators import signed_in_required
from accounts.models import Account, MagicLink
from accounts.session import current_account
from testimonies import revisions, services
from testimonies.emails import send_parental_link
from testimonies.forms import (
    ContributionForm,
    ParentalConfirmForm,
    ParentalEmailForm,
    SubmissionForm,
)
from testimonies.models import Testimony
from testimonies.rendering import render as render_markdown
from testimonies.revisions import SubmissionError
from testimonies.vocabularies import ConsentPath, DeclaredAgeBand

PARENTAL_REQUESTS_PER_ADDRESS = 3


def _initial(testimony):
    if testimony is None:
        return {}
    revision = revisions.current_revision(testimony)
    initial = {"language": testimony.language or ""}
    for name in ContributionForm.base_fields:
        if name not in ("language", "publication_statement"):
            initial[name] = getattr(revision, name) or ""
    initial["languages"] = ", ".join(revision.languages or [])
    initial["tools_used"] = "\n".join(revision.tools_used or [])
    initial["relationship_to_ai"] = revision.relationship_to_ai or []
    return initial


def _is_editable(testimony):
    if testimony.state in (Testimony.State.SUBMITTED, Testimony.State.PUBLISHED):
        return True
    return (
        testimony.state == Testimony.State.QUARANTINED
        and testimony.quarantine_reason == Testimony.QuarantineReason.AWAITING_EDIT
    )


@signed_in_required
def my_testimony(request):
    account = current_account(request)
    testimony = services.testimony_of(account)
    if testimony is None or testimony.state == Testimony.State.DRAFT:
        return _draft(request, account, testimony)
    if _is_editable(testimony):
        return _edit(request, testimony)
    return render(
        request,
        "testimonies/status.html",
        {
            "testimony": testimony,
            "awaiting_parental": services.awaiting_parental_consent(testimony),
        },
    )


def _draft(request, account, testimony):
    preview_html = None
    if request.method == "POST":
        form = ContributionForm(request.POST)
        if form.is_valid():
            services.save_draft(account, form.cleaned_data)
            action = request.POST.get("action")
            if action == "continue":
                return redirect("testimonies:submit")
            if action == "preview":
                preview_html = render_markdown(form.cleaned_data["body"])
            else:
                messages.info(request, _("Draft saved."))
                return redirect("testimonies:my-testimony")
    else:
        form = ContributionForm(initial=_initial(testimony))
    return render(
        request,
        "testimonies/draft.html",
        {"form": form, "preview_html": preview_html},
    )


def _edit(request, testimony):
    preview_html = None
    if request.method == "POST":
        form = ContributionForm(request.POST, edit=True)
        if form.is_valid():
            action = request.POST.get("action")
            if action == "preview":
                preview_html = render_markdown(form.cleaned_data["body"])
            elif action == "send":
                try:
                    revisions.submit_edit(testimony, form.cleaned_data)
                except SubmissionError as error:
                    form.add_error(None, str(error))
                else:
                    messages.info(request, _("Your changes are sent."))
                    return redirect("testimonies:my-testimony")
    else:
        form = ContributionForm(initial=_initial(testimony), edit=True)
    consent = testimony.consent_records.order_by("-publication_consent_at").first()
    return render(
        request,
        "testimonies/edit.html",
        {
            "form": form,
            "testimony": testimony,
            "preview_html": preview_html,
            "under_16": consent.declared_age_band == DeclaredAgeBand.UNDER_16,
            "awaiting_parental": services.awaiting_parental_consent(testimony),
        },
    )


@signed_in_required
def submit_testimony(request):
    account = current_account(request)
    testimony = services.testimony_of(account)
    if testimony is None or testimony.state != Testimony.State.DRAFT:
        return redirect("testimonies:my-testimony")
    if account.status == Account.Status.RESTRICTED:
        messages.error(request, _("Your account cannot submit testimonies."))
        return redirect("testimonies:my-testimony")

    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            try:
                consent = services.submit(
                    testimony, form.cleaned_data["declared_age_band"]
                )
            except SubmissionError as error:
                form.add_error(None, str(error))
            else:
                if consent.consent_path == ConsentPath.PARENTAL:
                    return redirect("testimonies:parental-request")
                messages.info(
                    request, _("Thank you. Your testimony is awaiting review.")
                )
                return redirect("testimonies:my-testimony")
    else:
        form = SubmissionForm()
    return render(request, "testimonies/submit.html", {"form": form})


@signed_in_required
def parental_request(request):
    account = current_account(request)
    testimony = services.testimony_of(account)
    if testimony is None or not services.awaiting_parental_consent(testimony):
        return redirect("testimonies:my-testimony")

    if request.method == "POST":
        form = ParentalEmailForm(request.POST)
        if form.is_valid():
            parent_email = form.cleaned_data["parent_email"]
            allowed = limits.within_limit(
                "parental-link",
                hashing.email_key(parent_email),
                PARENTAL_REQUESTS_PER_ADDRESS,
                timedelta(days=1),
            )
            if allowed:
                token = services.request_parental_link(testimony, parent_email)
                send_parental_link(
                    parent_email,
                    services.public_site_url(
                        reverse("testimonies:parental-confirm", args=[token])
                    ),
                )
            messages.info(
                request,
                _(
                    "If the address can receive email, a link for the parent or guardian is on its way."
                ),
            )
            return redirect("testimonies:my-testimony")
    else:
        form = ParentalEmailForm()
    return render(request, "testimonies/parental_request.html", {"form": form})


def parental_confirm(request, token):
    if request.method == "POST":
        form = ParentalConfirmForm(request.POST)
        if form.is_valid():
            link = magic_links.redeem(MagicLink.Purpose.PARENTAL, token)
            if link is None:
                return render(request, "testimonies/link_invalid.html", status=404)
            services.confirm_parental_consent(link)
            return render(request, "testimonies/parental_done.html")
    else:
        form = ParentalConfirmForm()

    link = magic_links.peek(MagicLink.Purpose.PARENTAL, token)
    if link is None:
        return render(request, "testimonies/link_invalid.html", status=404)
    revision = revisions.current_revision(link.testimony)
    return render(
        request,
        "testimonies/parental_confirm.html",
        {
            "form": form,
            "token": token,
            "body_html": render_markdown(revision.body or ""),
        },
    )
