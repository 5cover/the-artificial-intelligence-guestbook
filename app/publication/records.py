from django.conf import settings

from publication import citation

# The allow-list of public fields (data model, section 1.1, rule 1). Pages,
# data URLs and editions are built from these tuples and nothing else.
IDENTITY_FIELDS = (
    "display_name",
    "age_range",
    "country",
    "region",
    "languages",
    "profession",
    "field",
    "field_note",
    "organization",
    "organization_type",
    "organization_type_note",
    "relationship_to_ai",
    "relationship_to_ai_note",
    "link",
)
AUTHORSHIP_FIELDS = (
    "provider",
    "product",
    "model",
    "model_version",
    "mode_or_setting",
    "inputs",
    "workflow",
    "changes_after",
    "comment",
)
STRUCTURED_FIELDS = (
    "ai_use_frequency",
    "tools_used",
    "attitude",
    "attitude_note",
    "prediction",
    "prediction_horizon",
)


def _present(value):
    return value is not None and value != "" and value != []


def public_record(testimony):
    revision = testimony.public_revision
    identity = {"mode": revision.identity_mode}
    identity.update(
        {
            name: getattr(revision, name)
            for name in IDENTITY_FIELDS
            if _present(getattr(revision, name))
        }
    )
    authorship = {"category": revision.authorship_category}
    authorship.update(
        {
            name: getattr(revision, name)
            for name in AUTHORSHIP_FIELDS
            if _present(getattr(revision, name))
        }
    )
    structured = {
        name: getattr(revision, name)
        for name in STRUCTURED_FIELDS
        if _present(getattr(revision, name))
    }
    timeline = [
        _timeline_entry(entry)
        for entry in testimony.revisions.filter(revision_number__isnull=False)
        .exclude(review_state="returned")
        .order_by("revision_number")
    ]
    record = {
        "format_version": 0,
        "public_id": testimony.public_id,
        "url": f"{settings.PUBLIC_BASE_URL.rstrip('/')}/testimonies/{testimony.public_id}",
        "language": testimony.language,
        "published_on": testimony.published_at.date().isoformat(),
        "edition_period": testimony.edition_period,
        "licence": testimony.licence,
        "body_format": "commonmark-0.31.2",
        "body": revision.body,
        "revisions": timeline,
        "identity": identity,
        "authorship": authorship,
    }
    if structured:
        record["structured"] = structured
    record["citation"] = citation.plain(record)
    return record


def _timeline_entry(revision):
    entry = {
        "revision_number": revision.revision_number,
        "live_on": revision.live_at.date().isoformat(),
    }
    if revision.summary:
        entry["summary"] = revision.summary
    return entry
