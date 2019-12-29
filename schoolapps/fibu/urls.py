from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='fibu_index'),
    path('<int:pk>/', views.user_edit, name='fibu_bookings_user_edit'),
    path('bookings/check/', views.check, name='fibu_bookings_check'),
    path('bookings/new/', views.new_booking, name='fibu_bookings_new'),
    path('bookings/', views.booking, name='fibu_bookings'),
    path('bookings/<str:is_archive>/', views.booking, name='fibu_bookings_archive'),
    path('bookings/<int:pk>/edit/', views.book, name='fibu_bookings_edit'),
    path('costcenters/', views.cost_centers, name='fibu_cost_centers'),
    path('costcenters/edit/<int:pk>/', views.cost_center_edit, name='fibu_cost_centers_edit'),
    path('accounts/', views.account, name='fibu_accounts'),
    path('accounts/<int:pk>/', views.account_edit, name='fibu_accounts_edit'),
    path('reports/', views.reports, name='fibu_reports'),
    path('reports/expenses/', views.expenses, name='fibu_reports_expenses'),
]
