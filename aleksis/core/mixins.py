from datetime import datetime
from typing import Any, Callable, Optional

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet

from easyaudit.models import CRUDEvent
from jsonstore.fields import JSONField, JSONFieldMixin


class CRUDMixin(models.Model):
    class Meta:
        abstract = True

    @property
    def crud_events(self) -> QuerySet:
        """Get all CRUD events connected to this object from easyaudit."""

        content_type = ContentType.objects.get_for_model(self)

        return CRUDEvent.objects.filter(
            object_id=self.pk, content_type=content_type
        ).select_related("user")


class ExtensibleModel(CRUDMixin):
    """ Base model for all objects in AlekSIS apps

    This base model ensures all objects in AlekSIS apps fulfill the
    following properties:

     * crud_events property to retrieve easyaudit's CRUD event log
     * created_at and updated_at properties based n CRUD events
     * Allow injection of fields and code from AlekSIS apps to extend
       model functionality.

    Injection of fields and code
    ============================

    After all apps have been loaded, the code in the `model_extensions` module
    in every app is executed. All code that shall be injected into a model goes there.

    :Example:

    .. code-block:: python

       from datetime import date, timedelta

       from jsonstore import CharField

       from aleksis.core.models import Person

       @Person.property
       def is_cool(self) -> bool:
           return True

       @Person.property
       def age(self) -> timedelta:
           return self.date_of_birth - date.today()

       Person.field(shirt_size=CharField())

    For a more advanced example, using features from the ORM, see AlekSIS-App-Chronos
    and AlekSIS-App-Alsijil.

    :Date: 2019-11-07
    :Authors:
        - Dominik George <dominik.george@teckids.org>
    """

    @property
    def created_at(self) -> Optional[datetime]:
        """ Determine creation timestamp from CRUD log """

        event = self.crud_events.filter(event_type=CRUDEvent.CREATE).latest("datetime")
        if event:
            return event.datetime

    @property
    def updated_at(self) -> Optional[datetime]:
        """ Determine last timestamp from CRUD log """

        event = self.crud_events.latest("datetime")
        if event:
            return event.datetime

    extended_data = JSONField(default=dict, editable=False)

    @classmethod
    def _safe_add(cls, obj: Any, name: Optional[str]) -> None:
        # Decide the name for the attribute
        if name is None:
            prop_name = obj.__name__
        else:
            if name.isidentifier():
                prop_name = name
            else:
                raise ValueError("%s is not a valid name." % name)

        # Verify that attribute name does not clash with other names in the class
        if hasattr(cls, prop_name):
            raise ValueError("%s already used." % prop_name)

        # Let Django's model magic add the attribute if we got here
        cls.add_to_class(name, obj)

    @classmethod
    def property(cls, func: Callable[[], Any], name: Optional[str] = None) -> None:
        """ Adds the passed callable as a property. """

        cls._safe_add(property(func), func.__name__)

    @classmethod
    def method(cls, func: Callable[[], Any], name: Optional[str] = None) -> None:
        """ Adds the passed callable as a method. """

        cls._safe_add(func, func.__name__)

    @classmethod
    def field(cls, **kwargs) -> None:
        """ Adds the passed jsonstore field. Must be one of the fields in
        django-jsonstore.

        Accepts exactly one keyword argument, with the name being the desired
        model field name and the value the field instance.
        """

        # Force kwargs to be exactly one argument
        if len(kwargs) != 1:
            raise TypeError("field() takes 1 keyword argument but %d were given" % len(kwargs))
        name, field = kwargs.popitem()

        # Force the field to be one of the jsonstore fields
        if JSONFieldMixin not in field.__class__.__mro__:
            raise TypeError("Only jsonstore fields can be added to models.")

        # Force use of the one JSONField defined in this mixin
        field.json_field_name = "extended_data"

        cls._safe_add(field, name)

    class Meta:
        abstract = True
