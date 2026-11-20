from datetime import timedelta

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

from accounts import hashing, limits, magic_links, proof_of_work
from accounts.models import MagicLink
from reports import services
from reports.emails import send_confirmation_link
from reports.forms import ReportForm
from reports.models import Notice
from testimonies.models import Testimony

DAY = timedelta(days=1)
REPORTS_PER_EMAIL = 3
REPORTS_PER_NETWORK = 10
REPORTS_PER_NETWORK_WITHOUT_PROOF = 3


def report_form(request, public_id):
    testimony = Testimony.objects.filter(
        public_id=public_id, state=Testimony.State.PUBLISHED
    ).first()
    if testimony is None:
        raise Http404
    if request.method == "POST":
        expected = proof_of_work.take_challenge(request)
        form = ReportForm(request.POST, expected_challenge=expected)
        if form.is_valid():
            return _file_report(request, form, testimony)
    else:
        challenge = proof_of_work.issue_challenge(request)
        form = ReportForm(initial={"pow_challenge": challenge})
    return render(
        request,
        "reports/report_form.html",
        {"form": form, "testimony": testimony, "pow_difficulty": 16},
    )


def _file_report(request, form, testimony):
    data = form.cleaned_data
    email = data.get("email") or ""
    reason = data["reason"]
    if email and services.already_reported(testimony.public_id, email):
        return render(request, "reports/report_sent.html", {"repeated": True})
    if reason != Notice.Reason.CSAM:
        network = request.META.get("REMOTE_ADDR", "")
        network_limit = (
            REPORTS_PER_NETWORK
            if form.proof_verified
            else REPORTS_PER_NETWORK_WITHOUT_PROOF
        )
        allowed = limits.within_limit(
            "report-email", hashing.email_key(email), REPORTS_PER_EMAIL, DAY
        ) and limits.within_limit(
            "report-network", hashing.address_key(network), network_limit, DAY
        )
        if not allowed:
            form.add_error(None, _("Too many reports. Try again later."))
            return render(
                request,
                "reports/report_form.html",
                {"form": form, "testimony": testimony, "pow_difficulty": 16},
            )

    grounds = data["grounds"]
    if data.get("passage"):
        grounds = f"{grounds}\n\nPassage: {data['passage']}"
    notice = services.create_notice(testimony.public_id, reason, grounds, email)
    if reason == Notice.Reason.CSAM:
        services.confirm(notice)
    else:
        token = magic_links.issue(MagicLink.Purpose.REPORT, email, notice=notice)
        send_confirmation_link(
            email,
            _base(reverse("reports:confirm", args=[token])),
        )
    return render(request, "reports/report_sent.html", {"repeated": False})


def _base(path):
    return settings.PUBLIC_BASE_URL.rstrip("/") + path


def confirm_report(request, token):
    if magic_links.peek(MagicLink.Purpose.REPORT, token) is None:
        return render(request, "testimonies/link_invalid.html", status=404)
    if request.method == "POST":
        link = magic_links.redeem(MagicLink.Purpose.REPORT, token)
        if link is None or link.notice is None:
            return render(request, "testimonies/link_invalid.html", status=404)
        if link.notice.confirmed_at is None:
            services.confirm(link.notice)
        return render(request, "reports/report_done.html")
    return render(request, "reports/report_confirm.html", {"token": token})
