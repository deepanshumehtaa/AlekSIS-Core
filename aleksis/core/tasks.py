from .util.core_helpers import celery_optional
from .util.notifications import send_notification as _send_notification


@celery_optional
def send_notification(notification: int, resend: bool = False) -> None:
    _send_notification(notification, resend)
