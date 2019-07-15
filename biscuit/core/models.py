from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(AbstractUser):
    SEX_CHOICES = [
        ('f', _('female')),
        ('m', _('male'))
    ]

    additional_name = models.CharField(max_length=30, blank=True)

    street = models.CharField(max_length=30, blank=True)
    housenumber = models.CharField(max_length=10, blank=True)
    postal_code = models.CharField(max_length=5, blank=True)
    place = models.CharField(max_length=30, blank=True)

    phone_number = models.CharField(max_length=30, blank=True)
    mobile_number = models.CharField(max_length=30, blank=True)

    date_of_birth = models.DateField(blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)

    photo = models.ImageField(blank=True)

    import_ref = models.CharField(max_length=64, blank=True, editable=False)

    guardians = models.ManyToManyField(
        'self', symmetrical=False, related_name='children')

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)
