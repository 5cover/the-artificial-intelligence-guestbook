from django.urls import path
from django.views.generic import TemplateView

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("sign-in/", views.sign_in_request, name="sign-in"),
    path(
        "sign-in/sent/",
        TemplateView.as_view(template_name="accounts/sign_in_sent.html"),
        name="sign-in-sent",
    ),
    path("sign-in/link/<str:token>/", views.sign_in_link, name="sign-in-link"),
    path("sign-out/", views.sign_out_request, name="sign-out"),
    path("account/", views.account_home, name="account"),
]
