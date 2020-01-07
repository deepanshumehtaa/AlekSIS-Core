from typing import Callable

from django.contrib.auth.decorators import login_required, user_passes_test

from aleksis.core.util.core_helpers import has_person


def admin_required(function: Callable = None) -> Callable:
    actual_decorator = user_passes_test(lambda u: u.is_active and u.is_superuser)
    return actual_decorator(function)


def person_required(function: Callable = None) -> Callable:
    """ Requires a logged-in user which is linked to a person. """

    actual_decorator = user_passes_test(has_person)
    return actual_decorator(login_required(function))
