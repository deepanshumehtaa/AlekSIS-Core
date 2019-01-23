import pkgutil
from typing import Sequence

def get_app_packages() -> Sequence:
    """ Find all packages within the biscuit.apps namespace. """

    import biscuit.apps
    pkgs = ['biscuit.apps.%s' % i[1] for i in pkgutil.iter_modules(biscuit.apps.__path__)]

    return pkgs
