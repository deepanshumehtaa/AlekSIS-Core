from django.utils import timezone

from schoolapps.settings import DEBUG
from untisconnect import models
from untisconnect.api import run_default_filter, row_by_row_helper, format_classes
from untisconnect.api_helper import run_using, untis_split_first
from untisconnect.parse import get_lesson_element_by_id_and_teacher, build_drive

DATE_FORMAT = "%Y%m%d"


def untis_date_to_date(untis):
    return timezone.datetime.strptime(str(untis), DATE_FORMAT)


def date_to_untis_date(date):
    return date.strftime(DATE_FORMAT)


TYPE_SUBSTITUTION = 0
TYPE_CANCELLATION = 1
TYPE_TEACHER_CANCELLATION = 2
TYPE_CORRIDOR = 3


def parse_type_of_untis_flags(flags):
    type_ = TYPE_SUBSTITUTION
    if "E" in flags:
        type_ = TYPE_CANCELLATION
    elif "F" in flags:
        type_ = TYPE_TEACHER_CANCELLATION
    return type_


drive = build_drive()


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
        self.lesson_element = None
        self.lesson_time = None

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
        self.type = parse_type_of_untis_flags(db_obj.flags)
        self.text = db_obj.text

        # Lesson

        # Teacher
        # print(db_obj.teacher_idlessn)
        if db_obj.teacher_idlessn != 0:
            self.teacher_old = drive["teachers"][db_obj.teacher_idlessn]

        if db_obj.teacher_idsubst != 0:
            self.teacher_new = drive["teachers"][db_obj.teacher_idsubst]

            if self.teacher_old is not None and self.teacher_new.id == self.teacher_old.id:
                self.teacher_new = None

            if self.teacher_old is None and self.teacher_new is not None:
                self.teacher_old = self.teacher_new
                self.teacher_new = None

        self.lesson_element, self.room_old = get_lesson_element_by_id_and_teacher(self.lesson_id, self.teacher_old,
                                                                                  self.lesson, self.date.weekday() + 1)
        # print(self.lesson)
        # print(self.room_old)
        # Subject
        self.subject_old = self.lesson_element.subject if self.lesson_element is not None else None
        if db_obj.subject_idsubst != 0:
            self.subject_new = drive["subjects"][db_obj.subject_idsubst]

            if self.subject_old is not None and self.subject_old.id == self.subject_new.id:
                self.subject_new = None

        # Room
        # self.rooms_old = self.lesson_element.rooms if self.lesson_element is not None else []
        # if len(self.rooms_old) >= 1:
        #     self.room_old = self.rooms_old[0]

        if db_obj.room_idsubst != 0:
            self.room_new = drive["rooms"][db_obj.room_idsubst]

            if self.room_old is not None and self.room_old.id == self.room_new.id:
                self.room_new = None
        # if self.rooms_old

        # print(self.room_new)
        # print("CORRIDOR")
        # print(self.corridor)
        if db_obj.corridor_id != 0:
            self.corridor = drive["corridors"][db_obj.corridor_id]
            self.type = TYPE_CORRIDOR
        # Classes

        self.classes = []
        class_ids = untis_split_first(db_obj.classids, conv=int)

        # print(class_ids)
        for id in class_ids:
            self.classes.append(drive["classes"][id])
        # print(self.classes)


def substitutions_sorter(sub):
    # First, sort by class
    sort_by = "".join(class_.name for class_ in sub.classes)

    # If the sub hasn't got a class, then put it to the bottom
    if sort_by == "":
        sort_by = "Z"

    # Second, sort by lesson number
    sort_by += str(sub.lesson)

    return sort_by


class SubRow(object):
    def __init__(self):
        self.color = "black"
        self.css_class = "black-text"
        self.lesson = ""
        self.classes = ""
        self.teacher = ""
        self.teacher_full = ""
        self.subject = ""
        self.subject_full = ""
        self.room = ""
        self.room_full = ""
        self.text = ""
        self.extra = ""


def generate_teacher_row(sub, full=False):
    # print(sub.id)
    teacher = ""
    if sub.type == 1:
        teacher = "<s>{}</s>".format(sub.teacher_old.shortcode if not full else sub.teacher_old.name)

    elif sub.teacher_new and sub.teacher_old:
        teacher = "<s>{}</s> → <strong>{}</strong>".format(
            sub.teacher_old.shortcode if not full else sub.teacher_old.name,
            sub.teacher_new.shortcode if not full else sub.teacher_new.name)
    elif sub.teacher_new and not sub.teacher_old:
        teacher = "<strong>{}</strong>".format(sub.teacher_new.shortcode if not full else sub.teacher_new.name)
    elif sub.teacher_old:
        teacher = "<strong>{}</strong>".format(sub.teacher_old.shortcode if not full else sub.teacher_old.name)

    return teacher


