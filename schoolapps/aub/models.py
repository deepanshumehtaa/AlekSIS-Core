from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def get_default_user():
    user, created = User.objects.get_or_create(username='nouser')
    return user.id


class Status(models.Model):
    name = models.CharField(max_length=100)
    style_classes = models.CharField(max_length=200)

    def __str__(self):
        return self.name


def get_default_status():
    status, created = Status.objects.get_or_create(name='In Bearbeitung 1', style_classes='orange')
    return status.id


class Aub(models.Model):
    # Time
    from_dt = models.DateTimeField(default=timezone.now)
    to_dt = models.DateTimeField(default=timezone.now)

    # Information
    description = models.TextField()
    status = models.ForeignKey(Status, related_name='aubs', on_delete=models.SET(get_default_status()),
                               default=get_default_status())
    # Meta
    created_by = models.ForeignKey(User, related_name='aubs', on_delete=models.SET(get_default_user()),
                                   default=get_default_user())
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description

    class Meta:
        permissions = (
            ('apply_for_aub', 'Apply for a AUB'),
            ('cancel_aub', 'Cancel a AUB'),
            ('allow1_aub', 'First permission'),
            ('allow2_aub', 'Second permission'),
            ('check1_aub', 'Check a AUB'),
            ('check2_aub', 'Check a AUB')
        )
