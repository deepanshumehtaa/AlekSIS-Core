from datetime import date, datetime
from typing import Iterable, List, Optional, Sequence, Union

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import QuerySet
from django.forms.widgets import Media
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

import jsonstore
from dynamic_preferences.models import PerInstancePreferenceModel
from image_cropping import ImageCropField, ImageRatioField
from phonenumber_field.modelfields import PhoneNumberField
from polymorphic.models import PolymorphicModel

from .mixins import ExtensibleModel, PureDjangoModel
from .tasks import send_notification
from .util.core_helpers import get_site_preferences, now_tomorrow
from .util.model_helpers import ICONS

FIELD_CHOICES = (
    ("BooleanField", _("Boolean (Yes/No)")),
    ("CharField", _("Text (one line)")),
    ("DateField", _("Date")),
    ("DateTimeField", _("Date and time")),
    ("DecimalField", _("Decimal number")),
    ("EmailField", _("E-mail address")),
    ("IntegerField", _("Integer")),
    ("GenericIPAddressField", _("IP address")),
    ("NullBooleanField", _("Boolean or empty (Yes/No/Neither)")),
    ("TextField", _("Text (multi-line)")),
    ("TimeField", _("Time")),
    ("URLField", _("URL / Link")),
)


class Person(ExtensibleModel):
    """
    A model describing any person related to a school, including, but not
    limited to, students, teachers and guardians (parents).
    """

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        permissions = (
            ("view_address", _("Can view address")),
            ("view_contact_details", _("Can view contact details")),
            ("view_photo", _("Can view photo")),
            ("view_person_groups", _("Can view persons groups")),
            ("view_personal_details", _("Can view personal details")),
        )

    icon_ = "person"

    SEX_CHOICES = [("f", _("female")), ("m", _("male"))]

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="person",
        verbose_name=_("Linked user"),
    )
    is_active = models.BooleanField(verbose_name=_("Is person active?"), default=True)

    first_name = models.CharField(verbose_name=_("First name"), max_length=255)
    last_name = models.CharField(verbose_name=_("Last name"), max_length=255)
    additional_name = models.CharField(
        verbose_name=_("Additional name(s)"), max_length=255, blank=True
    )

    short_name = models.CharField(
        verbose_name=_("Short name"), max_length=255, blank=True, null=True, unique=True
    )

    street = models.CharField(verbose_name=_("Street"), max_length=255, blank=True)
    housenumber = models.CharField(verbose_name=_("Street number"), max_length=255, blank=True)
    postal_code = models.CharField(verbose_name=_("Postal code"), max_length=255, blank=True)
    place = models.CharField(verbose_name=_("Place"), max_length=255, blank=True)

    phone_number = PhoneNumberField(verbose_name=_("Home phone"), blank=True)
    mobile_number = PhoneNumberField(verbose_name=_("Mobile phone"), blank=True)

    email = models.EmailField(verbose_name=_("E-mail address"), blank=True)

    date_of_birth = models.DateField(verbose_name=_("Date of birth"), blank=True, null=True)
    sex = models.CharField(verbose_name=_("Sex"), max_length=1, choices=SEX_CHOICES, blank=True)

    photo = ImageCropField(verbose_name=_("Photo"), blank=True, null=True)
    photo_cropping = ImageRatioField("photo", "600x800", size_warning=True)

    guardians = models.ManyToManyField(
        "self",
        verbose_name=_("Guardians / Parents"),
        symmetrical=False,
        related_name="children",
        blank=True,
    )

    primary_group = models.ForeignKey(
        "Group", models.SET_NULL, null=True, blank=True, verbose_name=_("Primary group")
    )

    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)

    def get_absolute_url(self) -> str:
        return reverse("person_by_id", args=[self.id])

    @property
    def primary_group_short_name(self) -> Optional[str]:
        """Returns the short_name field of the primary group related object."""
        if self.primary_group:
            return self.primary_group.short_name

    @primary_group_short_name.setter
    def primary_group_short_name(self, value: str) -> None:
        """
        Sets the primary group related object by a short name.

        It uses the first existing group
        with this short name it can find, creating one
        if it can't find one.
        """
        group, created = Group.objects.get_or_create(short_name=value, defaults={"name": value})
        self.primary_group = group

    @property
    def full_name(self) -> str:
        """Full name of person in last name, first name order."""
        return f"{self.last_name}, {self.first_name}"

    @property
    def adressing_name(self) -> str:
        """Full name of person in format configured for addressing."""
        if get_site_preferences()["notification__addressing_name_format"] == "last_first":
            return f"{self.last_name}, {self.first_name}"
        elif get_site_preferences()["notification__addressing_name_format"] == "first_last":
            return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        """Age of the person at current time."""
        return self.age_at(timezone.datetime.now().date())

    def age_at(self, today):
        """Age of the person at a given date and time."""
        years = today.year - self.date_of_birth.year
        if self.date_of_birth.month > today.month or (
            self.date_of_birth.month == today.month and self.date_of_birth.day > today.day
        ):
            years -= 1
        return years

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Synchronise user fields to linked User object to keep it up to date
        if self.user:
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.email = self.email
            self.user.save()

        # Save all related groups once to keep synchronisation with Django
        for group in self.member_of.union(self.owner_of.all()).all():
            group.save()

        # Select a primary group if none is set
        self.auto_select_primary_group()

    def __str__(self) -> str:
        return self.full_name

    @classmethod
    def maintain_default_data(cls):
        # Ensure we have an admin user
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            admin = User.objects.create_superuser(
                username="admin", email="root@example.com", password="admin"
            )
            admin.save()

    def auto_select_primary_group(
        self, pattern: Optional[str] = None, field: Optional[str] = None, force: bool = False
    ) -> None:
        """Auto-select the primary group among the groups the person is member of.

        Uses either the pattern passed as argument, or the pattern configured system-wide.

        Does not do anything if either no pattern is defined or the user already has
        a primary group, unless force is True.
        """
        pattern = pattern or get_site_preferences()["account__primary_group_pattern"]
        field = field or get_site_preferences()["account__primary_group_field"]

        if pattern:
            if force or not self.primary_group:
                self.primary_group = self.member_of.filter(**{f"{field}__regex": pattern}).first()


