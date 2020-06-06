from datetime import date
from typing import Union

from django.contrib.sites.managers import CurrentSiteManager as _CurrentSiteManager
from django.db.models import QuerySet

from calendarweek import CalendarWeek


class CurrentSiteManagerWithoutMigrations(_CurrentSiteManager):
    """CurrentSiteManager for auto-generating managers just by query sets."""

    use_in_migrations = False


class DateRangeQuerySetMixin:
    """QuerySet with custom query methods for models with date ranges.

    Filterable fields: date_start, date_end
    """

    def within_dates(self, start: date, end: date):
        """Filter for all objects within a date range."""
        return self.filter(date_start__lte=end, date_end__gte=start)

    def in_week(self, wanted_week: CalendarWeek):
        """Filter for all objects within a calendar week."""
        return self.within_dates(wanted_week[0], wanted_week[6])

    def on_day(self, day: date):
        """Filter for all objects on a certain day."""
        return self.within_dates(day, day)


class SchoolYearQuerySet(QuerySet, DateRangeQuerySetMixin):
    """Custom query set for school years."""


class SchoolYearRelatedQuerySet(QuerySet):
    """Custom query set for all models related to school years."""

    def within_dates(self, start: date, end: date) -> "SchoolYearRelatedQuerySet":
        """Filter for all objects within a date range."""
        return self.filter(school_year__date_start__lte=end, school_year__date_end__gte=start)

    def in_week(self, wanted_week: CalendarWeek) -> "SchoolYearRelatedQuerySet":
        """Filter for all objects within a calendar week."""
        return self.within_dates(wanted_week[0], wanted_week[6])

    def on_day(self, day: date) -> "SchoolYearRelatedQuerySet":
        """Filter for all objects on a certain day."""
        return self.within_dates(day, day)

    def for_school_year(self, school_year: "SchoolYear") -> "SchoolYearRelatedQuerySet":
        return self.filter(school_year=school_year)

    def for_current_school_year_or_all(self) -> "SchoolYearRelatedQuerySet":
        """Get all objects related to current school year.

        If there is no current school year, it will return all objects.
        """
        from aleksis.core.models import SchoolYear

        current_school_year = SchoolYear.current
        if current_school_year:
            return self.for_school_year(current_school_year)
        else:
            return self

    def for_current_school_year_or_none(self) -> Union["SchoolYearRelatedQuerySet", None]:
        """Get all objects related to current school year.

        If there is no current school year, it will return `None`.
        """
        from aleksis.core.models import SchoolYear

        current_school_year = SchoolYear.current
        if current_school_year:
            return self.for_school_year(current_school_year)
        else:
            return None
