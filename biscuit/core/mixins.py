from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet

from easyaudit.models import CRUDEvent

from .util.core_helpers import get_current_school


class SchoolRelated(models.Model):
    class Meta:
        abstract = True

#    objects = SchoolRelatedManager()

    school = models.ForeignKey(
        'core.School', on_delete=models.CASCADE, default=get_current_school)

    @property
    def crud_events(self) -> QuerySet:
        """Get all CRUD events connected to this object from easyaudit."""

        content_type = ContentType.objects.get_for_model(self)

        return CRUDEvent.objects.filter(
            object_id=self.pk,
            content_type=content_type
        ).select_related(
            'user'
        )
