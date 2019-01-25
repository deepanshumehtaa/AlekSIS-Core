import pkgutil
from typing import Sequence

def get_app_packages() -> Sequence:
    """ Find all packages within the biscuit.apps namespace. """

    # Import error are non-fatal here because probably simply no app is installed.
    try:
        import biscuit.apps
    except ImportError:
        return []

    pkgs = ['biscuit.apps.%s' % i[1] for i in pkgutil.iter_modules(biscuit.apps.__path__)]

    return pkgs