class DummyPerson(Person):
    """A dummy person that is not stored into the database.

    Used to temporarily inject a Person object into a User.
    """

    class Meta:
        managed = False
        proxy = True

    is_dummy = True

    def save(self, *args, **kwargs):
        # Do nothing, not even call Model's save(), so this is never persisted
        pass


class AdditionalField(ExtensibleModel):
    """An additional field that can be linked to a group."""

    title = models.CharField(verbose_name=_("Title of field"), max_length=255)
    field_type = models.CharField(
        verbose_name=_("Type of field"), choices=FIELD_CHOICES, max_length=50
    )

    class Meta:
        verbose_name = _("Addtitional field for groups")
        verbose_name_plural = _("Addtitional fields for groups")


class Group(ExtensibleModel):
    """
    Any kind of group of persons in a school, including, but not limited
    classes, clubs, and the like.
    """

    class Meta:
        ordering = ["short_name", "name"]
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
        permissions = (("assign_child_groups_to_groups", _("Can assign child groups to groups")),)

    icon_ = "group"

    name = models.CharField(verbose_name=_("Long name"), max_length=255, unique=True)
    short_name = models.CharField(
        verbose_name=_("Short name"), max_length=255, unique=True, blank=True, null=True
    )

    members = models.ManyToManyField(
        "Person",
        related_name="member_of",
        blank=True,
        through="PersonGroupThrough",
        verbose_name=_("Members"),
    )
    owners = models.ManyToManyField(
        "Person", related_name="owner_of", blank=True, verbose_name=_("Owners")
    )

    parent_groups = models.ManyToManyField(
        "self",
        related_name="child_groups",
        symmetrical=False,
        verbose_name=_("Parent groups"),
        blank=True,
    )

    type = models.ForeignKey(
        "GroupType",
        on_delete=models.SET_NULL,
        related_name="type",
        verbose_name=_("Type of group"),
        null=True,
        blank=True,
    )
    additional_fields = models.ManyToManyField(AdditionalField, verbose_name=_("Additional fields"))

    def get_absolute_url(self) -> str:
        return reverse("group_by_id", args=[self.id])

    @property
    def announcement_recipients(self):
        """Flat list of all members and owners to fulfill announcement API contract."""
        return list(self.members.all()) + list(self.owners.all())

    def __str__(self) -> str:
        return f"{self.name} ({self.short_name})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Synchronise group to Django group with same name
        dj_group, _ = DjangoGroup.objects.get_or_create(name=self.name)
        dj_group.user_set.set(
            list(
                self.members.filter(user__isnull=False)
                .values_list("user", flat=True)
                .union(self.owners.filter(user__isnull=False).values_list("user", flat=True))
            )
        )
        dj_group.save()


class PersonGroupThrough(ExtensibleModel):
    """Through table for many-to-many relationship of group members.

    It does not have any fields on its own; these are generated upon instantiation
    by inspecting the additional fields selected for the linked group.
    """

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.group.additional_fields:
            field_class = getattr(jsonstore, field.field_type)
            field_name = slugify(field.title).replace("-", "_")
            field_instance = field_class(verbose_name=field.title)
            setattr(self, field_name, field_instance)


