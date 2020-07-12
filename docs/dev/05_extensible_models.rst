Extensible models
=================

In AlekSIS you can use ``ExtensibleModels`` to add model fields to other
apps models.

If you want to make your apps models extensible, use the ``ExtensibleModel``
class as parent class of your models.

If you want to extend other apps extensible models, create a new file
``model_extensions.py``::

    from django.utils.translation import gettext_lazy as _

    from jsonstore import CharField

    from aleksis.core.models import Group

    Group.field(example=CharField(verbose_name=_("Example field"), blank=True))
