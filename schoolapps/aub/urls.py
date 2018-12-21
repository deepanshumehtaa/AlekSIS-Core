from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='aub_index'),
    path('details/<int:aub_id>/', views.details, name='aub_details'),
    path('apply_for', views.apply_for, name='aub_apply_for'),
    path('applied_for', views.applied_for, name='aub_applied_for'),
    path('check1', views.check1, name='aub_check1'),
    path('check2', views.check2, name='aub_check2'),
    ]
