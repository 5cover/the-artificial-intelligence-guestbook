from django.urls import path

from testimonies import views, withdrawal_views

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
    path("account/withdraw/", withdrawal_views.account_withdraw, name="withdraw"),
    path("withdraw/", withdrawal_views.public_withdraw, name="withdraw-public"),
    path(
        "withdraw/link/<str:token>/",
        withdrawal_views.withdraw_confirm,
        name="withdraw-confirm",
    ),
    path("account/close/", withdrawal_views.account_close, name="close"),
    path(
        "close/link/<str:token>/",
        withdrawal_views.closure_confirm,
        name="close-confirm",
    ),
]
