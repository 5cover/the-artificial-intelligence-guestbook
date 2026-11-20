from django.urls import include, path

urlpatterns = [
    path("", include("publication.urls")),
    path("", include("accounts.urls")),
    path("", include("testimonies.urls")),
    path("", include("moderation.urls")),
]
