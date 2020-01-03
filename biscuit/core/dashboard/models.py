import datetime

from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from mailer import send_mail_with_template


class Activity(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=500)

    app = models.CharField(max_length=100)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Notification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    link = models.URLField(blank=True)

    app = models.CharField(max_length=100)

    read = models.BooleanField(default=False)
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

