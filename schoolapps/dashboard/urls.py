from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    # path('test/', views.test_notification, name='test'),
    path("tools", views.tools, name="tools"),
    path("tools/clear-cache", views.tools_clear_cache, name="tools_clear_cache"),
    path("tools/clear-cache/<str:id>", views.tools_clear_cache, name="tools_clear_single_cache"),
]
