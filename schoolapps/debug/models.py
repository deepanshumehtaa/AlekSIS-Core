import os

from django.db import models
from django.utils import timezone

from schoolapps.settings import BASE_DIR


class DebugLogGroup(models.Model):
    # Meta
    id = models.CharField(primary_key=True, blank=False, max_length=100, verbose_name="ID")
    name = models.CharField(blank=False, max_length=200, verbose_name="Name")
    desc_as_pre = models.CharField(blank=True, max_length=250, verbose_name="Beschreibung, dargestellt als HTML-PRE")

    class Meta:
        verbose_name = "Debug-Log-Gruppe"
        verbose_name_plural = "Debug-Log-Gruppen"

    def __str__(self):
        return self.name or self.id

    def is_successful(self):
        successful = True
        for log in self.logs.all():
            if not log.is_successful():
                successful = False
        return successful


DEBUG_LOG_DIR = os.path.join(BASE_DIR, "latex")


class DebugLog(models.Model):
    # Meta
    id = models.CharField(primary_key=True, blank=False, max_length=100, verbose_name="ID")
    name = models.CharField(blank=False, max_length=200, verbose_name="Name")
    group = models.ForeignKey(DebugLogGroup, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                              related_name="logs", verbose_name="Gruppe")  # If null, it wouldn't be displayed

    # Data
    return_code = models.IntegerField(blank=True, null=True, verbose_name="UNIX-Rückgabecode")
    filename = models.FilePathField(path=DEBUG_LOG_DIR, match=".*.log",
                                    verbose_name="Dateiname zur Logdatei")
    updated_at = models.DateTimeField(blank=False, default=timezone.now, verbose_name="Aktualisierungszeitpunkt")

    class Meta:
        verbose_name = "Debug-Log"
        verbose_name_plural = "Debug-Logs"

    def __str__(self):
        return self.name or self.id

    def get_file_content(self):
        if self.filename:
            print(self.filename)
            f = open(os.path.join(DEBUG_LOG_DIR, self.filename), "r")
            content = f.read()
            f.close()
            return content
        else:
            return ""

    def is_successful(self):
        return self.return_code == 0


def get_log_group_by_id(id):
    p, _ = DebugLogGroup.objects.get_or_create(id=id)
    return p


def register_log_with_filename(id, group_id, filename, return_code):
    p, _ = DebugLog.objects.get_or_create(id=id)
    group = get_log_group_by_id(group_id)
    p.group = group
    p.return_code = return_code
    p.filename = filename
    p.updated_at = timezone.now()
    p.save()