class Activity(ExtensibleModel):
    """Activity of a user to trace some actions done in AlekSIS in displayable form."""

    user = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="activities", verbose_name=_("User")
    )

    title = models.CharField(max_length=150, verbose_name=_("Title"))
    description = models.TextField(max_length=500, verbose_name=_("Description"))

    app = models.CharField(max_length=100, verbose_name=_("Application"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")


class Notification(ExtensibleModel):
    """Notification to submit to a user."""

    sender = models.CharField(max_length=100, verbose_name=_("Sender"))
    recipient = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Recipient"),
    )

    title = models.CharField(max_length=150, verbose_name=_("Title"))
    description = models.TextField(max_length=500, verbose_name=_("Description"))
    link = models.URLField(blank=True, verbose_name=_("Link"))

    read = models.BooleanField(default=False, verbose_name=_("Read"))
    sent = models.BooleanField(default=False, verbose_name=_("Sent"))

    def __str__(self):
        return str(self.title)

    def save(self, **kwargs):
        super().save(**kwargs)
        if not self.sent:
            send_notification(self.pk, resend=True)
        self.sent = True
        super().save(**kwargs)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")


class AnnouncementQuerySet(models.QuerySet):
    """Queryset for announcements providing time-based utility functions."""

    def relevant_for(self, obj: Union[models.Model, models.QuerySet]) -> models.QuerySet:
        """
        Get a QuerySet with all announcements relevant for a certain Model (e.g. a Group)
        or a set of models in a QuerySet.
        """
        if isinstance(obj, models.QuerySet):
            ct = ContentType.objects.get_for_model(obj.model)
            pks = list(obj.values_list("pk", flat=True))
        else:
            ct = ContentType.objects.get_for_model(obj)
            pks = [obj.pk]

        return self.filter(recipients__content_type=ct, recipients__recipient_id__in=pks)

    def at_time(self, when: Optional[datetime] = None) -> models.QuerySet:
        """Get all announcements at a certain time."""
        when = when or timezone.datetime.now()

        # Get announcements by time
        announcements = self.filter(valid_from__lte=when, valid_until__gte=when)

        return announcements

    def on_date(self, when: Optional[date] = None) -> models.QuerySet:
        """Get all announcements at a certain date."""
        when = when or timezone.datetime.now().date()

        # Get announcements by time
        announcements = self.filter(valid_from__date__lte=when, valid_until__date__gte=when)

        return announcements

    def within_days(self, start: date, stop: date) -> models.QuerySet:
        """Get all announcements valid for a set of days."""
        # Get announcements
        announcements = self.filter(valid_from__date__lte=stop, valid_until__date__gte=start)

        return announcements

    def for_person(self, person: Person) -> List:
        """Get all announcements for one person."""
        # Filter by person
        announcements_for_person = []
        for announcement in self:
            if person in announcement.recipient_persons:
                announcements_for_person.append(announcement)

        return announcements_for_person


class Announcement(ExtensibleModel):
    """
    Persistent announcement to display to groups or persons in various places during a
    specific time range.
    """

    objects = models.Manager.from_queryset(AnnouncementQuerySet)()

    title = models.CharField(max_length=150, verbose_name=_("Title"))
    description = models.TextField(max_length=500, verbose_name=_("Description"), blank=True)
    link = models.URLField(blank=True, verbose_name=_("Link to detailed view"))

    valid_from = models.DateTimeField(
        verbose_name=_("Date and time from when to show"), default=timezone.datetime.now
    )
    valid_until = models.DateTimeField(
        verbose_name=_("Date and time until when to show"), default=now_tomorrow,
    )

    @property
    def recipient_persons(self) -> Sequence[Person]:
        """Return a list of Persons this announcement is relevant for."""
        persons = []
        for recipient in self.recipients.all():
            persons += recipient.persons
        return persons

    def get_recipients_for_model(self, obj: Union[models.Model]) -> Sequence[models.Model]:
        """
        Get all recipients for this announcement
        with a special content type (provided through model)
        """
        ct = ContentType.objects.get_for_model(obj)
        return [r.recipient for r in self.recipients.filter(content_type=ct)]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Announcement")
        verbose_name_plural = _("Announcements")


class AnnouncementRecipient(ExtensibleModel):
    """
    Generalisation of a recipient for an announcement, used to wrap arbitrary
    objects that can receive announcements.

    Contract: Objects to serve as recipient have a property announcement_recipients
    returning a flat list of Person objects.
    """

    announcement = models.ForeignKey(
        Announcement, on_delete=models.CASCADE, related_name="recipients"
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    recipient_id = models.PositiveIntegerField()
    recipient = GenericForeignKey("content_type", "recipient_id")

    @property
    def persons(self) -> Sequence[Person]:
        """Return a list of Persons selected by this recipient object.

        If the recipient is a Person, return that object. If not, it returns the list
        from the announcement_recipients field on the target model.
        """
        if isinstance(self.recipient, Person):
            return [self.recipient]
        else:
            return getattr(self.recipient, "announcement_recipients", [])

    def __str__(self):
        return str(self.recipient)

    class Meta:
        verbose_name = _("Announcement recipient")
        verbose_name_plural = _("Announcement recipients")


class DashboardWidget(PolymorphicModel, PureDjangoModel):
    """Base class for dashboard widgets on the index page.

    To implement a widget, add a model that subclasses DashboardWidget, sets the template
    and implements the get_context method to return a dictionary to be passed as context
    to the template.

    If your widget does not add any database fields, you should mark it as a proxy model.

    You can provide a Media meta class with custom JS and CSS files which
    will be added to html head.  For further information on media definition
    see https://docs.djangoproject.com/en/3.0/topics/forms/media/

    Example::

      from django.forms.widgets import Media

      from aleksis.core.models import DashboardWidget

      class MyWidget(DhasboardWIdget):
          template = "myapp/widget.html"

          def get_context(self):
              context = {"some_content": "foo"}
              return context

          class Meta:
              proxy = True

          media = Media(css={
                  'all': ('pretty.css',)
              },
              js=('animations.js', 'actions.js')
          )
    """

    @staticmethod
    def get_media(widgets: Union[QuerySet, Iterable]):
        """Return all media required to render the selected widgets."""
        media = Media()
        for widget in widgets:
            media = media + widget.media
        return media

    template = None
    media = Media()

    title = models.CharField(max_length=150, verbose_name=_("Widget Title"))
    active = models.BooleanField(blank=True, verbose_name=_("Activate Widget"))

    def get_context(self):
        """Get the context dictionary to pass to the widget template."""
        raise NotImplementedError("A widget subclass needs to implement the get_context method.")

    def get_template(self):
        """
        Get the template to render the widget with. Defaults to the template attribute,
        but can be overridden to allow more complex template generation scenarios.
        """
        return self.template

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Dashboard Widget")
        verbose_name_plural = _("Dashboard Widgets")


class CustomMenu(ExtensibleModel):
    """A custom menu to display in the footer."""

    name = models.CharField(max_length=100, verbose_name=_("Menu ID"), unique=True)

    def __str__(self):
        return self.name if self.name != "" else self.id

    @classmethod
    def get_default(cls, name):
        """Get a menu by name or create if it does not exist."""
        menu, _ = cls.objects.get_or_create(name=name)
        return menu

    class Meta:
        verbose_name = _("Custom menu")
        verbose_name_plural = _("Custom menus")


class CustomMenuItem(ExtensibleModel):
    """Single item in a custom menu."""

    menu = models.ForeignKey(
        CustomMenu, models.CASCADE, verbose_name=_("Menu"), related_name="items"
    )
    name = models.CharField(max_length=150, verbose_name=_("Name"))
    url = models.URLField(verbose_name=_("Link"))
    icon = models.CharField(
        max_length=50, blank=True, null=True, choices=ICONS, verbose_name=_("Icon")
    )

    def __str__(self):
        return f"[{self.menu}] {self.name}"

    class Meta:
        verbose_name = _("Custom menu item")
        verbose_name_plural = _("Custom menu items")


class GroupType(ExtensibleModel):
    """
    Descriptive type of a group; used to tag groups and for apps to distinguish
    how to display or handle a certain group.
    """

    name = models.CharField(verbose_name=_("Title of type"), max_length=50)
    description = models.CharField(verbose_name=_("Description"), max_length=500)

    class Meta:
        verbose_name = _("Group type")
        verbose_name_plural = _("Group types")


class GlobalPermissions(ExtensibleModel):
    """Container for global permissions."""

    class Meta:
        managed = False
        permissions = (
            ("view_system_status", _("Can view system status")),
            ("link_persons_accounts", _("Can link persons to accounts")),
            ("manage_data", _("Can manage data")),
            ("impersonate", _("Can impersonate")),
            ("search", _("Can use search")),
            ("change_site_preferences", _("Can change site preferences")),
            ("change_person_preferences", _("Can change person preferences")),
            ("change_group_preferences", _("Can change group preferences")),
        )


class SitePreferenceModel(PerInstancePreferenceModel, PureDjangoModel):
    """Preference model to hold pereferences valid for a site."""

    instance = models.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta:
        app_label = "core"


class PersonPreferenceModel(PerInstancePreferenceModel, PureDjangoModel):
    """Preference model to hold pereferences valid for a person."""

    instance = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        app_label = "core"


class GroupPreferenceModel(PerInstancePreferenceModel, PureDjangoModel):
    """Preference model to hold pereferences valid for members of a group."""

    instance = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        app_label = "core"
