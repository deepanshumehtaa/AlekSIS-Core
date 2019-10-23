from django import template

import copy as copylib

register = template.Library()


def copy(obj):
    """copy.copy()"""
    return copylib.copy(obj)


def deepcopy(obj):
    """copy.deepcopy()"""
    return copylib.deepcopy(obj)


register.filter("copy", copy)
register.filter("deepcopy", deepcopy)

