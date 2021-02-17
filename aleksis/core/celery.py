import os

from django.db import transaction

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aleksis.core.settings")

app = Celery("aleksis")  # noqa
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


class OnCommitTask(app.Task):
    """Task that is delayed at least until the current transaction commits."""
    def delay(self, *args, **kwargs):
        def _real_delay():
            return super().delay(*args, **kwargs)
        transaction.on_commit(_real_delay)


app.Task = OnCommitTask
