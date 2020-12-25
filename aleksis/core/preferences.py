from django.conf import settings
from django.forms import EmailField, ImageField, URLField
from django.forms.widgets import SelectMultiple
from django.utils.translation import gettext_lazy as _

from dynamic_preferences.preferences import Section
from dynamic_preferences.types import (
    ChoicePreference,
    FilePreference,
    MultipleChoicePreference,
    StringPreference,
)

from .models import Person
from .registries import person_preferences_registry, site_preferences_registry
from .util.notifications import get_notification_choices_lazy

general = Section("general")
school = Section("school")
theme = Section("theme")
mail = Section("mail")
notification = Section("notification")
footer = Section("footer")
account = Section("account")
auth = Section("auth", verbose_name=_("Authentication"))
internationalisation = Section("internationalisation", verbose_name=_("Internationalisation"))


@site_preferences_registry.register
class SiteTitle(StringPreference):
    """Title of the AlekSIS instance, e.g. schools display name."""

    section = general
    name = "title"
    default = "AlekSIS"
    required = False
    verbose_name = _("Site title")


@site_preferences_registry.register
class SiteDescription(StringPreference):
    """Site description, e.g. a slogan."""

    section = general
    name = "description"
    default = "The Free School Information System"
    required = False
    verbose_name = _("Site description")


@site_preferences_registry.register
class ColourPrimary(StringPreference):
    """Primary colour in AlekSIS frontend."""

    section = theme
    name = "primary"
    default = "#0d5eaf"
    required = False
    verbose_name = _("Primary colour")


@site_preferences_registry.register
class ColourSecondary(StringPreference):
    """Secondary colour in AlekSIS frontend."""

    section = theme
    name = "secondary"
    default = "#0d5eaf"
    required = False
    verbose_name = _("Secondary colour")


@site_preferences_registry.register
class Logo(FilePreference):
    """Logo of your AlekSIS instance."""

    section = theme
    field_class = ImageField
    name = "logo"
    verbose_name = _("Logo")


@site_preferences_registry.register
class Favicon(FilePreference):
    """Favicon of your AlekSIS instance."""

    section = theme
    field_class = ImageField
    name = "favicon"
    verbose_name = _("Favicon")


@site_preferences_registry.register
class PWAIcon(FilePreference):
    """PWA-Icon"""

    section = theme
    field_class = ImageField
    name = "pwa_icon"
    verbose_name = _("PWA-Icon")


@site_preferences_registry.register
class MailOutName(StringPreference):
    """Mail out name"""

    section = mail
    name = "name"
    default = "AlekSIS"
    required = False
    verbose_name = _("Mail out name")


@site_preferences_registry.register
class MailOut(StringPreference):
    """Mail out address"""

    section = mail
    name = "address"
    default = settings.DEFAULT_FROM_EMAIL
    required = False
    verbose_name = _("Mail out address")
    field_class = EmailField


@site_preferences_registry.register
class PrivacyURL(StringPreference):
    """Link to privacy policy"""

    section = footer
    name = "privacy_url"
    default = ""
    required = False
    verbose_name = _("Link to privacy policy")
    field_class = URLField


@site_preferences_registry.register
class ImprintURL(StringPreference):
    """Link to imprint"""

    section = footer
    name = "imprint_url"
    default = ""
    required = False
    verbose_name = _("Link to imprint")
    field_class = URLField


@person_preferences_registry.register
class AdressingNameFormat(ChoicePreference):
    """User preference for adressing name format."""

    section = notification
    name = "addressing_name_format"
    default = "first_last"
    required = False
    verbose_name = _("Name format for addressing")
    choices = (
        ("first_last", "John Doe"),
        ("last_fist", "Doe, John"),
    )


@person_preferences_registry.register
class NotificationChannels(ChoicePreference):
    """User preference for notification channels."""

    # FIXME should be a MultipleChoicePreference
    section = notification
    name = "channels"
    default = "email"
    required = False
    verbose_name = _("Channels to use for notifications")
    choices = get_notification_choices_lazy()


@site_preferences_registry.register
class PrimaryGroupPattern(StringPreference):
    """Regular expression to match primary group."""

    section = account
    name = "primary_group_pattern"
    default = ""
    required = False
    verbose_name = _("Regular expression to match primary group, e.g. '^Class .*'")


@site_preferences_registry.register
class PrimaryGroupField(ChoicePreference):
    """Field on person to match primary group against."""

    section = account
    name = "primary_group_field"
    default = "name"
    required = False
    verbose_name = _("Field on person to match primary group against")

    def get_choices(self):
        return Person.syncable_fields_choices()


@site_preferences_registry.register
class SchoolName(StringPreference):
    """Display name of the school."""

    section = school
    name = "name"
    default = ""
    required = False
    verbose_name = _("Display name of the school")


@site_preferences_registry.register
class SchoolNameOfficial(StringPreference):
    """Official name of the school, e.g. as given by supervisory authority."""

    section = school
    name = "name_official"
    default = ""
    required = False
    verbose_name = _("Official name of the school, e.g. as given by supervisory authority")


@site_preferences_registry.register
class AuthenticationBackends(MultipleChoicePreference):
    section = auth
    name = "backends"
    default = None
    verbose_name = _("Enabled custom authentication backends")
    field_attribute = {"initial": []}

    def get_choices(self):
        return [(b, b) for b in settings.CUSTOM_AUTHENTICATION_BACKENDS]


@site_preferences_registry.register
class AvailableLanguages(MultipleChoicePreference):
    section = internationalisation
    name = "languages"
    default = [code[0] for code in settings.LANGUAGES]
    widget = SelectMultiple
    verbose_name = _("Available languages")
    field_attribute = {"initial": []}
    choices = settings.LANGUAGES
