import os
from functools import partial

from django.db import transaction

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aleksis.core.settings")

app = Celery("aleksis")  # noqa
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


def _amqp_send_task_message_on_commit(*args, **kwargs):
    transaction.on_commit(partial(app.amqp.send_task_message, *args, **kwargs))


app.amqp.send_task_message = _amqp_send_task_message_on_commit
