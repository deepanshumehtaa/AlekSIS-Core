from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def get_default_user():
    User.objects.get_or_create(username='nouser')


# Create your models here.

class Activity(models.Model):
    user = models.ForeignKey(User, models.CASCADE, default=get_default_user())

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)

    app = models.CharField(max_length=100)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
