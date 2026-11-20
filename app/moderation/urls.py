from django.urls import path

from moderation import views

app_name = "moderation"

urlpatterns = [
    path("moderation/", views.queue, name="queue"),
    path("moderation/review/<str:token>/", views.review, name="review"),
    path("moderation/review/<str:token>/decide/", views.decide, name="decide"),
]
