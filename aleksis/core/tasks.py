from django.conf import settings
from django.core import management

from .util.core_helpers import celery_optional


@celery_optional
def backup_data() -> None:
    """Backup database and media using django-dbbackup."""
    # Assemble command-line options for dbbackup management command
    db_options = []
    if settings.DBBACKUP_COMPRESS_DB:
        db_options.append("-z")
    if settings.DBBACKUP_ENCRYPT_DB:
        db_options.append("-e")
    if settings.DBBACKUP_CLEANUP_DB:
        db_options.append("-c")

    media_options = []
    if settings.DBBACKUP_COMPRESS_MEDIA:
        media_options.append("-z")
    if settings.DBBACKUP_ENCRYPT_MEDIA:
        media_options.append("-e")
    if settings.DBBACKUP_CLEANUP_MEDIA:
        media_options.append("-c")

    # Hand off to dbbackup's management commands
    management.call_command("dbbackup", *db_options)
    management.call_command("mediabackup", *media_options)
