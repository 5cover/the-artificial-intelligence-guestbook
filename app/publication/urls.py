from django.urls import path

from publication import data_views, views

app_name = "publication"

urlpatterns = [
    path("", views.home, name="home"),
    path("testimonies/", views.listing, name="listing"),
    path(
        "testimonies/<str:public_id>.md",
        data_views.testimony_markdown,
        name="testimony-markdown",
    ),
    path("testimonies/<str:public_id>", views.testimony, name="testimony"),
    path("data/testimonies.json", data_views.index, name="data-index"),
    path(
        "data/testimonies/<str:public_id>.json",
        data_views.testimony_json,
        name="data-testimony",
    ),
    path("data/withdrawals.json", data_views.withdrawals, name="data-withdrawals"),
    path("data/time-capsules.json", data_views.registry, name="data-registry"),
    path(
        "data/schema/<int:version>/<str:name>.schema.json",
        data_views.schema,
        name="data-schema",
    ),
    path("llms.txt", data_views.llms, name="llms"),
    path("robots.txt", data_views.robots, name="robots"),
    path("context/", views.placeholder, {"page": "context"}, name="context"),
    path("references/", views.placeholder, {"page": "references"}, name="references"),
    path(
        "methodology/", views.placeholder, {"page": "methodology"}, name="methodology"
    ),
    path(
        "publishing-rules/",
        views.placeholder,
        {"page": "publishing-rules"},
        name="publishing-rules",
    ),
    path("privacy/", views.placeholder, {"page": "privacy"}, name="privacy"),
    path("terms/", views.placeholder, {"page": "terms"}, name="terms"),
]
