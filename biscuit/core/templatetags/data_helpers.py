from typing import Dict, Any

from django import template

register = template.Library()


@register.filter
def get_dict(value: Dict[Any, Any], arg: Any) -> Any:
    return value.get(arg, None)
