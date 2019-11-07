from importlib import import_module

import django.apps


class AppConfig(django.apps.AppConfig):
    """ An extended version of DJango's AppConfig container. """

    def ready(self):
        super().ready()

        # Run model extension code
        try:
            import_module('%s.model_extensions' % self.__class__.__module__.package.name)
        except ImportError:
            # ImportErrors are non-fatal because model extensions are optional.
            pass
