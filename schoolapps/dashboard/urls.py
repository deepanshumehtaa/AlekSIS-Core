from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('test/', views.test_notification, name='test'),
    path('faq/', views.faq, name='faq')
]

