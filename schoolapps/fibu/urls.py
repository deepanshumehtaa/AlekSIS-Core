from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='fibu_index'),
    path('booking/check', views.check, name='booking_check'),
    path('booking/edit/<int:id>', views.edit, name='booking_edit'),
    path('booking/new', views.new_booking, name='new_booking'),
    path('booking/<int:archiv>', views.booking, name='booking'),
    path('booking/book/<int:id>', views.book, name='booking_book'),
    path('costcenter', views.costcenter, name='costcenter'),
    path('costcenter/edit/<int:id>', views.costcenter_edit, name='costcenter_edit'),
    path('account', views.account, name='account'),
    path('account/edit/<int:id>', views.account_edit, name='account_edit'),
    path('reports', views.reports, name='reports'),
    path('reports/expenses', views.expenses, name='expenses'),
    # path('make_booking', views.make_booking, name='fibu_make_booking'),
    # path('edit/<int:id>', views.edit, name='booking_edit'),
    ]
