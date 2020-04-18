from importlib import import_module
from typing import Any, List, Optional, Tuple

import django.apps
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_migrate, pre_migrate
from django.http import HttpRequest

from constance.signals import config_updated
from license_expression import Licensing, LicenseSymbol
from spdx_license_list import LICENSES


class AppConfig(django.apps.AppConfig):
    """ An extended version of DJango's AppConfig container. """

    def ready(self):
        super().ready()

        # Run model extension code
        try:
            import_module(
                ".".join(self.__class__.__module__.split(".")[:-1] + ["model_extensions"])
            )
        except ImportError:
            # ImportErrors are non-fatal because model extensions are optional.
            pass

        # Register default listeners
        pre_migrate.connect(self.pre_migrate, sender=self)
        post_migrate.connect(self.post_migrate, sender=self)
        config_updated.connect(self.config_updated)
        user_logged_in.connect(self.user_logged_in)
        user_logged_out.connect(self.user_logged_out)

        # Getting an app ready means it should look at its config once
        self.config_updated()

        # Register system checks of this app
        try:
            import_module(".".join(self.__class__.__module__.split(".")[:-1] + ["checks"]))
        except ImportError:
            # ImportErrors are non-fatal because checks are optional.
            pass

    @classmethod
    def get_name(cls):
        return getattr(cls, "verbose_name", cls.name)
        # TODO Try getting from distribution if not set

    @classmethod
    def get_version(cls):
        try:
            from .. import __version__  # noqa
        except ImportError:
            __version__ = None

        return getattr(cls, "version", __version__)

    @classmethod
    def get_licence(cls) -> Tuple:
        licence = getattr(cls, "licence", None)

        default_dict = {
            'isDeprecatedLicenseId': False,
            'isFsfLibre': False,
            'isOsiApproved': False,
            'licenseId': 'unknown',
            'name': 'Unknown Licence',
            'referenceNumber': -1,
            'url': '',
        }

        if licence:
            licensing = Licensing(LICENSES.keys())
            parsed = licensing.parse(licence).simplify()
            readable = parsed.render_as_readable()

            for symbol in parsed.symbols:
                licence_dict = LICENSES.get(symbol.key, None)

                if licence_dict is None:
                    licence_dict = default_dict
                else:
                    licence_dict["url"] = "https://spdx.org/licenses/{}.html".format(licence_dict["licenseId"])

            return (readable, licence_dicts)
        else:
            return ("Unknown", [default_dict])

    @classmethod
    def get_urls(cls):
        return getattr(cls, "urls", {})
        # TODO Try getting from distribution if not set

    @classmethod
    def get_copyright(cls):
        return getattr(self, "copyright", tuple())
        # TODO Try getting from distribution if not set

    def config_updated(
        self,
        key: Optional[str] = "",
        old_value: Optional[Any] = None,
        new_value: Optional[Any] = None,
        **kwargs,
    ) -> None:
        """ Called on every app instance if a Constance config chagnes, and once on startup

        By default, it does nothing.
        """
        pass

    def pre_migrate(
        self,
        app_config: django.apps.AppConfig,
        verbosity: int,
        interactive: bool,
        using: str,
        plan: List[Tuple],
        apps: django.apps.registry.Apps,
        **kwargs,
    ) -> None:
        """ Called on every app instance before its models are migrated

        By default, it does nothing.
        """
        pass

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
        """ Called on every app instance after its models have been migrated

        By default, asks all models to do maintenance on their default data.
        """
        self._maintain_default_data()

    def user_logged_in(
        self, sender: type, request: Optional[HttpRequest], user: "User", **kwargs
    ) -> None:
        """ Called after a user logged in

        By default, it does nothing.
        """
        pass

    def user_logged_out(
        self, sender: type, request: Optional[HttpRequest], user: "User", **kwargs
    ) -> None:
        """ Called after a user logged out

        By default, it does nothing.
        """
        pass

    def _maintain_default_data(self):
        if not self.models_module:
            # This app does not have any models, so bail out early
            return

        for model in self.get_models():
            if hasattr(model, "maintain_default_data"):
                # Method implemented by each model object; can be left out
                model.maintain_default_data()
