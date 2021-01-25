"""Utility code for notification system."""

from typing import Sequence, Union

from django.apps import apps
from django.conf import settings
from django.template.loader import get_template
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _

from notifications.channels import __import_channel as import_channel
from templated_email import send_templated_mail

from .core_helpers import lazy_preference

try:
    from twilio.rest import Client as TwilioClient
except ImportError:
    TwilioClient = None


def send_templated_sms(
    template_name: str, from_number: str, recipient_list: Sequence[str], context: dict
) -> None:
    """Render a plan-text template and send via SMS to all recipients."""
    template = get_template(template_name)
    text = template.render(context)

    client = TwilioClient(settings.TWILIO_SID, settings.TWILIO_TOKEN)
    for recipient in recipient_list:
        client.messages.create(body=text, to=recipient, from_=from_number)


def _send_notification_email(notification: "Notification", template: str = "notification") -> None:
    context = {
        "notification": notification,
        "notification_user": notification.recipient.addressing_name,
    }
    send_templated_mail(
        template_name=template,
        from_email=lazy_preference("mail", "address"),
        recipient_list=[notification.recipient.email],
        context=context,
    )


def _send_notification_sms(
    notification: "Notification", template: str = "sms/notification.txt"
) -> None:
    context = {
        "notification": notification,
        "notification_user": notification.recipient.addressing_name,
    }
    send_templated_sms(
        template_name=template,
        from_number=settings.TWILIO_CALLER_ID,
        recipient_list=[notification.recipient.mobile_number.as_e164],
        context=context,
    )


def get_notification_choices() -> list:
    """Return all available channels for notifications.

    This gathers the channels that are technically available as per the
    system configuration. Which ones are available to users is defined
    by the administrator (by selecting a subset of these choices).
    """
    choices = []
    for channel, path in settings.NOTIFICATIONS_CHANNELS.items():
        module = import_channel(path)
        name = getattr(module, "verbose_name", channel)

        choices.append((name, channel))
    return choices


get_notification_choices_lazy = lazy(get_notification_choices, tuple)
