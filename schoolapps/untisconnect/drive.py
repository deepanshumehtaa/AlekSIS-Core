from .api import *

def build_drive():
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

    return drive


drive = build_drive()