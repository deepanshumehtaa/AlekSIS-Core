from django.db import models

# Create your models here.
from helper import path_and_rename


class MealPlan(models.Model):
    calendar_week = models.IntegerField()
    year = models.IntegerField()
    pdf = models.FileField(upload_to=path_and_rename)

    def __str__(self):
        return "KW {}/{}".format(self.calendar_week, self.year)
