from django.contrib import admin

from guardian.admin import GuardedModelAdmin


from .models import (
    Group,
    Person,
    School,
    SchoolTerm,
    Activity,
    Notification,
    Announcement,
    AnnouncementRecipient,
    CustomMenuItem,
)

class PersonAdmin(GuardedModelAdmin):
    pass


admin.site.register(Person, PersonAdmin)
admin.site.register(Group)
admin.site.register(School)
admin.site.register(SchoolTerm)
admin.site.register(Activity)
admin.site.register(Notification)
admin.site.register(CustomMenuItem)


class AnnouncementRecipientInline(admin.StackedInline):
    model = AnnouncementRecipient


class AnnouncementAdmin(admin.ModelAdmin):
    inlines = [
        AnnouncementRecipientInline,
    ]


admin.site.register(Announcement, AnnouncementAdmin)
