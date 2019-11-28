from glob import glob
import os
from warnings import warn

from django.apps import AppConfig, apps
from django.conf import settings
from django.db.utils import ProgrammingError


class CoreConfig(AppConfig):
    name = 'biscuit.core'
    verbose_name = 'BiscuIT - The Free School Information System'

    def clean_scss(self) -> None:
        for source_map in glob(os.path.join(settings.STATIC_ROOT, '*.css.map')):
            try:
                os.unlink(source_map)
            except OSError:
                # Ignore because old is better than nothing
                pass  # noqa

    def setup_data(self) -> None:
        if 'otp_yubikey' in settings.INSTALLED_APPS:
            try:
                apps.get_model('otp_yubikey', 'ValidationService').objects.update_or_create(
                    name='default', defaults={'use_ssl': True, 'param_sl': '', 'param_timeout': ''}
                )
            except ProgrammingError:
                warn('Yubikey validation service could not be created yet. If you are currently in a migration, this is expected.')

    def ready(self) -> None:
        self.clean_scss()
        self.setup_data()
