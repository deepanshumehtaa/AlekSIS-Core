from django.db import models

# Create your models here.
from utils.helper import path_and_rename


class Menu(models.Model):
    calendar_week = models.IntegerField(verbose_name="KW")
    year = models.IntegerField(verbose_name="Jahr")
    pdf = models.FileField(upload_to=path_and_rename, verbose_name="PDF")

    class Meta:
        unique_together = ("calendar_week", "year")
        verbose_name = "Speiseplan"
        verbose_name_plural = "Speisepläne"

    def __str__(self):
        return "KW {}/{}".format(self.calendar_week, self.year)
