from django.utils import timezone

from untisconnect import models
from untisconnect.api import run_default_filter, row_by_row_helper, format_classes, get_all_absences_by_date, \
    TYPE_TEACHER
from untisconnect.api_helper import run_using, untis_split_first, untis_date_to_date, date_to_untis_date
from untisconnect.parse import get_lesson_element_by_id_and_teacher
from untisconnect.drive import build_drive

TYPE_SUBSTITUTION = 0
TYPE_CANCELLATION = 1
TYPE_TEACHER_CANCELLATION = 2
TYPE_CORRIDOR = 3


def parse_type_of_untis_flags(flags):
    """
    Get type of substitution by parsing UNTIS flags
    :param flags: UNTIS flags (string)
    :return: type (int, constants are provided)
    """

    type_ = TYPE_SUBSTITUTION
    if "E" in flags:
        type_ = TYPE_CANCELLATION
    elif "F" in flags:
        type_ = TYPE_TEACHER_CANCELLATION
    return type_


# Build cache
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

        # Metadata
        self.id = db_obj.substitution_id
        self.lesson_id = db_obj.lesson_idsubst
        self.date = untis_date_to_date(db_obj.date)
        self.lesson = db_obj.lesson
        self.type = parse_type_of_untis_flags(db_obj.flags)
        self.text = db_obj.text

        # Teacher
        if db_obj.teacher_idlessn != 0:
            self.teacher_old = drive["teachers"][db_obj.teacher_idlessn]

        # print(self.teacher_new, self.teacher_old, self.lesson_id, self.id)
        if db_obj.teacher_idsubst != 0:
            self.teacher_new = drive["teachers"][db_obj.teacher_idsubst]

            if self.teacher_old is not None and self.teacher_new.id == self.teacher_old.id:
                self.teacher_new = None

            if self.teacher_old is None and self.teacher_new is not None:
                self.teacher_old = self.teacher_new
                self.teacher_new = None

        # print(self.teacher_old, self.teacher_new)

        self.lesson_element, self.room_old = get_lesson_element_by_id_and_teacher(self.lesson_id, self.teacher_old,
                                                                                  self.lesson, self.date.weekday() + 1)

        # Subject
        self.subject_old = self.lesson_element.subject if self.lesson_element is not None else None
        if db_obj.subject_idsubst != 0:
            self.subject_new = drive["subjects"][db_obj.subject_idsubst]

            if self.subject_old is not None and self.subject_old.id == self.subject_new.id:
                self.subject_new = None

        # Room
        if db_obj.room_idsubst != 0:
            self.room_new = drive["rooms"][db_obj.room_idsubst]

            if self.room_old is not None and self.room_old.id == self.room_new.id:
                self.room_new = None

        # Supervisement
        if db_obj.corridor_id != 0:
            self.corridor = drive["corridors"][db_obj.corridor_id]
            self.type = TYPE_CORRIDOR

        # Classes
        self.classes = []
        class_ids = untis_split_first(db_obj.classids, conv=int)

        for id in class_ids:
            self.classes.append(drive["classes"][id])


def substitutions_sorter(sub):
    """
    Sorting helper (sort function) for substitutions
    :param sub: Substitution to sort
    :return: A string for sorting by
    """

    # First, sort by class
    sort_by = sub.classes

    # If the sub hasn't got a class, then put it to the bottom
    if sort_by == "":
        sort_by = "Z"

    # Second, sort by lesson number
    sort_by += str(sub.lesson)

    return sort_by


class SubRow(object):
    def __init__(self):
        self.sub = None
        self.color = "black"
        self.css_class = "black-text"
        self.lesson = ""
        self.classes = ""
        self.teacher = ""
        self.teacher_full = ""
        self.teachers = []  # Only for events
        self.rooms = []  # Only for events
        self.absences = []  # Only for events
        self.subject = ""
        self.subject_full = ""
        self.room = ""
        self.room_full = ""
        self.text = ""
        self.extra = ""
        self.is_event = False
        self.event = None


def generate_event_table(events):
    sub_rows = []
    for event in events:
        sub_row = SubRow()
        sub_row.is_event = True
        sub_row.event = event

        if event.from_lesson != event.to_lesson:
            sub_row.lesson = "{}.-{}.".format(event.from_lesson, event.to_lesson)
        else:
            sub_row.lesson = "{}.".format(event.from_lesson)

        sub_row.classes = format_classes(event.classes)
        sub_row.teachers = event.teachers
        sub_row.rooms = event.rooms
        sub_row.absences = event.absences

        sub_row.color = "purple"
        sub_row.text = event.text

        sub_rows.append(sub_row)

    return sub_rows


