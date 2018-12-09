from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="menu_index"),
    path('upload/', views.upload, name="menu_upload"),
    path('delete/<int:id>', views.delete, name="menu_delete"),
    path('current.pdf', views.show_current, name="menu_show_current"),
    path('<str:msg>', views.index, name="menu_index_msg"),
]
