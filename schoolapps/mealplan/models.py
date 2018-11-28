from django.db import models


# Create your models here.
class MealPlan(models.Model):
    calendar_week = models.IntegerField()
    year = models.IntegerField()
    pdf = models.FileField(upload_to="mealplan/%Y/")