def generate_subject_row(sub, full=False):
    if sub.type == 3:
        subject = "Aufsicht"
    elif not sub.subject_new and not sub.subject_old:
        subject = ""
    elif sub.type == 1 or sub.type == 2:
        subject = "<s>{}</s>".format(sub.subject_old.shortcode if not full else sub.subject_old.name)
    elif sub.subject_new and sub.subject_old:
        subject = "<s>{}</s> → <strong>{}</strong>".format(
            sub.subject_old.shortcode if not full else sub.subject_old.name,
            sub.subject_new.shortcode if not full else sub.subject_new.name)
    elif sub.subject_new and not sub.subject_old:
        subject = "<strong>{}</strong>".format(sub.subject_new.shortcode if not full else sub.subject_new.name)
    else:
        subject = "<strong>{}</strong>".format(sub.subject_old.shortcode if not full else sub.subject_old.name)

    return subject


def generate_room_row(sub, full=False):
    room = ""
    if sub.type == 3:
        room = sub.corridor.name
    elif sub.type == 1 or sub.type == 2:
        pass
    elif sub.room_new and sub.room_old:
        room = "<s>{}</s> → <strong>{}</strong>".format(sub.room_old.shortcode if not full else sub.room_old.name,
                                                        sub.room_new.shortcode if not full else sub.room_new.name)
    elif sub.room_new and not sub.room_old:
        room = sub.room_new.shortcode if not full else sub.room_new.name
    elif not sub.room_new and not sub.room_old:
        pass
    else:
        room = sub.room_old.shortcode if not full else sub.room_old.name

    return room


def generate_sub_table(subs):
    sub_rows = []
    for sub in subs:
        sub_row = SubRow()

        sub_row.color = "black"
        if sub.type == 1 or sub.type == 2:
            sub_row.css_class = "green-text"
            sub_row.color = "green"
        elif sub.type == 3:
            sub_row.css_class = "blue-text"
            sub_row.color = "blue"

        if sub.type == 3:
            sub_row.lesson = "{}./{}".format(sub.lesson - 1, sub.lesson)
        else:
            sub_row.lesson = "{}.".format(sub.lesson)

        # for class_ in sub.classes:
        #     sub_row.classes += class_.name
        sub_row.classes = format_classes(sub.classes)

        sub_row.teacher = generate_teacher_row(sub)
        sub_row.teacher_full = generate_teacher_row(sub, full=True)
        sub_row.subject = generate_subject_row(sub)
        sub_row.subject_full = generate_subject_row(sub, full=True)
        sub_row.room = generate_room_row(sub)
        sub_row.room_full = generate_room_row(sub, full=True)

        # if DEBUG:
        #     # Add id only if debug mode is on
        #     if sub.text:
        #         sub_row.text = sub.text + " " + str(sub.id)
        #     else:
        #         sub_row.text = str(sub.id)
        # else:
        sub_row.text = sub.text

        sub_row.badge = None
        if sub.type == 1:
            sub_row.badge = "Schüler frei"
        elif sub.type == 2:
            sub_row.badge = "Lehrer frei"

        sub_row.extra = "{} {}".format(sub.id, sub.lesson_id)

        sub_rows.append(sub_row)
    return sub_rows


class HeaderInformation:
    def __init__(self):
        self.missing_teachers = []
        self.missing_classes = []
        self.affected_teachers = []
        self.affected_classes = []
        self.rows = []

    def is_box_needed(self):
        return len(self.missing_teachers) > 0 or len(self.missing_classes) > 0 or len(
            self.affected_teachers) > 0 or len(self.affected_classes) > 0


def get_header_information(subs):
    info = HeaderInformation()
    for sub in subs:
        if sub.teacher_old and sub.teacher_old not in info.affected_teachers:
            info.affected_teachers.append(sub.teacher_old)
        if sub.teacher_new and sub.teacher_new not in info.affected_teachers:
            info.affected_teachers.append(sub.teacher_new)
        # print(sub.teacher_old)

        for _class in sub.classes:
            if _class not in info.affected_classes:
                info.affected_classes.append(_class)

    if info.affected_teachers:
        joined = ", ".join(sorted([x.shortcode for x in info.affected_teachers]))
        # print(joined)
        info.rows.append(("Betroffene Lehrkräfte", joined))

    if info.affected_classes:
        joined = ", ".join(sorted([x.name for x in info.affected_classes]))
        info.rows.append(("Betroffene Klassen", joined))
    return info


def get_substitutions_by_date(date):
    subs_raw = run_default_filter(
        run_using(models.Substitution.objects.filter(date=date_to_untis_date(date), deleted=0).order_by("classids",
                                                                                                        "lesson")),
        filter_term=False)
    # print(subs_raw)

    subs = row_by_row_helper(subs_raw, Substitution)
    # print(subs)
    # for row in subs:
    #     print(row.classes)
    #     for class_ in row.classes:
    #         print(class_.name)
    subs.sort(key=substitutions_sorter)
    return subs


def get_substitutions_by_date_as_dict(date):
    subs_raw = get_substitutions_by_date(date)
    sub_table = generate_sub_table(subs_raw)
    # print("SUB RAW LEN", len(sub_table))
    subs = {}
    for i, sub_raw in enumerate(subs_raw):
        # print(i)
        if sub_raw.lesson_id not in subs.keys():
            subs[sub_raw.lesson_id] = []
        subs[sub_raw.lesson_id].append({"sub": sub_raw, "table": sub_table[i]})
        # print(sub_raw.teacher_old)
        # print(sub_table[i].teacher)
    # print(len(subs))
    return subs
