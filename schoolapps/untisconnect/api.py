from django.conf import settings

from untisconnect.api_helper import get_term_by_ids, run_using, untis_date_to_date, date_to_untis_date
from . import models
from timetable.settings import untis_settings

TYPE_TEACHER = 0
TYPE_ROOM = 1
TYPE_CLASS = 2

from datetime import date

def run_all(obj, filter_term=True):
    return run_default_filter(run_using(obj).all(), filter_term=filter_term)


def run_one(obj, filter_term=True):
    return run_default_filter(run_using(obj), filter_term=filter_term)


def run_default_filter(obj, filter_term=True):
    # Get term by settings in db
    TERM_ID = untis_settings.term
    SCHOOLYEAR_ID = untis_settings.school_year  # 20172018
    TERM = get_term_by_ids(TERM_ID, SCHOOLYEAR_ID)
    SCHOOL_ID = TERM.school_id  # 705103
    VERSION_ID = TERM.version_id  # 1

    if filter_term:
        return obj.filter(school_id=SCHOOL_ID, schoolyear_id=SCHOOLYEAR_ID, version_id=VERSION_ID, term_id=TERM_ID)
    else:
        return obj.filter(school_id=SCHOOL_ID, schoolyear_id=SCHOOLYEAR_ID, version_id=VERSION_ID)


def row_by_row_helper(db_rows, obj):
    out_rows = []
    for db_row in db_rows:
        o = obj()
        o.create(db_row)
        out_rows.append(o)
    return out_rows


def row_by_row(db_ref, obj, filter_term=True):
    db_rows = run_all(db_ref.objects, filter_term=filter_term)
    return row_by_row_helper(db_rows, obj)


def one_by_id(db_ref, obj):
    # print(db_ref)
    if db_ref is not None:
        o = obj()
        o.create(db_ref)
        return o
    else:
        return None


###########
# TEACHER #
###########
class Teacher(object):
    def __init__(self):
        self.filled = False
        self.id = None
        self.shortcode = None
        self.first_name = None
        self.name = None
        self.full_name = None

    def __str__(self):
        if self.filled:
            return (self.first_name or "") + " " + (self.name or "")
        else:
            return "Unbekannt"

    def create(self, db_obj):
        self.filled = True
        self.id = db_obj.teacher_id
        self.shortcode = db_obj.name
        self.name = db_obj.longname
        self.first_name = db_obj.firstname


def get_all_teachers():
    teachers = row_by_row(models.Teacher, Teacher)
    return teachers


def get_teacher_by_id(id):
    teacher = run_one(models.Teacher.objects).get(teacher_id=id)
    return one_by_id(teacher, Teacher)


def get_teacher_by_shortcode(shortcode):
    shortcode = shortcode.upper()
    teacher = run_one(models.Teacher.objects).get(name__icontains=shortcode)
    return one_by_id(teacher, Teacher)


#########
# CLASS #
#########
class Class(object):
    def __init__(self):
        self.filled = False
        self.id = None
        self.name = None
        self.text1 = None
        self.text2 = None
        self.room = None

    def __str__(self):
        if self.filled:
            return self.name or "Unbekannt"
        else:
            return "Unbekannt"

    def create(self, db_obj):
        self.filled = True
        self.id = db_obj.class_id
        self.name = db_obj.name
        self.text1 = db_obj.longname
        self.text2 = db_obj.text
        # print(db_obj.room_id)
        if db_obj.room_id != 0:
            #   print("RAUM")
            self.room = get_room_by_id(db_obj.room_id)


def get_all_classes():
    classes = row_by_row(models.Class, Class)
    return classes


def get_class_by_id(id):
    _class = run_one(models.Class.objects).get(class_id=id)
    return one_by_id(_class, Class)


def get_class_by_name(name):
    name = name[0].upper() + name[1:]
    _class = run_one(models.Class.objects).filter(name__icontains=name).all()[0]
    return one_by_id(_class, Class)


def format_classes(classes):
    """
    Formats a list of Class objects to a combined string

    example return: "9abcd" for classes 9a, 9b, 9c and 9d

    :param classes: Class list
    :return: combined string
    """
    classes_as_dict = {}

    for _class in classes:
        step = _class.name[:-1]
        part = _class.name[-1:]
        if step not in classes_as_dict.keys():
            classes_as_dict[step] = [part]
        else:
            classes_as_dict[step].append(part)

    out = []
    for key, value in classes_as_dict.items():
        out.append(key + "".join(value))
    return ", ".join(out)


########
# ROOM #
########
class Room(object):
    def __init__(self):
        self.filled = False
        self.id = None
        self.shortcode = None
        self.name = None

    def __str__(self):
        if self.filled:
            return self.name or "Unbekannt"
        else:
            return "Unbekannt"

    def create(self, db_obj):
        self.filled = True
        self.id = db_obj.room_id
        self.shortcode = db_obj.name
        self.name = db_obj.longname


def get_all_rooms():
    db_rooms = row_by_row(models.Room, Room)
    return db_rooms


