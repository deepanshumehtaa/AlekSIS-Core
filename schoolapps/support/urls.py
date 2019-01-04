from django.urls import path

from support import views

urlpatterns = [
    path("rebus/", views.rebus, name="rebus"),
    path("feedback/", views.feedback, name="feedback"),
]

