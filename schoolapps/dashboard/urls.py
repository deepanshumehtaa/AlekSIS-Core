from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('mail/', views.test_mail, name='dashboard_mail')
]
