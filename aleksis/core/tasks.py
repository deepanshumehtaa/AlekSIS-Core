from datetime import timedelta

from constance import config
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.core import management

from .util.core_helpers import celery_optional, year_agnostic_date_range_query
from .util.notifications import send_notification as _send_notification
from .models import Notification, Person


@celery_optional
def send_notification(notification: int, resend: bool = False) -> None:
    """Send a notification object to its recipient.

    :param notification: primary key of the notification object to send
    :param resend: Define whether to also send if the notification was already sent
    """
    _send_notification(notification, resend)


@celery_optional
def birthday_announcement():
    if config.ENABLE_BIRTHDAY_ANNOUNCEMENT:
        subscribers = Person.objects.all()
    else:
        subscribers = Person.objects.empty()

    yesterday = timezone.now().date() - timedelta(days=1)

    for subscriber in subscribers:
        query = year_agnostic_date_range_query(config.BIRTHDAY_DAYS, "date_of_birth")
        persons = Person.objects.filter(query).order_by("date_of_birth__month", "date_of_birth__day", "-date_of_birth__year")

        description = ""
        for person in persons:
            description += _('%s\t%s (%s years)\n') % (person.date_of_birth, person.full_name, str(person.age_at(yesterday)+1))

        Notification.objects.create(
            sender = _("AlekSIS"),
            title = _("Upcoming birthdays"),
            recipient = subscriber,
            description = description,
        )


@celery_optional
def backup_data() -> None:
    """Backup database and media using django-dbbackup."""
    # Assemble command-line options for dbbackup management command
    db_options = "-z " * settings.DBBACKUP_COMPRESS_DB + "-e" * settings.DBBACKUP_ENCRYPT_DB
    media_options = (
        "-z " * settings.DBBACKUP_COMPRESS_MEDIA + "-e" * settings.DBBACKUP_ENCRYPT_MEDIA
    )

    # Hand off to dbbackup's management commands
    management.call_command("dbbackup", db_options)
    management.call_command("mediabackup", media_options)
