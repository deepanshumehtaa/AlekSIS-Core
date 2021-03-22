from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from maintenance_mode.backends import AbstractStateBackend


class DefaultStorageBackend(AbstractStateBackend):
    """django-maintenance-mode backend using default cache."""

    def get_value(self) -> bool:
        filename = settings.MAINTENANCE_MODE_STATE_FILE_NAME

        try:
            with default_storage.open(filename) as statefile:
                return bool(int(statefile.read()))
        except IOError:
            return False

    def set_value(self, value: bool) -> None:
        filename = settings.MAINTENANCE_MODE_STATE_FILE_NAME

        if default_storage.exists(filename):
            default_storage.delete(filename)
        default_storage.save(filename, ContentFile(str(int(value))))
