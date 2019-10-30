from django.urls import path
from . import views

urlpatterns = [
    path('', views.faq, name='faq'),
    path('ask', views.ask, name='ask-faq')
]
