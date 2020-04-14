from datetime import date, datetime
from typing import Optional, Iterable, Union, Sequence, List

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet
from django.forms.widgets import Media
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from image_cropping import ImageCropField, ImageRatioField
from phonenumber_field.modelfields import PhoneNumberField
from polymorphic.models import PolymorphicModel

from .mixins import ExtensibleModel, PureDjangoModel
from .tasks import send_notification
from .util.core_helpers import now_tomorrow
from .util.model_helpers import ICONS

from constance import config


class School(ExtensibleModel):
    """A school that will have many other objects linked to it.
    AlekSIS has multi-tenant support by linking all objects to a school,
    and limiting all features to objects related to the same school as the
    currently logged-in user.
    """

    name = models.CharField(verbose_name=_("Name"), max_length=255)
    name_official = models.CharField(
        verbose_name=_("Official name"),
        max_length=255,
        help_text=_("Official name of the school, e.g. as given by supervisory authority"),
    )

    logo = ImageCropField(verbose_name=_("School logo"), blank=True, null=True)
    logo_cropping = ImageRatioField("logo", "600x600", size_warning=True)

    @classmethod
    def get_default(cls):
        return cls.objects.first()

    @property
    def current_term(self):
        return SchoolTerm.objects.get(current=True)

    class Meta:
        ordering = ["name", "name_official"]
        verbose_name = _("School")
        verbose_name_plural = _("Schools")


class SchoolTerm(ExtensibleModel):
    """ Information about a term (limited time frame) that data can
    be linked to.
    """

    caption = models.CharField(verbose_name=_("Visible caption of the term"), max_length=255)

    date_start = models.DateField(verbose_name=_("Effective start date of term"), null=True)
    date_end = models.DateField(verbose_name=_("Effective end date of term"), null=True)

    current = models.NullBooleanField(default=None, unique=True)

    def save(self, *args, **kwargs):
        if self.current is False:
            self.current = None
        super().save(*args, **kwargs)

    @classmethod
    def maintain_default_data(cls):
        if not cls.objects.filter(current=True).exists():
            if cls.objects.exists():
                term = cls.objects.latest('date_start')
                term.current=True
                term.save()
            else:
                cls.objects.create(date_start=date.today(), current=True)

    class Meta:
        verbose_name = _("School term")
        verbose_name_plural = _("School terms")


class Person(ExtensibleModel):
    """ A model describing any person related to a school, including, but not
    limited to, students, teachers and guardians (parents).
    """

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    SEX_CHOICES = [("f", _("female")), ("m", _("male"))]

    user = models.OneToOneField(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True, related_name="person"
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
    longtitude = models.FloatField(verbose_name=_("Longtitude"), blank=True, null=True)
    latitude = models.FloatField(verbose_name=_("Latitude"), blank=True, null=True)

    phone_number = PhoneNumberField(verbose_name=_("Home phone"), blank=True)
    mobile_number = PhoneNumberField(verbose_name=_("Mobile phone"), blank=True)

    email = models.EmailField(verbose_name=_("E-mail address"), blank=True)

    date_of_birth = models.DateField(verbose_name=_("Date of birth"), blank=True, null=True)
    sex = models.CharField(verbose_name=_("Sex"), max_length=1, choices=SEX_CHOICES, blank=True)

    photo = ImageCropField(verbose_name=_("Photo"), blank=True, null=True)
    photo_cropping = ImageRatioField("photo", "600x800", size_warning=True)

    guardians = models.ManyToManyField(
        "self", verbose_name=_("Guardians / Parents"), symmetrical=False, related_name="children", blank=True
    )

    primary_group = models.ForeignKey("Group", models.SET_NULL, null=True, blank=True)

    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)

    @property
    def primary_group_short_name(self) -> Optional[str]:
        """ Returns the short_name field of the primary
        group related object.
        """

        if self.primary_group:
            return self.primary_group.short_name

    @primary_group_short_name.setter
    def primary_group_short_name(self, value: str) -> None:
        """ Sets the primary group related object by
        a short name. It uses the first existing group
        with this short name it can find, creating one
        if it can't find one.
        """

        group, created = Group.objects.get_or_create(short_name=value, defaults={"name": value})
        self.primary_group = group

    @property
    def full_name(self) -> str:
        return f"{self.last_name}, {self.first_name}"

    @property
    def full_address(self) -> str:
        return f"{self.street} {self.housenumber}, {self.postal_code} {self.place}"

    @property
    def adressing_name(self) -> str:
        if config.ADRESSING_NAME_FORMAT == "dutch":
            return f"{self.last_name} {self.first_name}"
        elif config.ADRESSING_NAME_FORMAT == "english":
            return f"{self.last_name}, {self.first_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        return self.age_at(timezone.datetime.now().date())

    def age_at(self, today):
        years = today.year - self.date_of_birth.year
        if (self.date_of_birth.month > today.month
            or (self.date_of_birth.month == today.month
                and self.date_of_birth.day > today.day)):
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
        for group in self.member_of.union(self.owner_of).all():
            group.save()

        # Update geolocation
        if self.full_address:
            update_geolocation(self)

        self.auto_select_primary_group()

    def __str__(self) -> str:
        return self.full_name

    @classmethod
    def maintain_default_data(cls):
        # First, ensure we have an admin user
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='root@example.com',
                password='admin'
            )
            admin.save()

            # Ensure this admin user has a person linked to it
            person = Person(user=admin)
            person.save()

    def auto_select_primary_group(self, pattern: Optional[str] = None, force: bool = False) -> None:
        """ Auto-select the primary group among the groups the person is member of

        Uses either the pattern passed as argument, or the pattern configured system-wide.

        Does not do anything if either no pattern is defined or the user already has
        a primary group, unless force is True.
        """

        pattern = pattern or config.PRIMARY_GROUP_PATTERN

        if pattern:
            if force or not self.primary_group:
                self.primary_group = self.member_of.filter(name__regex=pattern).first()


