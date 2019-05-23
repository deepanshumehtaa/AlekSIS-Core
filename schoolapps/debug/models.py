import os
import traceback

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
        """
        :return: Were all operations in this group successful?
        """
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
                                    verbose_name="Dateiname zur Logdatei (falls nicht Log-Text)", blank=True)
    log_text = models.TextField(verbose_name="Log-Text (falls nicht Datei)", blank=True)
    updated_at = models.DateTimeField(blank=False, default=timezone.now, verbose_name="Aktualisierungszeitpunkt")

    class Meta:
        verbose_name = "Debug-Log"
        verbose_name_plural = "Debug-Logs"

    def __str__(self):
        return self.name or self.id

    def get_file_content(self):
        """
        :return: The log text (file or DB)
        """
        if self.filename:
            print(self.filename)
            f = open(os.path.join(DEBUG_LOG_DIR, self.filename), "r")
            content = f.read()
            f.close()
            return content
        elif self.log_text:
            return self.log_text
        else:
            return ""

    def is_successful(self):
        """
        :return: Was the last operation successful?
        """
        return self.return_code == 0


def get_log_group_by_id(id):
    """
    Get a log group from DB by given id
    :param id: ID of log group
    :return:
    """
    p, _ = DebugLogGroup.objects.get_or_create(id=id)
    return p


def register_log_with_filename(id, group_id, filename, return_code):
    """
    Register a operation in debugging tool with a log file

    :param id: id of operation
    :param group_id: id of group
    :param filename: file path (based on latex dir)
    :param return_code: UNIX return code
    """
    p, _ = DebugLog.objects.get_or_create(id=id)
    group = get_log_group_by_id(group_id)
    p.group = group
    p.return_code = return_code
    p.filename = filename
    p.updated_at = timezone.now()
    p.save()


def register_return_0(id, group_id):
    """
    Register a operation in debugging tool with an return code of 0 (success) and no log text/log file

    :param id: id of operation
    :param group_id: id of group
    """
    p, _ = DebugLog.objects.get_or_create(id=id)
    group = get_log_group_by_id(group_id)
    p.group = group
    p.return_code = 0
    p.log_text = ""
    p.updated_at = timezone.now()
    p.save()


def register_traceback(id, group_id):
    """
    Register a operation in debugging tool with an return code of 1 (error) and a log text

    :param id: id of operation
    :param group_id: id of group
    """
    msg = traceback.format_exc()
    p, _ = DebugLog.objects.get_or_create(id=id)
    group = get_log_group_by_id(group_id)
    p.group = group
    p.return_code = 1
    p.log_text = msg
    p.updated_at = timezone.now()
    p.save()
