from functools import wraps

from django.conf import settings
from django.contrib import messages
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
from testimonies.models import Testimony
from testimonies.revisions import current_revision, pending_revisions
from testimonies.services import awaiting_parental_consent

DECISIONS = {
    "approve",
    "return",
    "return-and-quarantine",
    "quarantine",
    "restrict-account",
}


def moderator_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        account = current_account(request)
        if account is None or account.email not in settings.MODERATOR_EMAILS:
            raise Http404
        return view(request, *args, **kwargs)

    return wrapper


@moderator_required
def queue(request):
    testimonies = (
        Testimony.objects.filter(revisions__review_state="pending")
        .distinct()
        .order_by("edition_period", "received_at", "pk")
    )
    items = [
        {
            "testimony": testimony,
            "token": review_token(testimony),
            "waiting_for_parent": awaiting_parental_consent(testimony),
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
