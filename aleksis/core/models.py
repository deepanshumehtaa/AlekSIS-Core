from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from image_cropping import ImageCropField, ImageRatioField
from phonenumber_field.modelfields import PhoneNumberField

from .mailer import send_mail_with_template
from templated_email import send_templated_mail
from .mixins import ExtensibleModel

from constance import config


class School(models.Model):
    """A school that will have many other objects linked to it.
    AlekSIS has multi-tenant support by linking all objects to a school,
    and limiting all features to objects related to the same school as the
    currently logged-in user.
    """

    name = models.CharField(verbose_name=_("Name"), max_length=30)
    name_official = models.CharField(
        verbose_name=_("Official name"),
        max_length=200,
        help_text=_("Official name of the school, e.g. as given by supervisory authority"),
    )

    logo = ImageCropField(verbose_name=_("School logo"), blank=True, null=True)
    logo_cropping = ImageRatioField("logo", "600x600", size_warning=True)

    @property
    def current_term(self):
        return SchoolTerm.objects.get(current=True)

    class Meta:
        ordering = ["name", "name_official"]
        verbose_name = _("School")
        verbose_name_plural = _("Schools")


class SchoolTerm(models.Model):
    """ Information about a term (limited time frame) that data can
    be linked to.
    """

    caption = models.CharField(verbose_name=_("Visible caption of the term"), max_length=30)

    date_start = models.DateField(verbose_name=_("Effective start date of term"), null=True)
    date_end = models.DateField(verbose_name=_("Effective end date of term"), null=True)

    current = models.NullBooleanField(default=None, unique=True)

    def save(self, *args, **kwargs):
        if self.current is False:
            self.current = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("School term")
        verbose_name_plural = _("School terms")


class Person(models.Model, ExtensibleModel):
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

    first_name = models.CharField(verbose_name=_("First name"), max_length=30)
    last_name = models.CharField(verbose_name=_("Last name"), max_length=30)
    additional_name = models.CharField(
        verbose_name=_("Additional name(s)"), max_length=30, blank=True
    )

    short_name = models.CharField(
        verbose_name=_("Short name"), max_length=5, blank=True, null=True, unique=True
    )

    street = models.CharField(verbose_name=_("Street"), max_length=30, blank=True)
    housenumber = models.CharField(verbose_name=_("Street number"), max_length=10, blank=True)
    postal_code = models.CharField(verbose_name=_("Postal code"), max_length=5, blank=True)
    place = models.CharField(verbose_name=_("Place"), max_length=30, blank=True)

    phone_number = PhoneNumberField(verbose_name=_("Home phone"), blank=True)
    mobile_number = PhoneNumberField(verbose_name=_("Mobile phone"), blank=True)

    email = models.EmailField(verbose_name=_("E-mail address"), blank=True)

    date_of_birth = models.DateField(verbose_name=_("Date of birth"), blank=True, null=True)
    sex = models.CharField(verbose_name=_("Sex"), max_length=1, choices=SEX_CHOICES, blank=True)

    photo = ImageCropField(verbose_name=_("Photo"), blank=True, null=True)
    photo_cropping = ImageRatioField("photo", "600x800", size_warning=True)

    import_ref = models.CharField(
        verbose_name=_("Reference ID of import source"),
        max_length=64,
        blank=True,
        null=True,
        editable=False,
        unique=True,
    )

    guardians = models.ManyToManyField(
        "self", verbose_name=_("Guardians / Parents"), symmetrical=False, related_name="children", blank=True
    )

    primary_group = models.ForeignKey("Group", models.SET_NULL, null=True)

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
        return "%s, %s" % (self.last_name, self.first_name)

    def __str__(self) -> str:
        return self.full_name


class Group(models.Model, ExtensibleModel):
    """Any kind of group of persons in a school, including, but not limited
    classes, clubs, and the like.
    """

    class Meta:
        ordering = ["short_name", "name"]
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    name = models.CharField(verbose_name=_("Long name of group"), max_length=60, unique=True)
    short_name = models.CharField(verbose_name=_("Short name of group"), max_length=16, unique=True)

    members = models.ManyToManyField("Person", related_name="member_of", blank=True)
    owners = models.ManyToManyField("Person", related_name="owner_of", blank=True)

    parent_groups = models.ManyToManyField(
        "self",
        related_name="child_groups",
        symmetrical=False,
        verbose_name=_("Parent groups"),
        blank=True,
    )

    def __str__(self) -> str:
        return "%s (%s)" % (self.name, self.short_name)


class Activity(models.Model):
    user = models.ForeignKey("Person", on_delete=models.CASCADE, related_name="activities")

    title = models.CharField(max_length=150, verbose_name=_("Title"))
    description = models.TextField(max_length=500, verbose_name=_("Description"))

    app = models.CharField(max_length=100, verbose_name=_("Application"))

    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Created at"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")


class Notification(models.Model):
    user = models.ForeignKey("Person", on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=150, verbose_name=_("Title"))
    description = models.TextField(max_length=500, verbose_name=_("Description"))
    link = models.URLField(blank=True, verbose_name=_("Link"))

    app = models.CharField(max_length=100, verbose_name=_("Application"))

    read = models.BooleanField(default=False, verbose_name=_("Read"))
    mailed = models.BooleanField(default=False, verbose_name=_("Mailed"))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Created at"))

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        super().save(**kwargs)

        if not self.mailed:
            context = self.__dict__
            context["notification_user"] = " ".join([self.user.first_name, self.user.last_name])
            send_templated_mail(
                template_name='notification',
                from_email=config.MAIL_OUT,
                recipient_list=[self.user.email],
                context=context,
            )
            self.mailed = True
            super().save(**kwargs)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
