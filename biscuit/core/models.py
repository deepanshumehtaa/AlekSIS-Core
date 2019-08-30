from typing import Optional

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from image_cropping import ImageCropField, ImageRatioField
from phonenumber_field.modelfields import PhoneNumberField

from .mixins import SchoolRelated


class School(models.Model):
    """A school that will have many other objects linked to it.
    BiscuIT has multi-tenant support by linking all objects to a school,
    and limiting all features to objects related to the same school as the
    currently logged-in user.
    """

    name = models.CharField(verbose_name=_('Name'), max_length=30)
    name_official = models.CharField(verbose_name=('Official name'), max_length=200, help_text=_(
        'Official name of the school, e.g. as given by supervisory authority'))


    class Meta:
        ordering = ['name', 'name_official']


class Person(SchoolRelated):
    """ A model describing any person related to a school, including, but not
    limited to, students, teachers and guardians (parents).
    """

    class Meta:
        unique_together = [['school', 'short_name'], ['school', 'import_ref']]
        ordering = ['last_name', 'first_name']

    SEX_CHOICES = [
        ('f', _('female')),
        ('m', _('male'))
    ]

    user = models.OneToOneField(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
        related_name='person')
    is_active = models.BooleanField(
        verbose_name=_('Is person active?'), default=False)

    first_name = models.CharField(verbose_name=_('First name'), max_length=30)
    last_name = models.CharField(verbose_name=_('Last name'), max_length=30)
    additional_name = models.CharField(verbose_name=_(
        'Additional name(s)'), max_length=30, blank=True)

    short_name = models.CharField(verbose_name=_(
        'Short name'), max_length=5, blank=True, null=True)

    street = models.CharField(verbose_name=_(
        'Street'), max_length=30, blank=True)
    housenumber = models.CharField(verbose_name=_(
        'Street number'), max_length=10, blank=True)
    postal_code = models.CharField(verbose_name=_(
        'Postal code'), max_length=5, blank=True)
    place = models.CharField(verbose_name=_(
        'Place'), max_length=30, blank=True)

    phone_number = PhoneNumberField(verbose_name=_('Home phone'), blank=True)
    mobile_number = PhoneNumberField(
        verbose_name=_('Mobile phone'), blank=True)

    email = models.EmailField(verbose_name=_('E-mail address'), blank=True)

    date_of_birth = models.DateField(
        verbose_name=_('Date of birth'), blank=True, null=True)
    sex = models.CharField(verbose_name=_(
        'Sex'), max_length=1, choices=SEX_CHOICES, blank=True)

    photo = ImageCropField(verbose_name=_('Photo'), blank=True, null=True)
    photo_cropping = ImageRatioField('photo', '600x800', size_warning=True)

    import_ref = models.CharField(verbose_name=_(
        'Reference ID of import source'), max_length=64, blank=True, null=True, editable=False)

    guardians = models.ManyToManyField('self', verbose_name=_('Guardians / Parents'),
                                       symmetrical=False, related_name='children')

    primary_group = models.ForeignKey('Group', models.SET_NULL, null=True)

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

        group, created = Group.objects.get_or_create(short_name=value,
                                                     defaults={'name': value})
        self.primary_group = group

    def save(self, *args, **kwargs):
        if self.primary_group:
            if self.primary_group not in self.member_of.all():
                self.member_of.add(self.primary_group)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return '%s, %s' % (self.last_name, self.first_name)


class Group(SchoolRelated):
    """Any kind of group of persons in a school, including, but not limited
    classes, clubs, and the like.
    """

    class Meta:
        unique_together = [['school', 'name'], ['school', 'short_name']]
        ordering = ['short_name', 'name']

    name = models.CharField(verbose_name=_(
        'Long name of group'), max_length=30)
    short_name = models.CharField(verbose_name=_(
        'Short name of group'), max_length=8)

    members = models.ManyToManyField('Person', related_name='member_of')
    owners = models.ManyToManyField('Person', related_name='owner_of')

    def __str__(self) -> str:
        return '%s (%s)' % (self.name, self.short_name)
