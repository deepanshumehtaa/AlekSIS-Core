from django.conf import settings
from django.forms import EmailField, URLField
from django.utils.translation import gettext_lazy as _

from colorfield.widgets import ColorWidget
from dynamic_preferences.types import BooleanPreference, StringPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.users.registries import user_preferences_registry


general = Section("general")
theme = Section("theme")
mail = Section("mail")
notification = Section("notification")
footer = Section("footer")
account = Section("account")


@global_preferences_registry.register
class SiteTitle(StringPreference):
    section = general
    name = "title"
    default = "AlekSIS"
    required = False
    verbose_name = _("Site title")


@global_preferences_registry.register
class SiteDescription(StringPreference):
    section = general
    name = "description"
    default = "The Free School Information System"
    required = False
    verbose_name = _("Site description")


@global_preferences_registry.register
class ColourPrimary(StringPreference):
    section = theme
    name = "primary"
    default = "#0d5eaf"
    required = False
    verbose_name = _("Primary colour")
    widget = ColorWidget


@global_preferences_registry.register
class ColourSecondary(StringPreference):
    section = theme
    name = "secondary"
    default = "#0d5eaf"
    required = False
    verbose_name = _("Secondary colour")
    widget = ColorWidget


@global_preferences_registry.register
class MailOutName(StringPreference):
    section = mail
    name = "name"
    default = "AlekSIS"
    required = False
    verbose_name = _("Mail out name")


@global_preferences_registry.register
class MailOut(StringPreference):
    section = mail
    name = "name"
    default = settings.DEFAULT_FROM_EMAIL
    required = False
    verbose_name = _("Mail out address")
    widget = EmailField


@global_preferences_registry.register
class PrivacyURL(StringPreference):
    section = footer
    name = "privacy_url"
    default = ""
    required = False
    verbose_name = _("Link to privacy policy")
    widget = URLField


@global_preferences_registry.register
class ImprintURL(StringPreference):
    section = footer
    name = "imprint_url"
    default = ""
    required = False
    verbose_name = _("Link to imprint")
    widget = URLField


@user_preferences_registry.register
class AdressingNameFormat(ChoicePreference):
    section = notification
    name = "addressing_name_format"
    default = "german"
    required = False
    verbose_name = _("Name format for addressing")
    choices = (
               (None, "-----"),
               ("german", "John Doe"),
               ("english", "Doe, John"),
               ("dutch", "Doe John"),
              )


@user_preferences_registry.register
class NotificationChannels(MultipleChoicePreference):
    section = notification
    name = "channels"
    default = ["email"]
    required = False
    verbose_name = _("Channels to use for notifications")
    choices = get_notification_choices_lazy


@global_preferences_registry.register
class PrimaryGroupPattern(StringPreference):
    section = account
    name = "primary_group_pattern"
    default = ""
    required = False
    verbose_name = _("Regular expression to match primary group, e.g. '^Class .*'")
