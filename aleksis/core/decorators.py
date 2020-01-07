from typing import Callable

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User


def admin_required(function: Callable = None) -> Callable:
    actual_decorator = user_passes_test(lambda u: u.is_active and u.is_superuser)
    return actual_decorator(function)


def has_person_by_user(user: User) -> bool:
    return getattr(user, "person", None) is not None


def person_required(function: Callable = None) -> Callable:
    """ Requires a logged-in user which is linked to a person. """

    actual_decorator = user_passes_test(has_person_by_user)
    return actual_decorator(login_required(function))
