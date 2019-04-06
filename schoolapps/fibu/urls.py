from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='booking_index'),
    path('edit/<int:id>', views.edit, name='booking_edit'),
    ]
