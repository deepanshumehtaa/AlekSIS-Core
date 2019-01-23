import pkgutil

def get_app_packages():
    import biscuit.apps
    pkgs = ['biscuit.apps.%s' % i[1] for i in pkgutil.iter_modules(biscuit.apps.__path__)]

    return pkgs
