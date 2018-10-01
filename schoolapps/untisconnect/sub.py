from django.utils import timezone

from untisconnect import models
from untisconnect.api import run_default_filter, row_by_row_helper, get_teacher_by_id, get_subject_by_id, \
    get_room_by_id, get_class_by_id
from untisconnect.api_helper import run_using, untis_split_first

DATE_FORMAT = "%Y%m%d"


def untis_date_to_date(untis):
    return timezone.datetime.strptime(str(untis), DATE_FORMAT)


def date_to_untis_date(date):
    return date.strftime(DATE_FORMAT)


class Substitution(object):
    def __init__(self):
        self.filled = False
        self.id = None
        self.lesson_id = None
        self.date = None
        self.lesson = None
        self.type = None
        self.text = None
        self.teacher_old = None
        self.teacher_new = None
        self.subject_old = None
        self.subject_new = None
        self.room_old = None
        self.room_new = None
        self.corridor = None
        self.classes = None

    def __str__(self):
        if self.filled:
            return self.id
        else:
            return "Unbekannt"

    def create(self, db_obj):
        self.filled = True
        self.id = db_obj.substitution_id
        self.lesson_id = db_obj.lesson_idsubst
        self.date = untis_date_to_date(db_obj.date)
        self.lesson = db_obj.lesson
        self.type = list(db_obj.flags)
        self.text = db_obj.text

        # Teacher
        if db_obj.teacher_idlessn != 0:
            self.teacher_old = get_teacher_by_id(db_obj.teacher_idlessn)
        if db_obj.teacher_idsubst != 0:
            self.teacher_new = get_teacher_by_id(db_obj.teacher_idsubst)

        # Subject
        self.subject_old = None
        if db_obj.subject_idsubst != 0:
            self.subject_new = get_subject_by_id(db_obj.subject_idsubst)

        # Room
        self.room_old = None
        if db_obj.room_idsubst != 0:
            self.room_new = get_room_by_id(db_obj.room_idsubst)
        self.corridor = db_obj.corridor_id

        # Classes
        self.classes = []
        class_ids = untis_split_first(db_obj.classids, conv=int)

        for id in class_ids:
            self.classes.append(get_class_by_id(id))


def get_substitutions_by_date():
    subs_raw = run_default_filter(run_using(models.Substitution.objects.filter(date="20180821")), filter_term=False)
    print(subs_raw)

    subs = row_by_row_helper(subs_raw, Substitution)
    print(subs)
    for row in subs:
        print(row.classes)
    return subs
