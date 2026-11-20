from django.urls import path

from publication import views

app_name = "publication"

urlpatterns = [
    path("", views.home, name="home"),
    path("testimonies/", views.listing, name="listing"),
    path("testimonies/<str:public_id>", views.testimony, name="testimony"),
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