def generate_sub_table(subs, events=[]):
    """
    Parse substitutions and prepare than for displaying in plan
    :param subs: Substitutions to parse
    :return: A list of SubRow objects
    """

    sub_rows = []
    for sub in subs:
        sub_row = SubRow()
        sub_row.sub = sub

        # Color
        sub_row.color = "black"
        if sub.type == 1 or sub.type == 2:
            sub_row.css_class = "green-text"
            sub_row.color = "green"
        elif sub.type == 3:
            sub_row.css_class = "blue-text"
            sub_row.color = "blue"

        #  Format lesson
        if sub.type == 3:
            sub_row.lesson = "{}./{}.".format(sub.lesson - 1, sub.lesson)
        else:
            sub_row.lesson = "{}.".format(sub.lesson)

        # Classes
        sub_row.classes = format_classes(sub.classes)

        # Hint text
        sub_row.text = sub.text

        # Badge
        sub_row.badge = None
        if sub.type == 1:
            sub_row.badge = "Schüler frei"
        elif sub.type == 2:
            sub_row.badge = "Lehrer frei"

        # Debugging information
        sub_row.extra = "{} {}".format(sub.id, sub.lesson_id)

        sub_rows.append(sub_row)

    sub_rows += generate_event_table(events)
    sub_rows.sort(key=substitutions_sorter)

    return sub_rows


class HeaderInformation:
    def __init__(self):
        self.absences = []
        self.missing_classes = []
        self.affected_teachers = []
        self.affected_classes = []
        self.rows = []

    def is_box_needed(self):
        return len(self.absences) > 0 or len(self.missing_classes) > 0 or len(
            self.affected_teachers) > 0 or len(self.affected_classes) > 0


def get_header_information(subs, date, events=[]):
    """
    Get header information like affected teachers/classes and missing teachers/classes for a given date
    :param date: The date as datetime object
    :param subs: All subs for the given date
    :return: HeaderInformation object with all kind of information
    """

    info = HeaderInformation()

    # Get all affected teachers and classes
    for sub in subs:
        if sub.teacher_old and sub.teacher_old not in info.affected_teachers:
            info.affected_teachers.append(sub.teacher_old)
        if sub.teacher_new and sub.teacher_new not in info.affected_teachers:
            info.affected_teachers.append(sub.teacher_new)

        for _class in sub.classes:
            if _class not in info.affected_classes:
                info.affected_classes.append(_class)

    for event in events:
        for teacher in event.teachers:
            if teacher.id not in [x.id for x in info.affected_teachers]:
                info.affected_teachers.append(teacher)

        for _class in event.classes:
            if _class.id not in [x.id for x in info.affected_classes]:
                info.affected_classes.append(_class)

    # Get all absences that are relevant for this day
    info.absences = get_all_absences_by_date(date)

    # Format list of affected teachers
    if info.affected_teachers:
        joined = ", ".join(sorted([x.shortcode for x in info.affected_teachers]))
        info.rows.append(("Betroffene Lehrkräfte", joined))

    # Format list of affected classes
    if info.affected_classes:
        joined = ", ".join(sorted([x.name for x in info.affected_classes]))
        info.rows.append(("Betroffene Klassen", joined))

    # Format list of missing teachers (absences)
    if info.absences:
        elements = []
        for absence in info.absences:
            if absence.type != TYPE_TEACHER:
                continue
            if absence.is_whole_day:
                # Teacher is missing the whole day
                elements.append("{}".format(absence.teacher.shortcode))
            elif absence.from_lesson == absence.to_lesson:
                elements.append("{} ({}.)".format(absence.teacher.shortcode, absence.from_lesson))
            else:
                # Teacher is only missing a part of day
                elements.append(
                    "{} ({}.-{}.)".format(absence.teacher.shortcode, absence.from_lesson, absence.to_lesson))
        joined = ", ".join(elements)

        info.rows.append(("Abwesende Lehrkräfte", joined))

    return info


def get_substitutions_by_date(date):
    subs_raw = run_default_filter(
        run_using(models.Substitution.objects.filter(date=date_to_untis_date(date), deleted=0).exclude(
            flags__contains="N").order_by("classids", "lesson")),
        filter_term=False)

    subs = row_by_row_helper(subs_raw, Substitution)
    # subs.sort(key=substitutions_sorter)
    return subs


def get_substitutions_by_date_as_dict(date):
    subs_raw = get_substitutions_by_date(date)
    sub_table = generate_sub_table(subs_raw)
    subs = {}
    for i, sub_raw in enumerate(subs_raw):
        if sub_raw.lesson_id not in subs.keys():
            subs[sub_raw.lesson_id] = []
        subs[sub_raw.lesson_id].append({"sub": sub_raw, "table": sub_table[i]})

    return subs
