from django.db import models


class SchoolRelated(models.Model):
    class Meta:
        abstract = True

    school = models.ForeignKey('core.School', on_delete=models.CASCADE)
