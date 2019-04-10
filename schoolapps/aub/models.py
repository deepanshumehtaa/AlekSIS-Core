from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date


def get_default_user():
    user, created = User.objects.get_or_create(username='nouser')
    return user.id


class Status():
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
print("status_list[0].name  :", status_list[0].name)



# def get_default_status():
#     status, created = Status.objects.get_or_create(name='In Bearbeitung 1', style_classes='orange')
#     return status.id
#

class Aub(models.Model):
    # Time
    from_date = models.DateField(default=date.today)
    from_time = models.TimeField(default=timezone.now)
    to_date = models.DateField(default=date.today)
    to_time = models.TimeField(default=timezone.now)

    # Information
    description = models.TextField()
#    status = models.ForeignKey(Status, related_name='aubs', on_delete=models.SET(get_default_status()),
#                               default=get_default_status())
#     status_choices = [(IN_PROCESSING_STATUS.id, IN_PROCESSING_STATUS.name),
#                       (SEMI_ALLOWED_STATUS.id, SEMI_ALLOWED_STATUS.name),
#                       (ALLOWED_STATUS.id, ALLOWED_STATUS.name),
#                       (NOT_ALLOWED_STATUS.id, NOT_ALLOWED_STATUS.name)]
    status = models.IntegerField(default=0)

    # Meta
    created_by = models.ForeignKey(User, related_name='aubs', on_delete=models.SET(get_default_user()),
                                   default=get_default_user())
    created_at = models.DateTimeField(default=timezone.now)

    def getStatus(self):
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
