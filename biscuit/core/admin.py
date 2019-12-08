from django.contrib import admin
from .models import Group, Person, School, SchoolTerm


class PersonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Person, PersonAdmin)


class GroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(Group, GroupAdmin)


class SchoolAdmin(admin.ModelAdmin):
    pass


admin.site.register(School, SchoolAdmin)


class SchoolTermAdmin(admin.ModelAdmin):
    pass


admin.site.register(SchoolTerm, SchoolTermAdmin)
