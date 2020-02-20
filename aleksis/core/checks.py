from typing import Optional

import django.apps
from django.core.checks import Tags, Warning, register

from .util.apps import AppConfig


@register(Tags.compatibility)
def check_app_configs_base_class(
    app_configs: Optional[django.apps.registry.Apps] = None, **kwargs
) -> list:
    """ Checks whether all apps derive from AlekSIS's base app config """

    results = []

    if app_configs is None:
        app_configs = django.apps.apps.get_app_configs()

    for app_config in filter(lambda c: c.name.startswith("aleksis.apps."), app_configs):
        if not isinstance(app_config, AppConfig):
            results.append(
                Warning(
                    "App config %s does not derive from aleksis.core.util.apps.AppConfig.",
                    hint="Ensure the app uses the correct base class for all registry functionality to work.",
                    obj=app_config,
                    id="aleksis.core.W001",
                )
            )

    return results
