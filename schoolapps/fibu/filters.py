from django.contrib.auth.models import User
import django_filters
from .models import Booking
from django.db.utils import ProgrammingError


def get_fibu_users():
    """ Find all users who requests a boooking """
    try:
        fibu_users = Booking.objects.values_list('contact')
        users = list(User.objects.filter(id__in=fibu_users))
        # user_ids = [(str(user.id),user.username) for user in users]
        user_ids = [(str(user.id), user.last_name + ', ' + user.first_name) for user in users]
        user_ids_sorted = sorted(user_ids, key=lambda user: user[1])
        return user_ids_sorted
    except ProgrammingError:
        return []


class BookingFilter(django_filters.FilterSet):
    contact = django_filters.ChoiceFilter(label='Von', choices=get_fibu_users())

    class Meta:
        model = Booking
        fields = ['contact', ]
