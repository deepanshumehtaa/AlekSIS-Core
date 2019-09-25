from dashboard.caches import DRIVE_CACHE, Cache
from .api import *


def build_drive(force_update=False):
    cached = DRIVE_CACHE.get()
    if cached is not False and not force_update:
        print("Drive come from cache")
        return cached
    odrive = {
        "teachers": get_all_teachers(),
        "rooms": get_all_rooms(),
        "classes": get_all_classes(),
        "subjects": get_all_subjects(),
        "corridors": get_all_corridors(),
    }

    drive = {}
    for key, value in odrive.items():
        drive[key] = {}
        for el in value:
            id = el.id
            drive[key][id] = el

    DRIVE_CACHE.update(drive)
    return drive


drive = build_drive()
