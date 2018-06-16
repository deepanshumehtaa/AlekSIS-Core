from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('test/', views.error_404, name='error_404'),
    path('impress/', views.impress, name='impress')
]

