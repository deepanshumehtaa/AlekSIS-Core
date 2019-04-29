from django.shortcuts import render
from faq.models import FAQQuestion
from faq.forms import FAQForm

# Create your views here.

def create_info(text):
    return '<div class="alert success"> <p> <i class="material-icons left">info</i>' + text + '</p> </div>'


def faq(request):
    """ Shows the FAQ site, also if not logged in"""
    context = {
        "questions": FAQQuestion.objects.filter(answered=True),
    }
    return render(request, 'faq/faq.html', context)

def ask(request):
    form = FAQForm()

    return render(request, "faq/ask.html", {"form": form})