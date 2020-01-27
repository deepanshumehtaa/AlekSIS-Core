from django.utils.translation import gettext_lazy as _


def myplan_dashboard(request):
    context = {
        "title": _("My plan for today"),
    }
    return context


def calendar_dashboard(request):
    context = {
        "title": _("Current events"),
    }
    return context


def wordpress_dashboard(request):
    context = {
        "title": _("News "),
    }
    return context


WIDGETS = [
    (_("Your plan"),)
]
