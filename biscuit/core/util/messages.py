import logging

from django.contrib import messages


def add_message(request, level, message):
    if request:
        return messages.add_message(request, level, message)
    else:
        return logging.getLogger(__name__).log(level, message)


def debug(request, message):
    return add_message(request, messages.DEBUG, message)


def info(request, message):
    return add_message(request, messages.INFO, message)


def success(request, message):
    return add_message(request, messages.SUCCESS, message)


def warning(request, message):
    return add_message(request, messages.WARNING, message)


def error(request, message):
    return add_message(request, messages.ERROR, message)
