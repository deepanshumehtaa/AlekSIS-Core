import logging

from django.contrib import messages


def add_message(request, level, message, **kwargs):
    if request:
        return messages.add_message(request, level, message, **kwargs)
    else:
        return logging.getLogger(__name__).log(level, message)


def debug(request, message, **kwargs):
    return add_message(request, messages.DEBUG, message, **kwargs)


def info(request, message, **kwargs):
    return add_message(request, messages.INFO, message, **kwargs)


def success(request, message, **kwargs):
    return add_message(request, messages.SUCCESS, message, **kwargs)


def warning(request, message, **kwargs):
    return add_message(request, messages.WARNING, message, **kwargs)


def error(request, message, **kwargs):
    return add_message(request, messages.ERROR, message, **kwargs)
