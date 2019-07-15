from django.contrib.auth.models import AbstractUser
from django.db import models


class Person(AbstractUser):
    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)
