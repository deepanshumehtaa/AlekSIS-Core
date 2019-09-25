from dashboard.caches import EXPIRATION_TIME_CACHE_FOR_PLAN_CACHES
from untisconnect.drive import drive, TYPE_TEACHER, TYPE_CLASS, Cache
from untisconnect.api_helper import date_to_untis_date


def get_cache_for_plan(type, id, smart=False, monday_of_week=None):
    cache_id = "plan_{}_{}{}".format(type, id, "_smart" if smart else "")
    if type == TYPE_TEACHER:
        idx = "teachers"
    elif type == TYPE_CLASS:
        idx = "classes"
    else:
        idx = "rooms"

    name = "Stundenplan für {}".format(drive[idx][id])

    if smart:
        cache_id += "_" + date_to_untis_date(monday_of_week)
        name += ", " + date_to_untis_date(monday_of_week)

    cache = Cache.objects.get_or_create(id=cache_id)[0]
    if cache.expiration_time != EXPIRATION_TIME_CACHE_FOR_PLAN_CACHES.expiration_time or cache.name != name:
        cache.expiration_time = EXPIRATION_TIME_CACHE_FOR_PLAN_CACHES.expiration_time
        cache.name = name
        cache.save()
    return cache
