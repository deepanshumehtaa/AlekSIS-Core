"""Management utilities for an AlekSIS installation."""

import os
import sys

from django.core.management import execute_from_command_line


def aleksis_cmd():
    """Run django-admin command with correct settings path."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aleksis.core.settings")
    execute_from_command_line(sys.argv)
