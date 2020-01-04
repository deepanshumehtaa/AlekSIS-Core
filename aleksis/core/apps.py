from django.apps import AppConfig, apps

from constance.signals import config_updated

from .signals import clean_scss


class CoreConfig(AppConfig):
    name = "aleksis.core"
    verbose_name = "AlekSIS — The Free School Information System"

    def ready(self) -> None:
        clean_scss()
        config_updated.connect(clean_scss)
