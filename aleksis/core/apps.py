from typing import Any, List, Optional, Tuple

import django.apps

from .signals import clean_scss
from .util.apps import AppConfig


class CoreConfig(AppConfig):
    name = "aleksis.core"
    verbose_name = "AlekSIS — The Free School Information System"

    def config_updated(self, *args, **kwargs) -> None:
        clean_scss()

    def post_migrate(
        self,
        app_config: django.apps.AppConfig,
        verbosity: int,
        interactive: bool,
        using: str,
        plan: List[Tuple],
        apps: django.apps.registry.Apps,
    ) -> None:
        super().post_migrate(app_config, verbosity, interactive, using, plan, apps)

        # Ensure presence of a OTP YubiKey default config
        apps.get_model('otp_yubikey', 'ValidationService').objects.using(using).update_or_create(
            name='default', defaults={'use_ssl': True, 'param_sl': '', 'param_timeout': ''}
        )
