from django.urls import path

from reports import views

app_name = "reports"

urlpatterns = [
    path("testimonies/<str:public_id>/report/", views.report_form, name="report"),
    path("reports/confirm/<str:token>/", views.confirm_report, name="confirm"),
]
