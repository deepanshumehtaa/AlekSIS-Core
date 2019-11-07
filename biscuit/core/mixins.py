from typing import Any, Callable, Optional

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet

from easyaudit.models import CRUDEvent

from .util.core_helpers import get_current_school


class ExtensibleModel(object):
    """ Mixin that adds class methods for glrofied monkey-patching. """

    @classmethod
    def _safe_add(cls, obj: Any, name: Optional[str]) -> None:
        # Decide the name for the attribute
        if name is None:
            prop_name = obj.__name__
        else:
            if name.isidentifier():
                prop_name = name
            else:
                raise ValueError('%s is not a valid name.' % name)

        # Verify that property name does not clash with other names in the class
        if hasattr(cls, prop_name):
            raise ValueError('%s already used.' % prop_name)

        # Add function wrapped in property decorator if we got here
        setattr(cls, prop_name, obj)

    @classmethod
    def property(cls, func: Callable[[], Any], name: Optional[str] = None) -> None:
        """ Adds the passed callable as a property. """

        cls._safe_add(property(func), func.__name__)

    @classmethod
    def method(cls, func: Callable[[], Any], name: Optional[str] = None) -> None:
        """ Adds the passed callable as a method. """

        cls._safe_add(func, func.__name__)


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
