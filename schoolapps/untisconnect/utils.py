from untisconnect.api import TYPE_TEACHER, get_teacher_by_shortcode, TYPE_CLASS, get_class_by_name, get_all_teachers, \
    get_all_classes, get_all_rooms, get_all_subjects
from untisconnect.datetimeutils import get_calendar_week, calendar_week, weekday
from untisconnect.plan import get_plan
from userinformation import UserInformation


def get_type_and_object_of_user(user):
    _type = UserInformation.user_type(user)
    if _type == UserInformation.TEACHER:
        # Teacher
        _type = TYPE_TEACHER
        shortcode = user.username
        el = get_teacher_by_shortcode(shortcode)
    elif _type == UserInformation.STUDENT:
        # Student
        _type = TYPE_CLASS
        _name = UserInformation.user_classes(user)[0]
        el = get_class_by_name(_name)
    else:
        # Nothing of both
        return None, None

    return _type, el


def overview_dict():
    return {
        'teachers': get_all_teachers(),
        'classes': get_all_classes(),
        'rooms': get_all_rooms(),
        'subjects': get_all_subjects()
    }


def get_plan_for_day(_type, plan_id, date):
    # Get calendar week and monday of week

    monday_of_week = get_calendar_week(calendar_week(date), date.year)["first_day"]
    week_day = weekday(date)

    # Get plan
    plan, holidays = get_plan(_type, plan_id, smart=True, monday_of_week=monday_of_week)
    lessons = [(row[week_day], time) for row, time in plan]

    holidays_for_date = holidays[week_day]
    return lessons, holidays_for_date
