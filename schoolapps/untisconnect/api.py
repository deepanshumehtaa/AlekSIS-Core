from . import models

DB_NAME = 'untis'
SCHOOL_ID = 705103
SCHOOLYEAR_ID = 20172018
VERSION_ID = 1
TERM_ID = 8


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


def run_all(obj):
    return run_default_filter(obj.using(DB_NAME).all())


def run_default_filter(obj):
    return obj.filter(school_id=SCHOOL_ID, schoolyear_id=SCHOOLYEAR_ID, version_id=VERSION_ID, term_id=TERM_ID)


def get_all_teachers():
    teachers = []
    db_teachers = run_all(models.Teacher.objects)
    for db_teacher in db_teachers:
        t = Teacher()
        t.create(db_teacher)
        teachers.append(t)
    return teachers
