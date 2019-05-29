from django.contrib import admin

from .models import DebugLogGroup, DebugLog


class DebugLogAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "group", "return_code", "filename", "updated_at"]


class DebugLogGroupAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]


# Register your models here.
admin.site.register(DebugLogGroup, DebugLogGroupAdmin)
admin.site.register(DebugLog, DebugLogAdmin)
