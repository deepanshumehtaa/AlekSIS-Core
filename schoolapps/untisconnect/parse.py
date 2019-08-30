from dashboard import caches

from .api import *
from .api_helper import untis_split_third

from .drive import drive

drive = drive


class Lesson(object):
    def __init__(self):
        self.filled = False
        self.id = None
        self.elements = []
        self.times = []

    def add_element(self, teacher, subject, rooms=[], classes=[]):
        el = LessonElement()
        el.create(teacher, subject, rooms, classes)
        self.elements.append(el)

    def add_time(self, day, hour, rooms=[]):
        el = LessonTime()
        el.create(day, hour, rooms)
        self.times.append(el)

    def create(self, raw_lesson, drive):
        self.filled = True

        # Split data (,)
        lesson_id = raw_lesson.lesson_id
        self.id = lesson_id
        raw_lesson_data = raw_lesson.lessonelement1.split(",")
        raw_time_data = raw_lesson.lesson_tt.split(",")

        rtd2 = []
        for el in raw_time_data:
            rtd2.append(el.split("~"))

        # print(rtd2)

        for el in rtd2:
            day = int(el[1])
            hour = int(el[2])
            room_ids = untis_split_third(el[3], conv=int)

            rooms = []
            for room_id in room_ids:
                r = drive["rooms"][room_id]
                rooms.append(r)

            self.add_time(day, hour, rooms)

        # print(raw_lesson_data)
        # print(raw_time_data)

        # Split data more (~)
        rld2 = []
        for el in raw_lesson_data:
            rld2.append(el.split("~"))

        # print(rld2)

        for i, el in enumerate(rld2):
            teacher_id = int(el[0])
            subject_id = int(el[2])
            class_ids = untis_split_third(el[17], conv=int)
            # print("TEACHER – ", teacher_id, "; SUBJECT – ", subject_id, "; ROOMS – ", room_ids, "; CLASSES – ",
            #       class_ids)

            if teacher_id != 0:
                teacher = drive["teachers"][teacher_id]
            else:
                teacher = None

            if subject_id != 0:
                subject = drive["subjects"][subject_id]
            else:
                subject = None

            rooms = []

            classes = []
            for class_id in class_ids:
                c = drive["classes"][class_id]
                classes.append(c)

            # print("TEACHER – ", teacher, "; SUBJECT – ", subject, "; ROOMS – ", rooms,
            #       "; CLASSES – ", classes)

            self.add_element(teacher, subject, rooms, classes)


class LessonElement(object):
    def __init__(self):
        self.teacher = None
        self.subject = None
        self.rooms = []
        self.classes = []

    def create(self, teacher, subject, rooms=[], classes=[]):
        self.teacher = teacher
        self.subject = subject
        self.rooms = rooms
        self.classes = classes


class LessonTime(object):
    def __init__(self):
        self.hour = None
        self.day = None
        self.rooms = []

    def create(self, day, hour, rooms=[]):
        self.day = day
        self.hour = hour
        self.rooms = rooms


def parse():
    global drive

    cached = caches.PARSED_LESSONS_CACHE.get()
    if cached is not False:
        print("Lessons come from cache")
        return cached
    lessons = []

    # Load lessons from Django ORM
    raw_lessons = get_raw_lessons()

    for raw_lesson in raw_lessons:

        if raw_lesson.lesson_tt and raw_lesson.lessonelement1:
            # Create object
            lesson_obj = Lesson()
            lesson_obj.create(raw_lesson, drive)

            lessons.append(lesson_obj)

    print("Lesson cache was refreshed")
    caches.PARSED_LESSONS_CACHE.update(lessons)

    return lessons


def get_lesson_by_id(id):
    global drive
    lesson = Lesson()
    raw_lesson = run_one(models.Lesson.objects, filter_term=True).get(lesson_id=id)
    lesson.create(raw_lesson, drive)
    return lesson


def get_lesson_element_by_id_and_teacher(lesson_id, teacher, hour=None, weekday=None):
    try:
        lesson = get_lesson_by_id(lesson_id)
    except Exception:
        return None, None
    el = None
    i = 0

    if teacher is not None:
        for i, element in enumerate(lesson.elements):
            if element.teacher is not None:
                if element.teacher.id == teacher.id:
                    el = element
                    break
    elif len(lesson.elements) > 0:
        el = lesson.elements[0]
    else:
        el = None

    t = None
    for time in lesson.times:
        if time.day == weekday and time.hour == hour:
            t = time

    room = None
    if t is not None and len(t.rooms) > i:
        room = t.rooms[i]

    if el is not None:
        return el, room
    return None, None
