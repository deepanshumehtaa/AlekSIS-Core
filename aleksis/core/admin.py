from django.contrib import admin

from .mixins import BaseModelAdmin
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


class PersonAdmin(BaseModelAdmin):
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


class AnnouncementAdmin(BaseModelAdmin):
    inlines = [
        AnnouncementRecipientInline,
    ]


admin.site.register(Announcement, AnnouncementAdmin)
