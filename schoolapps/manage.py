#!/usr/bin/env python3
import os
import sys

sys.path = ["/srv/sites/school-apps/env/lib/python3.5/site-packages/"] + sys.path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schoolapps.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    execute_from_command_line(sys.argv)
