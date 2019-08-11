from django.conf import settings

from schoolapps.settings import TIMETABLE_HEIGHT
from .drive import drive
from .api_helper import untis_date_to_date, date_to_untis_date
from .api import row_by_row_helper, run_all, get_absence_by_id
from . import models


#########
# EVENT #
#########

class Event(object):
    def __init__(self):
        self.filled = None
        self.id = None
        self.text = None
        self.teachers = []
        self.classes = []
        self.rooms = []
        self.absences = []
        self.from_date = None
        self.to_date = None
        self.from_lesson = None
        self.to_lesson = None
        self.is_whole_day = None

    def create(self, db_obj):
        """0~0~19~0~1859~0,0~0~65~0~1860~0,0~0~21~0~1861~0,0~0~3~0~1862~0"""
        self.filled = True
        self.id = db_obj.event_id

        event_parsed = db_obj.eventelement1.split(",")
        elements = []
        for element in event_parsed:
            elements.append(element.split("~"))

        for element in elements:
            if element[0] != "0" and element[0] != "":
                class_id = int(element[0])
                obj = drive["classes"][class_id]
                self.classes.append(obj)

            if element[2] != "0" and element[2] != "":
                teacher_id = int(element[2])
                obj = drive["teachers"][teacher_id]
                self.teachers.append(obj)

            if element[3] != "0" and element[3] != "":
                room_id = int(element[3])
                obj = drive["rooms"][room_id]
                self.rooms.append(obj)

            if element[4] != "0" and element[4] != "":
                print(element[4])
                try:
                    absence_id = int(element[4])
                    absence = get_absence_by_id(absence_id)
                    self.absences.append(absence)
                except models.Absence.DoesNotExist:
                    pass
        self.text = db_obj.text
        self.from_date = untis_date_to_date(db_obj.datefrom)
        self.to_date = untis_date_to_date(db_obj.dateto)
        self.from_lesson = db_obj.lessonfrom
        self.to_lesson = db_obj.lessonto
        self.is_whole_day = self.from_lesson == 1 and self.to_lesson >= settings.TIMETABLE_HEIGHT


def get_all_events_by_date(date):
    d_i = int(date_to_untis_date(date))
    db_rows = run_all(models.Event.objects.filter(dateto__gte=d_i, datefrom__lte=d_i, deleted=0), filter_term=False)
    rows = row_by_row_helper(db_rows, Event)

    # Remap the lesson numbers matching for the given date
    for i, event in enumerate(rows):
        if event.from_date != event.to_date:
            if event.from_date == date:
                event.to_lesson = TIMETABLE_HEIGHT
            elif event.to_date == date:
                event.from_lesson = 1
            else:
                event.from_lesson = 1
                event.to_lesson = TIMETABLE_HEIGHT

    return rows
