from django.shortcuts import render, redirect
from .forms import MenuUploadForm


# Create your views here.
def upload(request):
    if request.method == 'POST':
        form = MenuUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('menu_index')
    else:
        form = MenuUploadForm()
    return render(request, 'menu/upload.html', {
        'form': form
    })


def index(request):
    return render(request, 'menu/index.html')
