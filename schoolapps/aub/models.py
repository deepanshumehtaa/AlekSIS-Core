from django.db import models
from datetime import datetime

lessons = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9)
)


class Aub(models.Model):
    # Time
    from_date = models.DateField()
    to_date = models.DateField()

    from_lesson = models.DateField(choices=lessons)
    to_lesson = models.DateField(choices=lessons)

    # Information
    description = models.TextField()

    # Meta
    created_by =
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title
