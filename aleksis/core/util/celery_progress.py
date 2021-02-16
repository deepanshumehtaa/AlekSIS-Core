from decimal import Decimal
from functools import wraps
from typing import Callable, Union

from celery_progress.backend import PROGRESS_STATE, AbstractProgressRecorder

from ..celery import app


class ProgressRecorder(AbstractProgressRecorder):
    """Track the process of a Celery task and give data to the frontend.

    This recorder provides the functions `set_progress` and `add_message`
    which can be used to track the status of a Celery task.

    How to use
    ----------
    1. Write a function and include tracking methods

    ::

        from django.contrib import messages

        from aleksis.core.util.celery_progress import ProgressRecorder

        @ProgressRecorder.record
        def do_something(recorder: ProgressRecorder, foo, bar, baz=None):
            # ...
            recorder.total = len(list_with_data)

            for i, item in list_with_data:
                # ...
                recorder.set_progress(i + 1)
                # ...

            recorder.add_message(messages.SUCCESS, "All data were imported successfully.")

    2. Track progress in view:

    ::

        def my_view(request):
            context = {}
            # ...
            result = do_something(foo, bar, baz=baz)

            context = {
                "title": _("Progress: Import data"),
                "back_url": reverse("index"),
                "progress": {
                    "task_id": result.task_id,
                    "title": _("Import objects …"),
                    "success": _("The import was done successfully."),
                    "error": _("There was a problem while importing data."),
                },
            }

            # Render progress view
            return render(request, "core/progress.html", context)
    """

    def __init__(self, task):
        self.task = task
        self.messages = []
        self.total = 100
        self.current = 0

    def set_progress(self, current: Union[int, float], **kwargs):
        """Set the current progress in the frontend.

        The progress percentage is automatically calculated in relation to self.total.

        :param current: The number of proceeded items (no percentage)
        """
        self.current = current

        percent = 0
        if self.total > 0:
            percent = (Decimal(current) / Decimal(self.total)) * Decimal(100)
            percent = float(round(percent, 2))

        self.task.update_state(
            state=PROGRESS_STATE,
            meta={
                "current": current,
                "total": self.total,
                "percent": percent,
                "messages": self.messages,
            },
        )

    def add_message(self, level: int, message: str):
        """Show a message in the progress frontend.

        :param level: The message level (default levels from django.contrib.messages)
        :param message: The actual message (should be translated)
        """
        self.messages.append((level, message))
        self.set_progress(self.current)

    @classmethod
    def recorded_task(cls, orig: Callable) -> app.Task:
        """Create a Celery task that receives a ProgressRecorder.

        Returns a Task object with a wrapper that passes the recorder instance
        as the recorder keyword argument.
        """
        @wraps(orig)
        def _inject_recorder(task, *args, **kwargs):
            recorder = ProgressRecorder(task)
            return orig(*args, **kwargs, recorder=recorder)

        return app.task(_inject_recorder, bind=True)
