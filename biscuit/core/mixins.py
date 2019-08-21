from django.db import models

from .util.core_helpers import get_current_school


class SchoolRelatedManager(models.Manager):
    def get_queryset(self) -> models.query.QuerySet:
        qs = super().get_queryset()
        school = get_current_school()

        if school:
            return qs.filter(school=school)
        else:
            return qs.none()


class SchoolRelated(models.Model):
    class Meta:
        abstract = True

    objects = SchoolRelatedManager()

    school = models.ForeignKey(
        'core.School', on_delete=models.CASCADE, default=get_current_school)
