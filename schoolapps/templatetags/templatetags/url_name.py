from django.urls import resolve
from django import template

register = template.Library()

def get_url_name(request): # Only one argument.
    """Gets url_name"""
    return resolve(request.path_info).url_name

register.filter("url_name", get_url_name)