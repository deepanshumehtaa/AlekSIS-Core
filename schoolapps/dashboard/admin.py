from django.contrib import admin
from .models import Activity, Notification, Cache


class CacheAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "site_cache", "last_time_updated"]


admin.site.register(Activity)
admin.site.register(Notification)
admin.site.register(Cache, CacheAdmin)
