from django.core import management

from .util.core_helpers import celery_optional
from .util.notifications import send_notification as _send_notification


@celery_optional
def send_notification(notification: int, resend: bool = False) -> None:
    _send_notification(notification, resend)


@celery_optional
def backup_data() -> None:
    db_options = "-z " * settings.DBBACKUP_COMPRESS_DB + "-e" * settings.DBBACKUP_ENCRYPT_DB
    media_options = "-z " * settings.DBBACKUP_COMPRESS_MEDIA + "-e" * settings.DBBACKUP_ENCRYPT_MEDIA

    management.call_command("dbbackup", db_options)
    management.call_command("mediabackup", media_options)
