from django.conf import settings
from django.core import management
from django_cron import CronJobBase, Schedule


class Backup(CronJobBase):
    RUN_AT_TIMES = settings.DBBACKUP_CRON_TIMES
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'biscuit.core.Backup'

    def do(self):
        management.call_command('dbbackup', '-z')
        management.call_command('mediabackup' '-z')
