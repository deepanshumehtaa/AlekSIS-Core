from aleksis.core.db_settings import db_settings


def db_settings_processor(request):
    return {"DB_SETTINGS": db_settings}
