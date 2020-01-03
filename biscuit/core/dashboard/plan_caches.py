import datetime
from django.utils import timezone
from dashboard.caches import EXPIRATION_TIME_CACHE_FOR_PLAN_CACHES
from untisconnect.drive import drive, TYPE_TEACHER, TYPE_CLASS, Cache
from untisconnect.api_helper import date_to_untis_date


def get_cache_for_plan(type: int, id: int, smart: bool = False, monday_of_week=None) -> Cache:
    """
    Creates a Cache for a plan with given params
    :param type: TYPE_TEACHER, TYPE_CLASS or TYPE_ROOM
    :param id: database id of plan
    :param smart: Is smart?
    :param monday_of_week: Monday of needed week (if smart)
    :return: Cache object
    """

    # Create unique id for plan cache
    cache_id = "plan_{}_{}{}".format(type, id, "_smart" if smart else "")

    # Decide which type of plan
    if type == TYPE_TEACHER:
        idx = "teachers"
    elif type == TYPE_CLASS:
        idx = "classes"
    else:
        idx = "rooms"

    # Set name for cache entry
    name = "Stundenplan für {}".format(drive[idx][id])

    needed_until = timezone.now().date() + datetime.timedelta(days=1)
    if smart:
        # Add date to cache id and name if smart plan
        cache_id += "_" + date_to_untis_date(monday_of_week)
        name += ", " + date_to_untis_date(monday_of_week)

        # Set time after which cache will be deleted
        needed_until = monday_of_week + datetime.timedelta(days=4)

    # Create new cache entry
    cache = Cache.objects.get_or_create(id=cache_id)[0]

    # Set expiration time and name to cache entry
    if cache.expiration_time != EXPIRATION_TIME_CACHE_FOR_PLAN_CACHES.expiration_time or cache.name != name:
        cache.expiration_time = EXPIRATION_TIME_CACHE_FOR_PLAN_CACHES.expiration_time
        cache.name = name
        cache.needed_until = needed_until
        cache.save()

    return cache
