from .signals import clean_scss
from .util.apps import AppConfig


class CoreConfig(AppConfig):
    name = "aleksis.core"
    verbose_name = "AlekSIS — The Free School Information System"

    def ready(self) -> None:
        super().ready()

    def config_updated(self, *args, **kwargs) -> None:
        clean_scss()
