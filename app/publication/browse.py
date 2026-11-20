from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q
from django.db.models.functions import TruncDate
from django.utils.translation import gettext_lazy as _

from publication.presentation import display_value
from testimonies.models import Testimony

# Filters offered (browsing and filters, section 3.1). The options of each are the
# values that published testimonies actually have: no other threshold applies.
FILTERS = {
    "language": ("language", _("Original language"), "language"),
    "country": ("public_revision__country", _("Country"), "country"),
    "field": ("public_revision__field", _("Field"), "field"),
    "relationship": (
        "public_revision__relationship_to_ai",
        _("Relationship to AI"),
        "relationship_to_ai",
    ),
    "organization_type": (
        "public_revision__organization_type",
        _("Type of organization"),
        "organization_type",
    ),
    "age_range": ("public_revision__age_range", _("Age range"), "age_range"),
    "ai_use": (
        "public_revision__ai_use_frequency",
        _("How often AI is used"),
        "ai_use_frequency",
    ),
    "attitude": ("public_revision__attitude", _("Attitude towards AI"), "attitude"),
    "authorship": (
        "public_revision__authorship_category",
        _("AI involvement"),
        "category",
    ),
    "period": ("edition_period", _("Edition period"), "period"),
}

SEARCH_FIELDS = ("public_revision__body", "public_revision__display_name")


def published():
    return Testimony.objects.filter(state=Testimony.State.PUBLISHED).select_related(
        "public_revision"
    )


def selected_filters(params):
    return {name: params[name] for name in FILTERS if params.get(name)}


def apply_filters(queryset, selected):
    for name, value in selected.items():
        lookup = FILTERS[name][0]
        if name == "relationship":
            queryset = queryset.filter(**{f"{lookup}__contains": [value]})
        elif name == "period":
            queryset = queryset.filter(**{lookup: int(value)})
        else:
            queryset = queryset.filter(**{lookup: value})
    return queryset


def filter_options(selected):
    options = {}
    for name, (lookup, label, column) in FILTERS.items():
        values = set()
        for value in published().values_list(lookup, flat=True):
            if value is None:
                continue
            values.update(value if isinstance(value, list) else [value])
        options[name] = {
            "label": label,
            "choices": [
                (
                    str(value),
                    display_value(column, value),
                    str(value) == selected.get(name),
                )
                for value in sorted(values, key=str)
            ],
        }
    return options


def search(queryset, text):
    # Full-text search in the configuration of each testimony's language (data model, section 7).
    # Languages without a stemmer use the simple configuration.
    queryset = queryset.annotate(
        french_document=SearchVector(*SEARCH_FIELDS, config="french"),
        english_document=SearchVector(*SEARCH_FIELDS, config="english"),
        simple_document=SearchVector(*SEARCH_FIELDS, config="simple"),
    )
    is_french = Q(language__startswith="fr")
    is_english = Q(language__startswith="en")
    return queryset.filter(
        (is_french & Q(french_document=SearchQuery(text, config="french")))
        | (is_english & Q(english_document=SearchQuery(text, config="english")))
        | (
            ~is_french
            & ~is_english
            & Q(simple_document=SearchQuery(text, config="simple"))
        )
    )


def ordered(queryset):
    return queryset.annotate(day=TruncDate("published_at")).order_by(
        "-day", "public_id"
    )
