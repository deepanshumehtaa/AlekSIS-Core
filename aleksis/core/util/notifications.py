""" Utility code for notification system """

from typing import Sequence

from django.conf import settings
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _

from constance import config
from templated_email import send_templated_mail
try:
    from twilio.rest import Client as TwilioClient
except ImportError:
    TwilioClient = None

from ..models import Notification
from .core_helpers import celery_optional


def send_templated_sms(template_name: str, from_number: str, recipient_list: Sequence[str], context: dict):
    """ Render a plan-text template and send via SMS to all recipients. """

    template = get_template(template_name)
    text = template.render(context)

    client = TwilioClient(settings.TWILIO_SID, settings.TWILIO_TOKEN)
    for recipient in recipient_list:
        client.messages.create(body=text, to=recipient, from_=from_number)


def _send_notification_email(notification: Notification, template: str = "notification") -> None:
    context = {
        "notification": notification,
        "notification_user": notification.person.adressing_name,
    }
    send_templated_mail(
        template_name=template,
        from_email=config.MAIL_OUT,
        recipient_list=[notification.person.email],
        context=context,
    )


def _send_notification_sms(notification: Notification, template: str = "sms/notification.txt") -> None:
    context = {
        "notification": notification,
        "notification_user": notification.person.adressing_name,
    }
    send_templated_sms(
        template_name=template,
        from_number=settings.TWILIO_CALLER_ID,
        recipient_list=[notification.person.mobile_number],
        context=context,
    )


# Mapping of channel id to name and two functions:
# - Check for availability
# - Send notification through it
_CHANNELS_MAP = {
    "email": (_("E-Mail"), lambda: config.get("MAIL_OUT", None), _send_notification_email),
    "sms": (_("SMS"), lambda: settings.get("TWILIO_SID", None), _send_notification_sms),
}


@celery_optional
def send_notification(notification: Union[int, Notification], resend: bool = False) -> None:
    """ Send a notification through enabled channels.

    If resend is passed as True, the notification is sent even if it was
    previously marked as sent.
    """

    channels = config.get("NOTIFICATION_CHANNELS", [])

    if isinstance(notification, int):
        notification = Notification.objects.get(pk=notification)

    if resend or not notification.sent:
        for channel in channels:
            name, check, send = _CHANNEL_MAPS[channel]
            if check():
                send(notification)

    notification.sent = True
    notification.save()


def get_notification_choices() -> list:
    """ Return all available channels for notifications.

    This gathers the channels that are technically available as per the
    system configuration. Which ones are available to users is defined
    by the administrator (by selecting a subset of these choices).
    """

    choices = []
    for channel, (name, check, send) in _CHANNEL_MAPS:
        if check():
            choices += (channel, name)
    return choices

get_notification_choices_lazy = lazy(get_notification_choices, tuple)
