import datetime

from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from mailer import send_mail_with_template


class Activity(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)

    app = models.CharField(max_length=100)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Notification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    link = models.URLField(blank=True)

    app = models.CharField(max_length=100)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


def register_notification(user, title, description, app="SchoolApps", link=""):
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
    needed_until = models.DateField(default=None, null=True, verbose_name="Benötigt bis")

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

    def is_expired(self) -> bool:
        """
        Checks whether a cache is expired
        :return: Is cache expired?
        """
        # If cache never was updated it have to
        if self.last_time_updated is None:
            return True

        # Else check if now is bigger than last time updated + expiration time
        delta = datetime.timedelta(seconds=self.expiration_time)
        return timezone.now() > self.last_time_updated + delta

    def is_needed(self) -> bool:
        """
        Checks whether a plan can be deleted
        :return: Is cache needed?
        """
        if self.needed_until is None:
            return True
        elif timezone.now().date() > self.needed_until:
            return False
        else:
            return True

    def delete(self, *args, **kwargs):
        """Overrides model function delete to delete cache entry, too"""
        cache.delete(self.id)
        super(Cache, self).delete(*args, **kwargs)
