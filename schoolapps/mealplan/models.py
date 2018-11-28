from django.db import models


# Create your models here.
class MealPlan(models.Model):
    calendar_week = models.IntegerField()
    year = models.IntegerField()
    pdf = models.FileField(upload_to="menus/")

    def __str__(self):
        return "KW {}/{}".format(self.calendar_week, self.year)
