from datetime import timedelta

from constance import config
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .util.core_helpers import celery_optional, year_agnostic_date_range_query
from .util.notifications import send_notification as _send_notification
from .models import Notification, Person


@celery_optional
def send_notification(notification: int, resend: bool = False) -> None:
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
