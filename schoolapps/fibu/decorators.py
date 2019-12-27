from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

from .models import Booking


# prevent to show aub details from foreign users
def check_own_booking_verification(user):
    return Booking.objects.all().filter(created_by=user)


def check_own_booking(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user only gets his own bookings, redirecting
    to the dashboard if necessary.
    """
    actual_decorator = user_passes_test(
        check_own_booking_verification,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
