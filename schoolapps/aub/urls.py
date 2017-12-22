from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name='aub_index'),
    path('details/<int:aub_id>/', views.details, name='aub_details'),
    path('apply_for', views.apply_for, name='aub_apply_for')
]
