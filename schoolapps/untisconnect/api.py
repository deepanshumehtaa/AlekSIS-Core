from untisconnect.api_helper import get_term_by_id, run_using
from . import models
from timetable import models as models2


def run_all(obj, filter_term=True):
    return run_default_filter(run_using(obj).all(), filter_term=filter_term)


def run_one(obj, filter_term=True):
    return run_default_filter(run_using(obj), filter_term=filter_term)


def run_default_filter(obj, filter_term=True):
    # Get term by settings in db
    TERM_ID = models2.untis_settings.term
    TERM = get_term_by_id(TERM_ID)
    SCHOOL_ID = TERM.school_id  # 705103
    SCHOOLYEAR_ID = TERM.schoolyear_id  # 20172018
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
    if db_ref != None:
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
        hex_bgr = str(hex(db_obj.backcolor)).replace("0x", "")
        hex_rgb = hex_bgr[4:5] + hex_bgr[2:3] + hex_bgr[0:1]
        self.hex_color = "#" + hex_rgb


def get_all_subjects():
    db_rooms = row_by_row(models.Subjects, Subject, filter_term=False)
    return db_rooms


def get_subject_by_id(id):
    subject = run_one(models.Subjects.objects, filter_term=False).get(subject_id=id)
    return one_by_id(subject, Subject)


##########
# LESSON #
##########
def get_raw_lessons():
    return run_all(models.Lesson.objects)
