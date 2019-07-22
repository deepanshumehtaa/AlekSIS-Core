from django import template

register = template.Library()


@register.filter
def get_dict(value, arg):
    return value[arg]
