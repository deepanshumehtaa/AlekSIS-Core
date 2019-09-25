import datetime

from django.core.management import BaseCommand
from django.utils import timezone

from timetable.views import get_next_weekday_with_time, get_calendar_week
from untisconnect.drive import build_drive, TYPE_TEACHER, TYPE_CLASS, TYPE_ROOM
from untisconnect.parse import parse
from untisconnect.plan import get_plan


class Command(BaseCommand):
    help = 'Refresh all var caches'

    def start(self, s):
        self.stdout.write(s)

    def finish(self):
        self.stdout.write(self.style.SUCCESS('  Erledigt.'))

    def handle(self, *args, **options):
        self.start("Aktualisiere Drive ... ")
        drive = build_drive(force_update=True)
        self.finish()

        self.start("Aktualisiered Lessons ...")
        parse(force_update=True)
        self.finish()

        self.start("Aktualisiere Pläne ...")

        days = []
        days.append(get_next_weekday_with_time(timezone.now(), timezone.now().time()))
        days.append(get_next_weekday_with_time(days[0], datetime.time(0)))
        print(days)

        types = [
            (TYPE_TEACHER, "teachers"),
            (TYPE_CLASS, "classes"),
            (TYPE_ROOM, "rooms")
        ]
        for type_id, type_key in types:
            self.start(type_key)

            for id, obj in drive[type_key].items():
                self.start("  " + obj.name if obj.name is not None else "")
                self.start("     Regelplan")
                get_plan(type_id, id, force_update=True)
                for day in days:
                    calendar_week = day.isocalendar()[1]
                    monday_of_week = get_calendar_week(calendar_week, day.year)["first_day"]

                    self.start("    " + str(monday_of_week))
                    get_plan(type_id, id, smart=True, monday_of_week=monday_of_week, force_update=True)
