from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='fibu_index'),
    path('bookings/check', views.check, name='booking_check'),
    path('bookings/edit/<int:id>', views.edit, name='booking_edit'),
    path('bookings/new', views.new_booking, name='new_booking'),
    path('bookings/', views.booking, name='booking'),
    path('bookings/<str:is_archive>', views.booking, name='booking'),
    path('bookings/book/<int:id>', views.book, name='booking_book'),
    path('costcenter', views.cost_centers, name='fibu_cost_centers'),
    path('costcenter/edit/<int:id>', views.cost_center_edit, name='fibu_cost_centers_edit'),
    path('account', views.account, name='account'),
    path('account/edit/<int:id>', views.account_edit, name='account_edit'),
    path('reports', views.reports, name='reports'),
    path('reports/expenses', views.expenses, name='expenses'),
    # path('make_booking', views.make_booking, name='fibu_make_booking'),
    # path('edit/<int:id>', views.edit, name='booking_edit'),
]
