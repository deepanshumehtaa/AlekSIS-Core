from django.db import models
from datetime import datetime
from teachers.models import Teacher, get_default_teacher

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
    teacher = models.ForeignKey(Teacher,
                                related_name='aubs',
                                on_delete=models.SET(get_default_teacher()),
                                default=get_default_teacher())
    description = models.TextField()

    # Meta
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title
