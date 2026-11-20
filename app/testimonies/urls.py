from django.urls import path

from testimonies import views

app_name = "testimonies"

urlpatterns = [
    path("account/testimony/", views.my_testimony, name="my-testimony"),
    path("account/testimony/submit/", views.submit_testimony, name="submit"),
    path(
        "account/testimony/parental/",
        views.parental_request,
        name="parental-request",
    ),
    path("parental/<str:token>/", views.parental_confirm, name="parental-confirm"),
]
