from django.db import models

from .util.core_helpers import get_current_school


class SchoolRelatedManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        school = get_current_school()

        if school:
            return qs.filter(school=school)
        else:
            return qs.none()

    def create(self, *args, **kwargs):
        if 'school' not in kwargs:
            kwargs['school'] = get_current_school()

        return super().create(*args, **kwargs)


class SchoolRelated(models.Model):
    class Meta:
        abstract = True

    objects = SchoolRelatedManager()

    school = models.ForeignKey('core.School', on_delete=models.CASCADE)
