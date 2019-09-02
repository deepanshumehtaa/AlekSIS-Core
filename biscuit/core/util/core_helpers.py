from importlib import import_module
import pkgutil
from typing import Optional, Sequence
from warnings import warn

from django.apps import apps
from django.conf import settings
from django.http import HttpRequest

from django_global_request.middleware import get_request


def get_app_packages() -> Sequence[str]:
    """ Find all packages within the biscuit.apps namespace. """

    # Import error are non-fatal here because probably simply no app is installed.
    try:
        import biscuit.apps
    except ImportError:
        return []

    pkgs = []
    for pkg in pkgutil.iter_modules(biscuit.apps.__path__):
        mod = import_module('biscuit.apps.%s' % pkg[1])

        # Add additional apps defined in module's INSTALLED_APPS constant
        additional_apps = getattr(mod, 'INSTALLED_APPS', [])
        for app in additional_apps:
            if app not in pkgs:
                pkgs.append(app)

        pkgs.append('biscuit.apps.%s' % pkg[1])

    return pkgs


# FIXME Use more specific result type
def get_current_school() -> Optional:
    request = get_request()

    if request:
        # We are inside a web request, thus called from a public interface

        if hasattr(request, 'user') and hasattr(request.user, 'person'):
            # Use the same school as that of the logged-in user
            return request.user.person.school
        else:
            # Set no school so no data is ever returned
            # during an unauthenticated request
            return None
    else:
        # We are called from outside a request (probably shell),
        # thus called from a private interface

        School = apps.get_model('core.School')

        if hasattr(settings, 'DEFAULT_SCHOOL'):
            # Use school defined in settings
            return School.objects.get(pk=settings.DEFAULT_SCHOOL)
        else:
            # Use first school
            warn('No school set, using first known school.', RuntimeWarning)
            return School.objects.first()

    # Raise an exception because not finding a school wreaks havoc
    raise RuntimeError('No school set or found. Check your database.')


def is_impersonate(request: HttpRequest) -> bool:
    if hasattr(request, 'user'):
        return getattr(request.user, 'is_impersonate', False)
