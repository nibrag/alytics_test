from django.shortcuts import render
from .models import Data
from .forms import AddDataForm


def index(request):
    data = Data.objects.all()
    if request.method == 'POST':
        form = AddDataForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AddDataForm()
    return render(request, 'index.html', {'data': data, 'form': form})
