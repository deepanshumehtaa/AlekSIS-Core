import datetime

from django.utils import timezone

from schoolapps import settings
from schoolapps.settings import LESSONS
from untisconnect.api import format_classes, get_today_holidays
from untisconnect.parse import parse
from untisconnect.sub import get_substitutions_by_date_as_dict, TYPE_CANCELLATION

TYPE_TEACHER = 0
TYPE_ROOM = 1
TYPE_CLASS = 2


class LessonContainer(object):
    """
    Needed for Django template because template language does not support dictionaries
    Saves the time object and the lesson elements
    """

    def __init__(self, ):
        self.time = None
        self.elements = []

    def set_time(self, time):
        self.time = time

    def append(self, element):
        self.elements.append(element)


class LessonElementContainer(object):
    """
    Needed for Django template because template language does not support dictionaries
    Saves the lesson element object and the room (from time object)
    """

    def __init__(self, element, room, substitution=None):
        self.element = element
        self.room = room
        self.substitution = substitution
        self.is_old = False
        if self.element is not None:
            self.classes_formatted = format_classes(self.element.classes)


def parse_lesson_times():
    times = []
    for i, t in enumerate(LESSONS):
        start_split = t[0].split(":")
        start_time = timezone.datetime(year=2000, day=1, month=1, hour=int(start_split[0]), minute=int(start_split[1]))
        end_time = start_time + timezone.timedelta(minutes=45)
        # print(start_time)
        # print(end_time)
        times.append({
            "number": i + 1,
            "number_format": t[1],
            "start": start_time,
            "end": end_time,
        })
    return times


def get_plan(type, id, smart=False, monday_of_week=None):
    """ Generates a plan for type (TYPE_TEACHE, TYPE_CLASS, TYPE_ROOM) and a id of the teacher (class, room)"""

    # Get parsed lessons
    lessons = parse()
    times_parsed = parse_lesson_times()

    hols_for_weekday = []

    if smart:
        # print("Get substitutions for smart plan")
        week_days = [monday_of_week + datetime.timedelta(days=i) for i in range(5)]
        # print(week_days)
        subs_for_weekday = []
        for week_day in week_days:
            # print(week_day)
            subs = get_substitutions_by_date_as_dict(week_day)
            subs_for_weekday.append(subs)

            hols = get_today_holidays(week_day)
            hols_for_weekday.append(hols)
            # print(subs)
            # print(len(subs))
    # Init plan array
    plan = []
    already_added_subs_as_ids = []

    # Fill plan array with LessonContainers (show upside), WIDTH and HEIGHT are defined by Django settings
    for hour_idx in range(settings.TIMETABLE_HEIGHT):
        plan.append(([], times_parsed[hour_idx] if len(times_parsed) > hour_idx else None))
        for day_idx in range(settings.TIMETABLE_WIDTH):
            plan[hour_idx][0].append(LessonContainer())

    # Fill plan with lessons
    for lesson in lessons:
        for i, element in enumerate(lesson.elements):

            # Check if the lesson element is important for that plan (look by type and id)
            found = False
            if type == TYPE_CLASS:
                for lclass in element.classes:
                    if lclass.id == id:
                        found = True

            elif type == TYPE_TEACHER:
                if element.teacher:
                    if element.teacher.id == id:
                        found = True

            elif type == TYPE_ROOM:
                for time in lesson.times:
                    for j, lroom in enumerate(time.rooms):
                        if lroom.id == id:
                            # print(lroom.name)
                            found = True

            # If the lesson element is important then add it to plan array
            if found:
                for time in lesson.times:  # Go for every time the lesson is thought
                    # Find matching rooms
                    room_index = None
                    for j, lroom in enumerate(time.rooms):
                        if lroom.id == id:
                            room_index = j

                    # Add the time object to the matching LessonContainer on the right position in the plan array
                    plan[time.hour - 1][0][time.day - 1].set_time(time)

                    # Check if there is an room for this time and lesson
                    try:
                        room = time.rooms[i]
                    except IndexError:
                        room = None

                    # Smart Plan: Check if there substitutions for this lesson
                    matching_sub = None

                    if smart:
                        # If a sub with matching lesson id and day exists
                        if subs_for_weekday[time.day - 1].get(lesson.id, None) is not None:
                            for sub in subs_for_weekday[time.day - 1][lesson.id]:
                                # ... check whether the sub has the right old teacher and the right lesson number
                                if sub["sub"].teacher_old.id == element.teacher.id and sub["sub"].lesson == time.hour:
                                    matching_sub = sub

                        # If the lesson matches, add it to the list of already added subs
                        if matching_sub:
                            already_added_subs_as_ids.append(matching_sub["sub"].id)

                    # Create a LessonElementContainer with room and lesson element
                    element_container = LessonElementContainer(element, room, substitution=matching_sub)

                    # Important for rooms: Check if the current room is the old room
                    if smart and matching_sub is not None:
                        if matching_sub["sub"].room_new is not None:
                            if matching_sub["sub"].room_old is not None:
                                if matching_sub["sub"].room_old != matching_sub["sub"].room_new:
                                    element_container.is_old = True
                            else:
                                element_container.is_old = True

                                # The rooms is empty, too, if the lesson is canceled
                        if matching_sub["sub"].type == TYPE_CANCELLATION:
                            element_container.is_old = True

                    # Check for holidays
                    if smart and hols_for_weekday[time.day - 1]:
                        element_container.is_hol = True
                        element_container.element.holiday_reason = hols_for_weekday[time.day - 1][0].name


                    if type != TYPE_ROOM or i == room_index:
                        # Add this container object to the LessonContainer object in the plan array
                        plan[time.hour - 1][0][time.day - 1].append(element_container)

    # Now check subs which were not in this plan before
    if smart:
        for i, week_day in enumerate(week_days):
            subs_for_this_weekday = subs_for_weekday[i]
            for lesson_id, subs in subs_for_this_weekday.items():
                for sub in subs:
                    found = False
                    room = sub["sub"].room_old
                    if type == TYPE_CLASS:
                        if sub["sub"].classes:
                            for _class in sub["sub"].classes:
                                if _class.id == id:
                                    found = True
                    elif type == TYPE_TEACHER:
                        if sub["sub"].teacher_new:
                            if sub["sub"].teacher_new.id == id:
                                found = True

                    elif type == TYPE_ROOM:
                        if sub["sub"].room_new:
                            if sub["sub"].room_new.id == id:
                                found = True
                    if found:
                        element_container = LessonElementContainer(sub["sub"].lesson_element, room, substitution=sub)
                        if sub["sub"].id not in already_added_subs_as_ids:
                            plan[sub["sub"].lesson - 1][0][i].append(element_container)

    return plan, hols_for_weekday
