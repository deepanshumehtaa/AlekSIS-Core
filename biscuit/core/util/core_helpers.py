from importlib import import_module
import pkgutil
from typing import Optional, Sequence

from django.http import HttpRequest


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


def get_current_school() -> int:
    return 1


def is_impersonate(request: HttpRequest) -> bool:
    if hasattr(request, 'user'):
        return getattr(request.user, 'is_impersonate', False)
    else:
        return False


def has_person(request: HttpRequest) -> bool:
    if hasattr(request, 'user'):
        return getattr(request.user, 'person', None) is not None
    else:
        return False
