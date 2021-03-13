from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

import django_tables2 as tables
from django_tables2.utils import A, AttributeDict, computed_values


class SchoolTermTable(tables.Table):
    """Table to list persons."""

    class Meta:
        attrs = {"class": "responsive-table highlight"}

    name = tables.LinkColumn("edit_school_term", args=[A("id")])
    date_start = tables.Column()
    date_end = tables.Column()
    edit = tables.LinkColumn(
        "edit_school_term",
        args=[A("id")],
        text=_("Edit"),
        attrs={"a": {"class": "btn-flat waves-effect waves-orange orange-text"}},
        verbose_name=_("Actions"),
    )


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
    school_term = tables.Column()


class AdditionalFieldsTable(tables.Table):
    """Table to list group types."""

    class Meta:
        attrs = {"class": "responsive-table hightlight"}

    title = tables.LinkColumn("edit_additional_field_by_id", args=[A("id")])
    delete = tables.LinkColumn(
        "delete_additional_field_by_id",
        args=[A("id")],
        verbose_name=_("Delete"),
        text=_("Delete"),
        attrs={"a": {"class": "btn-flat waves-effect waves-red"}},
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


class DashboardWidgetTable(tables.Table):
    """Table to list dashboard widgets."""

    class Meta:
        attrs = {"class": "responsive-table highlight"}

    widget_name = tables.Column(accessor="pk")
    title = tables.LinkColumn("edit_dashboard_widget", args=[A("id")])
    active = tables.BooleanColumn(yesno="check,cancel", attrs={"span": {"class": "material-icons"}})
    delete = tables.LinkColumn(
        "delete_dashboard_widget",
        args=[A("id")],
        text=_("Delete"),
        attrs={"a": {"class": "btn-flat waves-effect waves-red red-text"}},
        verbose_name=_("Actions"),
    )

    def render_widget_name(self, value, record):
        return record._meta.verbose_name


class MaterializeCheckboxColumn(tables.CheckBoxColumn):
    """Checkbox column with Materialize support."""

    empty_values = ()

    @property
    def header(self):
        """Render the header cell."""
        default = {"type": "checkbox"}
        general = self.attrs.get("input")
        specific = self.attrs.get("th__input")
        attrs = AttributeDict(default, **(specific or general or {}))
        return mark_safe("<label><input %s/><span></span></label>" % attrs.as_html())  # noqa

    def render(self, value, bound_column, record):
        """Render a data cell."""
        default = {"type": "checkbox", "name": bound_column.name, "value": value}
        if self.is_checked(value, record):
            default.update({"checked": "checked"})

        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")

        attrs = dict(default, **(specific or general or {}))
        attrs = computed_values(attrs, kwargs={"record": record, "value": value})
        return mark_safe(  # noqa
            "<label><input %s/><span></span</label>" % AttributeDict(attrs).as_html()
        )


class SelectColumn(MaterializeCheckboxColumn):
    """Column with a check box prepared for `ActionForm` forms."""

    def __init__(self, *args, **kwargs):
        kwargs["attrs"] = {
            "td__input": {"name": "selected_objects"},
            "th__input": {"id": "header_box"},
        }
        kwargs.setdefault("accessor", A("pk"))
        super().__init__(*args, **kwargs)
