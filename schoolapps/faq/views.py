from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from faq.models import FAQSection, FAQQuestion, mail_settings
from faq.forms import FAQForm

from datetime import datetime

from dashboard.models import Activity

from mailer import send_mail_with_template


def create_info(text):
    return '<div class="alert success"> <p> <i class="material-icons left">info</i>' + text + '</p> </div>'


def faq(request):
    """ Shows the FAQ site, also if not logged in"""
    context = {
        "questions": FAQQuestion.objects.filter(show=True),
        "sections": FAQSection.objects.all(),
    }
    return render(request, 'faq/faq.html', context)


@login_required
def ask(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            # Read out form data
            question = form.cleaned_data['question']

            act = Activity(title="Du hast uns eine Frage gestellt.", description=question, app="FAQ",
                           user=request.user)
            act.save()

            context = {
                "question": question,
                "user": request.user
            }
            send_mail_with_template("[FAQ QUESTION] {}".format(question), [mail_settings.mail_questions],
                                    "faq/mail/question.txt",
                                    "faq/mail/question.html", context,
                                    "{} <{}>".format(request.user.get_full_name(), request.user.email))

            return render(request, 'faq/question_submitted.html')
    else:
        form = FAQForm()

    return render(request, "faq/ask.html", {"form": form})
