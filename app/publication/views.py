from datetime import timedelta

from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from accounts import hashing, limits
from publication import browse, citation, identifiers, presentation
from publication.records import public_record
from testimonies.models import Testimony
from testimonies.rendering import plain_text
from testimonies.rendering import render as render_markdown

PAGE_SIZE = 50
EXCERPT_LENGTH = 280
SEARCHES_PER_HOUR = 60
PLACEHOLDERS = {
    "context": _("Context"),
    "references": _("Reference shelf"),
    "methodology": _("Methodology"),
    "publishing-rules": _("Publishing rules"),
    "privacy": _("Privacy notice"),
    "terms": _("Terms"),
}


def _item(record):
    text = plain_text(record["body"])
    excerpt = (
        text
        if len(text) <= EXCERPT_LENGTH
        else text[:EXCERPT_LENGTH].rsplit(" ", 1)[0] + "..."
    )
    return {
        "record": record,
        "excerpt": excerpt,
        "attribution": citation.attribution(record),
    }


def _query_string(params):
    copy = params.copy()
    copy.pop("page", None)
    return copy.urlencode()


def home(request):
    return render(request, "publication/home.html")


def listing(request):
    params = request.GET
    query = params.get("q", "").strip()
    selected = browse.selected_filters(params)
    queryset = browse.published()
    if query:
        address = request.META.get("REMOTE_ADDR", "")
        if not limits.within_limit(
            "search",
            hashing.address_key(address),
            SEARCHES_PER_HOUR,
            timedelta(hours=1),
        ):
            return render(
                request, "publication/listing.html", {"too_many": True}, status=429
            )
        queryset = browse.search(queryset, query)
    queryset = browse.apply_filters(queryset, selected)
    page = Paginator(browse.ordered(queryset), PAGE_SIZE).get_page(params.get("page"))
    context = {
        "page": page,
        "items": [_item(public_record(testimony)) for testimony in page.object_list],
        "query": query,
        "selected": selected,
        "options": browse.filter_options(selected),
        "query_string": _query_string(params),
        "noindex": bool(query or selected),
    }
    return render(request, "publication/listing.html", context)


def testimony(request, public_id):
    canonical = identifiers.normalize(public_id)
    if canonical is None:
        raise Http404
    if canonical != public_id:
        return redirect(
            reverse("publication:testimony", args=[canonical]), permanent=True
        )

    found = (
        Testimony.objects.select_related("public_revision")
        .filter(public_id=canonical)
        .first()
    )
    if found is None:
        raise Http404
    if found.state == Testimony.State.WITHDRAWN:
        return render(
            request,
            "publication/tombstone.html",
            {"public_id": canonical},
            status=410,
        )
    if found.state != Testimony.State.PUBLISHED:
        raise Http404

    record = public_record(found)
    context = {
        "record": record,
        "body_html": render_markdown(record["body"], heading_base=1),
        "attribution": citation.attribution(record),
        "identity_rows": presentation.rows(
            record["identity"], presentation.IDENTITY_ROWS
        ),
        "authorship_rows": presentation.rows(
            record["authorship"], presentation.AUTHORSHIP_ROWS
        ),
        "structured_rows": presentation.rows(
            record.get("structured", {}), presentation.STRUCTURED_ROWS
        ),
        "citations": {
            "plain": record["citation"],
            "bibtex": citation.bibtex(record),
            "hayagriva": citation.hayagriva(record),
        },
    }
    return render(request, "publication/testimony.html", context)


def placeholder(request, page):
    if page not in PLACEHOLDERS:
        raise Http404
    return render(
        request, "publication/placeholder.html", {"title": PLACEHOLDERS[page]}
    )
