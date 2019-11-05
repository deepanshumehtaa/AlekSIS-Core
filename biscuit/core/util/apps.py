from importlib import import_module

import django.apps


class AppConfig(django.apps.AppConfig):
    """ An extended version of DJango's AppConfig container. """

    def ready(self):
        super().ready()

        # Run model extension code in all apps
        for app in django.apps.get_app_configs():
            try:
                import_module('%s.model_extensions' % app.module.__name__)
            except ImportError:
                # ImportErrors are non-fatal because model extensions are optional.
                pass
