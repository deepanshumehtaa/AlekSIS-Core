from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mailer import send_mail_with_template
from support.models import mail_settings
from untisconnect.api import get_all_rooms
from .forms import REBUSForm
from .forms import FeedbackForm
from dashboard.models import Activity


def add_arrows(array: list):
    return " → ".join([item for item in array if item != ""])


@login_required
def rebus(request):
    if request.method == 'POST':
        form = REBUSForm(request.POST)
        if form.is_valid():
            # Read out form data
            a = form.cleaned_data['a']
            b = form.cleaned_data["b"]
            c = form.cleaned_data["c"]
            short_description = form.cleaned_data['short_description']
            long_description = form.cleaned_data['long_description']

            # Register activity
            desc_act = "{} | {}".format(add_arrows([a, b, c]), short_description)
            act = Activity(title="Du hast uns ein Problem gemeldet.", description=desc_act, app="REBUS",
                           user=request.user)
            act.save()

            # Send mail
            context = {
                "arrow_list": add_arrows([a, b, c]),
                "short_desc": short_description,
                "long_desc": long_description,
                "user": request.user
            }
            send_mail_with_template("[REBUS] {}".format(short_description), [mail_settings.mail_rebus],
                                    "support/mail/rebus.txt",
                                    "support/mail/rebus.html", context,
                                    "{} <{}>".format(request.user.get_full_name(), request.user.email))

            return render(request, 'support/rebus_submitted.html')
    else:
        form = REBUSForm()

    rooms = [room.name for room in get_all_rooms()]

    return render(request, 'support/rebus.html', {'form': form, "props": {"rooms": rooms}})


@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Read out form data
            design_rating = form.cleaned_data['design_rating']
            performance_rating = form.cleaned_data['performance_rating']
            usability_rating = form.cleaned_data['usability_rating']
            overall_rating = form.cleaned_data['overall_rating']
            more = form.cleaned_data['more']
            ideas = form.cleaned_data['ideas']
            apps = form.cleaned_data["apps"]

            # Register activity
            act = Activity(title="Du hast uns Feedback gegeben.",
                           description="Du hast SchoolApps mit {} von 5 Sternen bewertet.".format(
                               overall_rating), app="Feedback",
                           user=request.user)
            act.save()

            # Send mail
            context = {
                "design": design_rating,
                "performance": performance_rating,
                "usability": usability_rating,
                "overall": overall_rating,
                "more": more,
                "apps": apps,
                "ideas": ideas,
                "user": request.user
            }
            send_mail_with_template("Feedback von {}".format(request.user.username),
                                    [mail_settings.mail_feedback],
                                    "support/mail/feedback.txt",
                                    "support/mail/feedback.html", context,
                                    "{} <{}>".format(request.user.get_full_name(), request.user.email))

            return render(request, 'support/feedback_submitted.html')
    else:
        form = FeedbackForm()

    return render(request, 'support/feedback.html', {'form': form})
