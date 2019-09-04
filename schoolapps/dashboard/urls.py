from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('api', views.api_information, name="api_information"),
    path('api/notifications/read/<int:id>', views.api_read_notification, name="api_read_notification"),
    path('api/my-plan', views.api_my_plan_html, name="api_my_plan_html"),
    path('test/', views.test_notification, name='test'),
]
