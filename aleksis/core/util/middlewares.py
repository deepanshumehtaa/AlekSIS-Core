from typing import Callable

from django.http import HttpRequest, HttpResponse

from ..models import DummyPerson, Person
from .core_helpers import get_site_preferences, has_person


class EnsurePersonMiddleware:
    """Middleware that ensures that the logged-in user is linked to a person.

    It is needed to inject a dummy person to a superuser that would otherwise
    not have an associated person, in order they can get their account set up
    without external help.

    In addition, if configured in preferences, it auto-creates or links persons
    to regular users if they match.
    """

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if not has_person(request):
            if request.user.is_superuser:
                # Super-users get a dummy person linked
                dummy_person = DummyPerson(
                    first_name=request.user.first_name, last_name=request.user.last_name
                )
                request.user.person = dummy_person
            else:
                prefs = get_site_preferences()

                if prefs.get("account__auto_link_person", False):
                    person, created = Person.objects.get_or_create(
                        email=request.user.email,
                        defaults={
                            "first_name": request.user.first_name,
                            "last_name": request.user.last_name,
                        },
                    )
                    if created and not prefs.get("account__auto_create_person"):
                        return

                    person.user = request.user
                    person.save()

        response = self.get_response(request)
        return response
