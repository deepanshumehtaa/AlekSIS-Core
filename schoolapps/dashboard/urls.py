from django.urls import path

from untisconnect.models import Terms, Schoolyear

try:
    from . import views

    urlpatterns = [
        path('', views.index, name='dashboard'),
        path('api', views.api_information, name="api_information"),
        path('api/notifications/read/<int:id>', views.api_read_notification, name="api_read_notification"),
        path('api/my-plan', views.api_my_plan_html, name="api_my_plan_html"),
    ]

except (Terms.DoesNotExist, Schoolyear.DoesNotExist):
    from timetable import fallback_view

    urlpatterns = [
        path('', fallback_view.fallback, name='dashboard'),
        path('api', fallback_view.fallback, name="api_information"),
        path('api/notifications/read/<int:id>', fallback_view.fallback, name="api_read_notification"),
        path('api/my-plan', fallback_view.fallback, name="api_my_plan_html"),
    ]
