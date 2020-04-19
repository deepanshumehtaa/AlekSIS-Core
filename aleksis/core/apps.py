from typing import Any, List, Optional, Tuple

import django.apps
from django.contrib.auth.signals import user_logged_in
from django.http import HttpRequest

from .signals import clean_scss
from .util.apps import AppConfig
from .util.core_helpers import has_person


class CoreConfig(AppConfig):
    name = "aleksis.core"
    verbose_name = "AlekSIS — The Free School Information System"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/official/AlekSIS/",
    }
    licence = "EUPL-1.2+"
    copyright = (
        ([2017, 2018, 2019, 2020], "Jonathan Weth", "wethjo@katharineum.de"),
        ([2017, 2018, 2019], "Frank Poetzsch-Heffter", "p-h@katharineum.de"),
        ([2018, 2019, 2020], "Julian Leucker", "leuckeju@katharineum.de"),
        ([2018, 2019, 2020], "Hangzhi Yu", "yuha@katharineum.de"),
        ([2019, 2020], "Dominik George", "dominik.george@teckids.org"),
        ([2019, 2020], "mirabilos", "thorsten.glaser@teckids.org"),
        ([2019, 2020], "Tom Teichler", "tom.teichler@teckids.org"),
    )

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
        **kwargs,
    ) -> None:
        super().post_migrate(app_config, verbosity, interactive, using, plan, apps)

        # Ensure presence of a OTP YubiKey default config
        apps.get_model("otp_yubikey", "ValidationService").objects.using(using).update_or_create(
            name="default", defaults={"use_ssl": True, "param_sl": "", "param_timeout": ""}
        )

    def user_logged_in(
        self, sender: type, request: Optional[HttpRequest], user: "User", **kwargs
    ) -> None:
        if has_person(user):
            # Save the associated person to pick up defaults
            user.person.save()
