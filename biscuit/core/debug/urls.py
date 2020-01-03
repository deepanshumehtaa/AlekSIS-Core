from django.urls import path

from . import views

urlpatterns = [
    path("", views.debugging_tool),
    path("logs/", views.debugging_tool, name="debug_logs")
]
