from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class Person(models.Model):
    SEX_CHOICES = [
        ('f', _('female')),
        ('m', _('male'))
    ]

    is_active = models.BooleanField(
        verbose_name=_('Is person active?'), default=False)

    first_name = models.CharField(verbose_name=_('First name'), max_length=30)
    last_name = models.CharField(verbose_name=_('Last name'), max_length=30)
    additional_name = models.CharField(verbose_name=_(
        'Additional name(s)'), max_length=30, blank=True)

    short_name = models.CharField(verbose_name=_(
        'Short name'), max_length=5, blank=True)

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

    photo = models.ImageField(verbose_name=_('Photo'), blank=True, null=True)

    import_ref = models.CharField(verbose_name=_(
        'Reference ID of import source'), max_length=64, blank=True, editable=False)

    guardians = models.ManyToManyField('self', verbose_name=_('Guardians / Parents'),
                                       symmetrical=False, related_name='children')

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


class Group(models.Model):
    name = models.CharField(verbose_name=_(
        'Long name of group'), max_length=30)
    short_name = models.CharField(verbose_name=_(
        'Short name of group'), max_length=8)

    members = models.ManyToManyField('Person', related_name='member_of')
    owners = models.ManyToManyField('Person', related_name='owner_of')

    def __str__(self):
        return '%s (%s)' % (self.name, self.short_name)
