from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

SEX_CHOICES = [
    ('f', _('female')),
    ('m', _('male'))
]


class Person(AbstractUser):
    additional_name = models.CharField(max_length=30)

    street = models.CharField(max_length=30)
    housenumber = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=5)
    place = models.CharField(max_length=30)

    phone_number = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=30)

    date_of_birth = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    photo = models.ImageField()

    import_ref = models.CharField(max_length=64)

    guardians = models.ManyToManyField(
        'self', symmetrical=False, related_name='children')

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)
