from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='fibu_index'),
    path('check', views.check, name='booking_check'),
    path('check', views.check, name='booking_check1'),
    path('check', views.check, name='booking_check2'),
    # path('make_booking', views.make_booking, name='fibu_make_booking'),
    # path('edit/<int:id>', views.edit, name='booking_edit'),
    ]
