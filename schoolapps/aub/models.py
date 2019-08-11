from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date


# def get_default_user():
#     user, created = User.objects.get_or_create(username='nouser')
#     return user.id


class Status:
    def __init__(self, name, style_class):
        self.name = name
        self.style_class = style_class

    def __str__(self):
        return self.name


status_list = [
    Status(name='In Bearbeitung 1', style_class='orange'),
    Status(name='In Bearbeitung 2', style_class='yellow'),
    Status(name='Genehmigt', style_class='green'),
    Status(name='Abgelehnt', style_class='red'),
]

status_choices = [(x, val.name) for x, val in enumerate(status_list)]


class Aub(models.Model):
    # Time
    from_date = models.DateField(default=date.today, verbose_name="Startdatum")
    from_time = models.TimeField(default=timezone.now, verbose_name="Startzeit")
    to_date = models.DateField(default=date.today, verbose_name="Enddatum")
    to_time = models.TimeField(default=timezone.now, verbose_name="Endzeit")

    # Information
    description = models.TextField()
    status = models.IntegerField(default=0, choices=status_choices, verbose_name="Status")

    # Meta
    created_by = models.ForeignKey(User, related_name='aubs', on_delete=models.SET_NULL
                                   , verbose_name="Erstellt von", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Erstellungszeitpunkt")

    def getStatus(self):
        print(self.status, self.created_by, self.id)
        return status_list[self.status]

    def __str__(self):
        return self.description

    class Meta:
        permissions = (
            ('apply_for_aub', 'Apply for a AUB'),
            ('cancel_aub', 'Cancel a AUB'),
            ('allow1_aub', 'First permission'),
            ('allow2_aub', 'Second permission'),
            ('check1_aub', 'Check a AUB'),
            ('check2_aub', 'Check a AUB'),
            ('view_archive', 'View AUB archive'),
        )

        verbose_name = "AUB"
        verbose_name_plural = "AUBs"
