from django.contrib import admin

from .models import Group, Person, School, SchoolTerm


admin.site.register(Person)
admin.site.register(Group)
admin.site.register(School)
admin.site.register(SchoolTerm)
