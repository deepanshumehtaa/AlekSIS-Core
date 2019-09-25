from dashboard.models import Cache

PARSED_LESSONS_CACHE, _ = Cache.objects.get_or_create(id="parsed_lessons",
                                                      defaults={"name": "Geparste Stunden (Regelplan)",
                                                                "expiration_time": 30})

DRIVE_CACHE, _ = Cache.objects.get_or_create(id="drive",
                                             defaults={"name": "Zwischenspeicher für teachers, rooms, classses, etc.",
                                                       "expiration_time": 60})

EXPIRATION_TIME_CACHE_FOR_PLAN_CACHES, _ = Cache.objects.get_or_create(id="expiration_time_cache_for_plan_caches",
                                                                       defaults={"name": "Ablaufzeit für Plan-Caches",
                                                                                 "expiration_time": 60})