class Group(ExtensibleModel):
    """Any kind of group of persons in a school, including, but not limited
    classes, clubs, and the like.
    """

    class Meta:
        ordering = ["short_name", "name"]
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    name = models.CharField(verbose_name=_("Long name of group"), max_length=255, unique=True)
    short_name = models.CharField(verbose_name=_("Short name of group"), max_length=255, unique=True, blank=True, null=True)

    members = models.ManyToManyField("Person", related_name="member_of", blank=True)
    owners = models.ManyToManyField("Person", related_name="owner_of", blank=True)

    parent_groups = models.ManyToManyField(
        "self",
        related_name="child_groups",
        symmetrical=False,
        verbose_name=_("Parent groups"),
        blank=True,
    )

    type = models.ForeignKey("GroupType", on_delete=models.CASCADE, related_name="type", verbose_name=_("Type of group"), null=True, blank=True)

    @property
    def announcement_recipients(self):
        return list(self.members.all()) + list(self.owners.all())

    def __str__(self) -> str:
        return "%s (%s)" % (self.name, self.short_name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Synchronise group to Django group with same name
        dj_group, _ = DjangoGroup.objects.get_or_create(name=self.name)
        dj_group.user_set.set(
            list(
                self.members.values_list("user", flat=True).union(self.owners.values_list("user", flat=True))
            )
        )
        dj_group.save()


class Activity(ExtensibleModel):
    user = models.ForeignKey("Person", on_delete=models.CASCADE, related_name="activities")

    title = models.CharField(max_length=150, verbose_name=_("Title"))
    description = models.TextField(max_length=500, verbose_name=_("Description"))

    app = models.CharField(max_length=100, verbose_name=_("Application"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")


class Notification(ExtensibleModel):
    sender = models.CharField(max_length=100, verbose_name=_("Sender"))
    recipient = models.ForeignKey("Person", on_delete=models.CASCADE, related_name="notifications")

    title = models.CharField(max_length=150, verbose_name=_("Title"))
    description = models.TextField(max_length=500, verbose_name=_("Description"))
    link = models.URLField(blank=True, verbose_name=_("Link"))

    read = models.BooleanField(default=False, verbose_name=_("Read"))
    sent = models.BooleanField(default=False, verbose_name=_("Sent"))

    def __str__(self):
        return str(self.title)

    def save(self, **kwargs):
        if not self.sent:
            send_notification(self.pk, resend=True)
        self.sent = True
        super().save(**kwargs)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")


class AnnouncementQuerySet(models.QuerySet):
    def relevant_for(self, obj: Union[models.Model, models.QuerySet]) -> models.QuerySet:
        """ Get a QuerySet with all announcements relevant for a certain Model (e.g. a Group)
        or a set of models in a QuerySet.
        """

        if isinstance(obj, models.QuerySet):
            ct = ContentType.objects.get_for_model(obj.model)
            pks = list(obj.values_list('pk', flat=True))
        else:
            ct = ContentType.objects.get_for_model(obj)
            pks = [obj.pk]

        return self.filter(recipients__content_type=ct, recipients__recipient_id__in=pks)

    def at_time(self,when: Optional[datetime] = None ) -> models.QuerySet:
        """ Get all announcements at a certain time """

        when = when or timezone.datetime.now()

        # Get announcements by time
        announcements = self.filter(valid_from__lte=when, valid_until__gte=when)

        return announcements

    def on_date(self, when: Optional[date] = None) -> models.QuerySet:
        """ Get all announcements at a certain date """

        when = when or timezone.datetime.now().date()

        # Get announcements by time
        announcements = self.filter(valid_from__date__lte=when, valid_until__date__gte=when)

        return announcements

    def within_days(self, start: date, stop: date) -> models.QuerySet:
        """ Get all announcements valid for a set of days """

        # Get announcements
        announcements = self.filter(valid_from__date__lte=stop, valid_until__date__gte=start)

        return announcements

    def for_person(self, person: Person) -> List:
        """ Get all announcements for one person """

        # Filter by person
        announcements_for_person = []
        for announcement in self:
            if person in announcement.recipient_persons:
                announcements_for_person.append(announcement)

        return announcements_for_person


class Announcement(ExtensibleModel):
    objects = models.Manager.from_queryset(AnnouncementQuerySet)()

    title = models.CharField(max_length=150, verbose_name=_("Title"))
    description = models.TextField(max_length=500, verbose_name=_("Description"), blank=True)
    link = models.URLField(blank=True, verbose_name=_("Link"))

    valid_from = models.DateTimeField(
        verbose_name=_("Date and time from when to show"), default=timezone.datetime.now
    )
    valid_until = models.DateTimeField(
        verbose_name=_("Date and time until when to show"),
        default=now_tomorrow,
    )

    @property
    def recipient_persons(self) -> Sequence[Person]:
        """ Return a list of Persons this announcement is relevant for """

        persons = []
        for recipient in self.recipients.all():
            persons += recipient.persons
        return persons

    def get_recipients_for_model(self, obj: Union[models.Model]) -> Sequence[models.Model]:
        """ Get all recipients for this announcement with a special content type (provided through model) """

        ct = ContentType.objects.get_for_model(obj)
        return [r.recipient for r in self.recipients.filter(content_type=ct)]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Announcement")
        verbose_name_plural = _("Announcements")


class AnnouncementRecipient(ExtensibleModel):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="recipients")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    recipient_id = models.PositiveIntegerField()
    recipient = GenericForeignKey("content_type", "recipient_id")

    @property
    def persons(self) -> Sequence[Person]:
        """ Return a list of Persons selected by this recipient object

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
    """ Base class for dashboard widgets on the index page

    To implement a widget, add a model that subclasses DashboardWidget, sets the template
    and implements the get_context method to return a dictionary to be passed as context
    to the template.

    If your widget does not add any database fields, you should mark it as a proxy model.

    You can provide a Media meta class with custom JS and CSS files which will be added to html head.
    For further information on media definition see https://docs.djangoproject.com/en/3.0/topics/forms/media/

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
        """ Return all media required to render the selected widgets. """

        media = Media()
        for widget in widgets:
            media = media + widget.media
        return media

    template = None
    media = Media()

    title = models.CharField(max_length=150, verbose_name=_("Widget Title"))
    active = models.BooleanField(blank=True, verbose_name=_("Activate Widget"))

    def get_context(self):
        raise NotImplementedError("A widget subclass needs to implement the get_context method.")

    def get_template(self):
        return self.template

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Dashboard Widget")
        verbose_name_plural = _("Dashboard Widgets")


class CustomMenu(ExtensibleModel):
    id = models.CharField(max_length=100, verbose_name=_("Menu ID"), primary_key=True)
    name = models.CharField(max_length=150, verbose_name=_("Menu name"))

    def __str__(self):
        return self.name if self.name != "" else self.id

    @classmethod
    def maintain_default_data(cls):
        menus = ["footer"]
        for menu in menus:
            cls.get_default(menu)

    @classmethod
    def get_default(cls, name):
        menu, _ = cls.objects.get_or_create(id=name, defaults={"name": name})
        return menu

    class Meta:
        verbose_name = _("Custom menu")
        verbose_name_plural = _("Custom menus")


class CustomMenuItem(ExtensibleModel):
    menu = models.ForeignKey(
        CustomMenu, models.CASCADE, verbose_name=_("Menu"), related_name="items"
    )
    name = models.CharField(max_length=150, verbose_name=_("Name"))
    url = models.URLField(verbose_name=_("Link"))
    icon = models.CharField(
        max_length=50, blank=True, null=True, choices=ICONS, verbose_name=_("Icon")
    )

    def __str__(self):
        return "[{}] {}".format(self.menu, self.name)

    class Meta:
        verbose_name = _("Custom menu item")
        verbose_name_plural = _("Custom menu items")

class GroupType(ExtensibleModel):
    name = models.CharField(verbose_name=_("Title of type"), max_length=50)
    description = models.CharField(verbose_name=_("Description"), max_length=500)

    class Meta:
        verbose_name = _("Group type")
        verbose_name_plural = _("Group types")
