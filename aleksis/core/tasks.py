from .util.core_helpers import celery_optional, update_geolocation
from .util.notifications import send_notification as _send_notification


@celery_optional
def send_notification(notification: int, resend: bool = False) -> None:
    _send_notification(notification, resend)


@celery_optional
def update_coordinates() -> None:
    for person in Person.objects.all():
        update_geolocation(person)
