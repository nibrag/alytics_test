from django.shortcuts import render
from .models import Data, Calculate, ErrorLog
from .forms import AddDataForm


def index(request):
    data = Data.objects.all()
    calc = Calculate.objects.order_by('ts').first()
    error_logs = ErrorLog.objects.all()

    if request.method == 'POST':
        form = AddDataForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AddDataForm()
    return render(request, 'index.html', {
        'data': data, 'form': form,
        'calculate': calc, 'error_logs': error_logs})
