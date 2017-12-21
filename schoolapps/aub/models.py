from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

lessons = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9)
)


def get_default_user():
    User.objects.get_or_create(username='nouser')


class Aub(models.Model):
    # Time
    from_date = models.DateField(default=timezone.now)
    to_date = models.DateField(default=timezone.now)

    from_lesson = models.IntegerField(choices=lessons, default=1, blank=True)
    to_lesson = models.IntegerField(choices=lessons, default=1, blank=True)

    from_time = models.TimeField(default=timezone.now)
    to_time = models.TimeField(default=timezone.now)

    # Information
    description = models.TextField()


    # Meta
    created_by = models.ForeignKey(User, related_name='aubs', on_delete=models.SET(get_default_user()),
                                   default=get_default_user())
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description
