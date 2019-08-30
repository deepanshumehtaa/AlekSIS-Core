from dashboard.models import Cache
from untisconnect.drive import drive, TYPE_TEACHER, TYPE_ROOM, TYPE_CLASS
from untisconnect.api_helper import date_to_untis_date

# drive = drive

PARSED_LESSONS_CACHE, _ = Cache.objects.get_or_create(id="parsed_lessons",
                                                      defaults={"name": "Geparste Stunden (Regelplan)",
                                                                "expiration_time": 30})


def get_cache_for_plan(type, id, smart=False, monday_of_week=None):
    cache_id = "plan_{}_{}{}".format(type, id, "_smart" if smart else "")
    if type == TYPE_TEACHER:
        idx = "teachers"
    elif type == TYPE_CLASS:
        idx = "classes"
    else:
        idx = "rooms"
    print(idx, )

    name = "Stundenplan für {}".format(drive[idx][id])

    if smart:
        cache_id += "_" + date_to_untis_date(monday_of_week)
        name += ", " + date_to_untis_date(monday_of_week)

    print("CACHE", cache_id, name)

    return Cache.objects.get_or_create(id=cache_id, defaults={"name": name, "expiration_time": 30})[0]
