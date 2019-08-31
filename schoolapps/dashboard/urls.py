from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('api', views.api_information, name="api_information"),
    path('test/', views.test_notification, name='test'),
]
