from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.urls import reverse

from publication import data, identifiers
from publication.records import public_record
from testimonies.models import Testimony

CORS = {"Access-Control-Allow-Origin": "*"}


def _json(document, status=200):
    response = HttpResponse(
        data.dumps(document),
        content_type="application/json; charset=utf-8",
        status=status,
    )
    for name, value in CORS.items():
        response[name] = value
    return response


def _testimony_or_response(public_id):
    canonical = identifiers.normalize(public_id)
    if canonical is None:
        raise Http404
    testimony = (
        Testimony.objects.select_related("public_revision")
        .filter(public_id=canonical)
        .first()
    )
    return canonical, testimony


def testimony_json(request, public_id):
    canonical, testimony = _testimony_or_response(public_id)
    if canonical != public_id:
        return HttpResponsePermanentRedirect(
            reverse("publication:data-testimony", args=[canonical])
        )
    if testimony is None:
        raise Http404
    if testimony.state == Testimony.State.WITHDRAWN:
        return _json({"public_id": canonical, "status": "withdrawn"}, status=410)
    if testimony.state != Testimony.State.PUBLISHED:
        raise Http404
    return _json(public_record(testimony))


def testimony_markdown(request, public_id):
    canonical, testimony = _testimony_or_response(public_id)
    if canonical != public_id:
        return HttpResponsePermanentRedirect(
            reverse("publication:testimony-markdown", args=[canonical])
        )
    if testimony is None or testimony.state != Testimony.State.PUBLISHED:
        raise Http404
    response = HttpResponse(
        public_record(testimony)["body"] + "\n",
        content_type="text/markdown; charset=utf-8",
    )
    return response


def index(request):
    return _json(data.index_document())


def withdrawals(request):
    return _json(data.withdrawals_document())


def registry(request):
    return _json(data.registry_document())


def schema(request, version, name):
    if version != 0 or name not in data.SCHEMA_NAMES:
        raise Http404
    response = HttpResponse(
        data.schema_text(name), content_type="application/schema+json; charset=utf-8"
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def llms(request):
    return HttpResponse(data.llms_text(), content_type="text/plain; charset=utf-8")


def robots(request):
    return HttpResponse(data.robots_text(), content_type="text/plain; charset=utf-8")
