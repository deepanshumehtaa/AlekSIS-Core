from django.utils.translation import gettext_lazy as _

import django_tables2 as tables
from django_tables2.utils import A


class PersonsTable(tables.Table):
    """Table to list persons."""

    class Meta:
        attrs = {"class": "responsive-table highlight"}

    first_name = tables.LinkColumn("person_by_id", args=[A("id")])
    last_name = tables.LinkColumn("person_by_id", args=[A("id")])


class GroupsTable(tables.Table):
    """Table to list groups."""

    class Meta:
        attrs = {"class": "responsive-table highlight"}

    name = tables.LinkColumn("group_by_id", args=[A("id")])
    short_name = tables.LinkColumn("group_by_id", args=[A("id")])


class AdditionalFieldsTable(tables.Table):
    """Table to list group types."""

    class Meta:
        attrs = {"class": "responsive-table hightlight"}

    title = tables.LinkColumn("edit_additional_field_by_id", args=[A("id")])
    delete = tables.LinkColumn(
        "delete_additional_field_by_id", args=[A("id")], verbose_name=_("Delete"), text=_("Delete")
    )


class GroupTypesTable(tables.Table):
    """Table to list group types."""

    class Meta:
        attrs = {"class": "responsive-table highlight"}

    name = tables.LinkColumn("edit_group_type_by_id", args=[A("id")])
    description = tables.LinkColumn("edit_group_type_by_id", args=[A("id")])
    delete = tables.LinkColumn(
        "delete_group_type_by_id", args=[A("id")], verbose_name=_("Delete"), text=_("Delete")
    )
