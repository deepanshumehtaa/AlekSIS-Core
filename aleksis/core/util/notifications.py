""" Utility code for notification system """

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from constance import config


def get_notification_choices():
    """ Return all available channels for notifications.

    This gathers the channels that are technically available as per the
    system configuration. Which ones are available to users is defined
    by the administrator (by selecting a subset of these choices).
    """

    choices = []

    if config.get("MAIL_OUT", None):
        choices += ("email", _("E-Mail"))

    if settings.get("TWILIO_SID", None):
        choices += ("sms", _("SMS"))

    return choices

get_notification_choices_lazy = lazy(get_notification_choices, tuple)
