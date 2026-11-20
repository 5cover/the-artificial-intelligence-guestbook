from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from accounts.session import current_account
from moderation import services
from moderation.diffs import word_diff
from moderation.forms import DecisionForm
from moderation.keys import review_token, testimony_for
from reports.models import Notice
from reports.services import PRIORITY_RANK, open_notices
from testimonies.models import Testimony
from testimonies.revisions import current_revision, pending_revisions
from testimonies.services import awaiting_parental_consent

DECISIONS = {
    "approve",
    "return",
    "return-and-quarantine",
    "quarantine",
    "restrict-account",
    "remove",
    "dismiss-reports",
}
NO_PRIORITY = len(PRIORITY_RANK)


def moderator_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        account = current_account(request)
        if account is None or account.email not in settings.MODERATOR_EMAILS:
            raise Http404
        return view(request, *args, **kwargs)

    return wrapper


def _priority_rank(testimony):
    ranks = [
        PRIORITY_RANK[notice.priority]
        for notice in open_notices(testimony.public_id or "")
    ]
    return min(ranks, default=NO_PRIORITY)


@moderator_required
def queue(request):
    reported = Notice.objects.filter(
        confirmed_at__isnull=False, outcome__isnull=True
    ).values("testimony_public_id")
    testimonies = list(
        Testimony.objects.filter(
            Q(revisions__review_state="pending") | Q(public_id__in=reported)
        )
        .distinct()
        .order_by("edition_period", "received_at", "pk")
    )
    # Urgent reports first, then the earliest edition period (data model, section 5; reports, section 3).
    testimonies.sort(
        key=lambda testimony: (_priority_rank(testimony), testimony.edition_period or 0)
    )
    items = [
        {
            "testimony": testimony,
            "token": review_token(testimony),
            "waiting_for_parent": awaiting_parental_consent(testimony),
            "reports": open_notices(testimony.public_id or "").count(),
        }
        for testimony in testimonies
    ]
    return render(request, "moderation/queue.html", {"items": items})


@moderator_required
def review(request, token):
    testimony = testimony_for(token)
    if testimony is None:
        raise Http404
    revisions = list(testimony.revisions.order_by("sequence"))
    pending = list(pending_revisions(testimony))
    baseline = testimony.archived_revision
    changes = ""
    if pending:
        changes = word_diff(baseline.body if baseline else "", pending[-1].body)
    steps = [
        {
            "earlier": earlier.sequence,
            "later": later.sequence,
            "diff": word_diff(earlier.body, later.body),
        }
        for earlier, later in zip(revisions, revisions[1:], strict=False)
    ]
    context = {
        "testimony": testimony,
        "token": token,
        "current": current_revision(testimony),
        "revisions": revisions,
        "pending": pending,
        "changes": changes,
        "steps": steps,
        "reports": open_notices(testimony.public_id or "")
        if testimony.public_id
        else [],
        "waiting_for_parent": awaiting_parental_consent(testimony),
        "form": DecisionForm(action="approve"),
    }
    return render(request, "moderation/review.html", context)


@moderator_required
@require_POST
def decide(request, token):
    testimony = testimony_for(token)
    if testimony is None:
        raise Http404
    action = request.POST.get("action", "")
    if action not in DECISIONS:
        raise Http404

    form = DecisionForm(request.POST, action=action)
    if not form.is_valid():
        messages.error(
            request, _("The decision needs the fields its outcome requires.")
        )
        return redirect("moderation:review", token=token)

    data = form.cleaned_data
    moderator = current_account(request).email
    try:
        if action == "approve":
            services.approve(testimony, moderator)
        elif action in {"return", "return-and-quarantine"}:
            services.return_revisions(
                testimony,
                moderator,
                rule=data["rule"],
                guidance=data["guidance"],
                quarantine=action == "return-and-quarantine",
            )
        elif action == "quarantine":
            services.quarantine_for_legal_hold(testimony, moderator, note=data["note"])
        elif action == "remove":
            services.remove_testimony(
                testimony,
                moderator,
                rule=data["rule"],
                guidance=data["guidance"],
            )
        elif action == "dismiss-reports":
            services.dismiss_reports(testimony, moderator)
        else:
            services.restrict_account(
                testimony,
                moderator,
                rule=data["rule"],
                guidance=data["guidance"],
            )
    except services.ReviewError as error:
        messages.error(request, str(error))
        return redirect(reverse("moderation:review", args=[token]))
    messages.info(request, _("Decision recorded."))
    return redirect("moderation:queue")
