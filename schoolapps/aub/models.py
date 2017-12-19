from django.db import models
from datetime import datetime


class Aub(models.Model):
    title = models.CharField(max_length=200)
    teacher_id = models.IntegerField(choices=[(x, x) for x in range(1, 32)])
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title
