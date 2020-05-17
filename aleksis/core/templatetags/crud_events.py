import json
from typing import Optional, Union

from django.contrib.contenttypes.models import ContentType
from django.template import Library

register = Library()


@register.simple_tag
def verbose_name(app_label: str, model: str, field: Optional[str] = None) -> str:
    """Get a verbose name of a model or a field by app label and model name."""
    ct = ContentType.objects.get(app_label=app_label, model=model).model_class()

    if field:
        # Field
        return ct._meta.get_field(field).verbose_name.title()
    else:
        # Whole model
        return ct._meta.verbose_name.title()


@register.simple_tag
def parse_json(value: Optional[str] = None) -> Union[dict, None]:
    """Template tag for parsing JSON from a string."""
    if not value:
        return None
    return json.loads(value)
