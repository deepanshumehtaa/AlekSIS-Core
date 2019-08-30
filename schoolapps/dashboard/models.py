import datetime

import dbsettings
from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from mailer import send_mail_with_template


# def get_default_user():
#     User.objects.get_or_create(username='nouser')


# Create your models here.

class Activity(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)

    app = models.CharField(max_length=100)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Notification(models.Model):
    # to = models.ManyToManyField(User, related_name='notifications')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    link = models.URLField(blank=True)

    app = models.CharField(max_length=100)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


def register_notification(user, title, description, app="SchoolApps", link=""):
    print(link)
    n = Notification(user=user, title=title, description=description, app=app, link=link)

    n.save()
    context = {
        'notification': n
    }
    send_mail_with_template(title, [user.email], "mail/notification.txt", "mail/notification.html", context)


class Cache(models.Model):
    id = models.CharField(max_length=200, unique=True, primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=200, verbose_name="Name")
    expiration_time = models.IntegerField(default=20, verbose_name="Ablaufzeit")
    last_time_updated = models.DateTimeField(blank=True, null=True,
                                             verbose_name="Letzter Aktualisierungszeitpunkt des Caches")
    site_cache = models.BooleanField(default=False, verbose_name="Seitencache?")

    class Meta:
        verbose_name = "Cacheeintrag"
        verbose_name_plural = "Cacheeinträge"

    def __str__(self):
        return self.name or self.id

    def update(self, new_value):
        if not self.site_cache:
            self.last_time_updated = timezone.now()
            cache.set(self.id, new_value, self.expiration_time)
            self.save()

    def get(self):
        if not self.site_cache:
            return cache.get(self.id, False)
        else:
            return None

    def is_expired(self):
        if not self.expiration_time:
            return True
        delta = datetime.timedelta(seconds=self.expiration_time)
        print(self.last_time_updated)
        print(self.last_time_updated + delta)
        print(timezone.now())
        return timezone.now() > self.last_time_updated + delta
