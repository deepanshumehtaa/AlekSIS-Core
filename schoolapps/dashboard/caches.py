from dashboard.models import Cache

PARSED_LESSONS_CACHE, _ = Cache.objects.get_or_create(id="parsed_lessons",
                                                      defaults={"name": "Geparste Stunden (Regelplan)",
                                                                "expiration_time": 60 * 60 * 24})

DRIVE_CACHE, _ = Cache.objects.get_or_create(id="drive",
                                             defaults={"name": "Zwischenspeicher für teachers, rooms, classses, etc.",
                                                       "expiration_time": 60})

EXPIRATION_TIME_CACHE_FOR_PLAN_CACHES, _ = Cache.objects.get_or_create(id="expiration_time_cache_for_plan_caches",
                                                                       defaults={"name": "Ablaufzeit für Plan-Caches",
                                                                                 "expiration_time": 60})

BACKGROUND_CACHE_REFRESH, _ = Cache.objects.get_or_create(id="background_cache_refresh",
                                                          defaults={
                                                              "name": "Hintergrundaktualisierung der Variablencaches",
                                                              "expiration_time": 0})

PLAN_VIEW_CACHE, _ = Cache.objects.get_or_create(id="plan_view_cache",
                                                 defaults={
                                                     "site_cache": True,
                                                     "name": "Wochenplan (Regelplan/SMART PLAN)",
                                                     "expiration_time": 60})

MY_PLAN_VIEW_CACHE, _ = Cache.objects.get_or_create(id="my_plan_view_cache",
                                                    defaults={
                                                        "site_cache": True,
                                                        "name": "Mein Plan",
                                                        "expiration_time": 60})

SUBS_VIEW_CACHE, _ = Cache.objects.get_or_create(id="subs_view_cache",
                                                 defaults={
                                                     "site_cache": True,
                                                     "name": "Vertretungen (Tabellenansicht)",
                                                     "expiration_time": 60})
