from django.db import models

from .util.core_helpers import get_current_school


class SchoolRelated(models.Model):
    class Meta:
        abstract = True

#    objects = SchoolRelatedManager()

    school = models.ForeignKey(
        'core.School', on_delete=models.CASCADE, default=get_current_school)
