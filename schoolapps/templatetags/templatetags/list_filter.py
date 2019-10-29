from django import template

register = template.Library()


def as_list(obj):
    """list()"""
    return list(obj)


register.filter("as_list", as_list)