def get_room_by_id(id):
    room = run_one(models.Room.objects).get(room_id=id)
    return one_by_id(room, Room)


########
# CORRIDOR #
########
class Corridor(object):
    def __init__(self):
        self.filled = False
        self.id = None
        self.name = None

    def __str__(self):
        if self.filled:
            return self.name or "Unbekannt"
        else:
            return "Unbekannt"

    def create(self, db_obj):
        self.filled = True
        self.id = db_obj.corridor_id
        self.name = db_obj.name


def get_all_corridors():
    corridors = row_by_row(models.Corridor, Corridor, filter_term=False)
    return corridors


def get_corridor_by_id(id):
    # print(id)
    corridor = run_one(models.Corridor.objects, filter_term=False).get(corridor_id=id)
    return one_by_id(corridor, Corridor)


###########
# SUBJECT #
###########
class Subject(object):
    def __init__(self):
        self.filled = False
        self.id = None
        self.shortcode = None
        self.name = None
        self.color = None
        self.hex_color = None

    def create(self, db_obj):
        self.filled = True
        self.id = db_obj.subject_id
        self.shortcode = db_obj.name
        self.name = db_obj.longname
        self.color = db_obj.backcolor

        # Convert UNTIS number to HEX
        hex_bgr = str(hex(db_obj.backcolor)).replace("0x", "")

        # Add beginning zeros if len < 6
        if len(hex_bgr) < 6:
            hex_bgr = "0" * (6 - len(hex_bgr)) + hex_bgr

        # Change BGR to RGB
        hex_rgb = hex_bgr[4:6] + hex_bgr[2:4] + hex_bgr[0:2]

        # Add html #
        self.hex_color = "#" + hex_rgb


def get_all_subjects():
    db_rooms = row_by_row(models.Subjects, Subject, filter_term=False)
    return db_rooms


def get_subject_by_id(id):
    subject = run_one(models.Subjects.objects, filter_term=False).get(subject_id=id)
    return one_by_id(subject, Subject)


class Absence(object):
    def __init__(self):
        self.filled = None
        self.teacher = None
        self.room = None
        self.type = TYPE_TEACHER
        self.from_date = None
        self.to_date = None
        self.from_lesson = None
        self.to_lesson = None
        self.is_whole_day = None

    def create(self, db_obj):
        self.filled = True
        # print(db_obj.ida)
        # print(db_obj.typea)
        if db_obj.typea == 101:
            self.type = TYPE_TEACHER
        elif db_obj.typea == 100:
            self.type = TYPE_CLASS
        elif db_obj.typea == 102:
            self.type = TYPE_ROOM

        if self.type == TYPE_TEACHER:
            # print("IDA", db_obj.ida)
            self.teacher = get_teacher_by_id(db_obj.ida)
        else:
            self.room = get_room_by_id(db_obj.ida)
        self.from_date = untis_date_to_date(db_obj.datefrom)
        self.to_date = untis_date_to_date(db_obj.dateto)
        self.from_lesson = db_obj.lessonfrom
        self.to_lesson = db_obj.lessonto
        self.is_whole_day = self.from_lesson == 1 and self.to_lesson >= settings.TIMETABLE_HEIGHT


def get_all_absences_by_date(date):
    d_i = int(date_to_untis_date(date))
    db_rows = run_all(models.Absence.objects.filter(dateto__gte=d_i, datefrom__lte=d_i, deleted=0), filter_term=False)
    return row_by_row_helper(db_rows, Absence)


def get_absence_by_id(id):
    absence = run_one(models.Absence.objects, filter_term=False).get(absence_id=id)
    return one_by_id(absence, Absence)


#########
# EVENT #
#########

class Event(object):
    def __init__(self):
        self.filled = None
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
        event_parsed = db_obj.eventelement1.split(",")
        elements = []
        for element in event_parsed:
            elements.append(element.split("~"))

        for element in elements:
            if element[0] != "0" and element[0] != "":
                self.classes.append(element[0])

            if element[2] != "0" and element[2] != "":
                self.teachers.append(element[2])

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


##########
# LESSON #
##########
def get_raw_lessons():
    return run_all(models.Lesson.objects)

###########
# HOLIDAY #
###########
class Holiday(object):
    def __init__(self):
        self.filled = False
        self.name = None
        self.datefrom = None
        self.dateto = None

    def __str__(self):
        if self.filled:
            return self.name or "Unbekannt"
        else:
            return "Unbekannt"

    def create(self, db_obj):
        self.filled = True
        self.name = db_obj.name
        self.datefrom = db_obj.datefrom
        self.dateto = db_obj.dateto


def get_today_holidays(date):
    #db_holidays = row_by_row(models.Holiday, Holiday)
    d_i = int(date_to_untis_date(date))
    db_rows = run_all(models.Holiday.objects.filter(dateto__gte=d_i, datefrom__lte=d_i), filter_term=False)
    return row_by_row_helper(db_rows, Holiday)