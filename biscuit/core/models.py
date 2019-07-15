from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(AbstractUser):
    SEX_CHOICES = [
        ('f', _('female')),
        ('m', _('male'))
    ]

    additional_name = models.CharField(verbose_name=_(
        'Additional name(s)'), max_length=30, blank=True)

    street = models.CharField(verbose_name=_(
        'Street'), max_length=30, blank=True)
    housenumber = models.CharField(verbose_name=_(
        'Street number'), max_length=10, blank=True)
    postal_code = models.CharField(verbose_name=_(
        'Postal code'), max_length=5, blank=True)
    place = models.CharField(verbose_name=_(
        'Place'), max_length=30, blank=True)

    phone_number = models.CharField(verbose_name=_(
        'Home phone'), max_length=30, blank=True)
    mobile_number = models.CharField(verbose_name=_(
        'Mobile phone'), max_length=30, blank=True)

    date_of_birth = models.DateField(
        verbose_name=_('Date of birth'), blank=True)
    sex = models.CharField(verbose_name=_(
        'Sex'), max_length=1, choices=SEX_CHOICES, blank=True)

    photo = models.ImageField(verbose_name=_('Photo'), blank=True)

    import_ref = models.CharField(verbose_name=_(
        'Reference ID of import source'), max_length=64, blank=True, editable=False)

    guardians = models.ManyToManyField('self', verbose_name=_('Guardians / Parents'),
                                       symmetrical=False, related_name='children')

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)
