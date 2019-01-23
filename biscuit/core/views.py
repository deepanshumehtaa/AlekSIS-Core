from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'bisquit/index.html', context)
