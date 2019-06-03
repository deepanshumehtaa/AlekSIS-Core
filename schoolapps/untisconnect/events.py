from .drive import drive
from .api_helper import untis_date_to_date, date_to_untis_date
from .api import row_by_row_helper, run_all
from . import models

#########
# EVENT #
#########

class Event(object):
    def __init__(self):
        self.filled = None
        self.text = None
        self.teachers = []
        self.classes  = []
        self.rooms    = []
        self.absences = []
        self.from_date = None
        self.to_date = None
        self.from_lesson = None
        self.to_lesson = None
        self.is_whole_day = None

    def create(self, db_obj):
        """0~0~19~0~1859~0,0~0~65~0~1860~0,0~0~21~0~1861~0,0~0~3~0~1862~0"""
        self.filled = True
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
                teacher_id = int(element[0])
                obj = drive["teachers"][teacher_id]
                self.teachers.append(obj)

            if element[3] != "0" and element[3] != "":
                self.rooms.append(element[3])

            if element[4] != "0" and element[4] != "":
                self.absences.append(element[4])

        self.text = db_obj.text
        self.from_date = untis_date_to_date(db_obj.datefrom)
        self.to_date = untis_date_to_date(db_obj.dateto)
        self.from_lesson = db_obj.lessonfrom
        self.to_lesson = db_obj.lessonto
        self.is_whole_day = self.from_lesson == 1 and self.to_lesson >= settings.TIMETABLE_HEIGHT


def get_all_events_by_date(date):
    d_i = int(date_to_untis_date(date))
    db_rows = run_all(models.Event.objects.filter(dateto__gte=d_i, datefrom__lte=d_i, deleted=0), filter_term=False)
    return row_by_row_helper(db_rows, Event)
