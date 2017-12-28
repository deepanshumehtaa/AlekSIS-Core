from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import ApplyForAUBForm
from .models import Aub


@login_required
@permission_required('aub.apply_for_aub')
def index(request):
    aubs = Aub.objects.all()[:10]

    context = {
        'aubs': aubs
    }
    return render(request, 'aub/index.html', context)


@login_required
@permission_required('aub.apply_for_aub')
def details(request, todo_id):
    todo = Aub.objects.get(id=todo_id)
    context = {
        'aub': aub
    }
    return render(request, 'aub/details.html', context)


@login_required
@permission_required('aub.apply_for_aub')
def apply_for(request):
    if request.method == 'POST':
        form = ApplyForAUBForm(request.POST)

        if form.is_valid():
            from_dt = form.cleaned_data['from_dt']
            to_dt = form.cleaned_data['to_dt']
            description = form.cleaned_data['description']

            aub = Aub(from_dt=from_dt, to_dt=to_dt, description=description, created_by=request.user)
            aub.save()

            return redirect(reverse('aub_applied_for'))

    else:
        form = ApplyForAUBForm()

    context = {
        'form': form,
    }

    return render(request, 'aub/apply_for.html', context)


@login_required
@permission_required('aub.apply_for_aub')
def applied_for(request):
    context = {

    }

    return render(request, 'aub/applied_for.html', context)
