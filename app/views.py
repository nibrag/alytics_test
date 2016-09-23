from __future__ import absolute_import
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils import timezone
from celery import shared_task, chain, chord
from .models import Data, Calculate, ErrorLog
from .forms import AddDataForm


def index(request):
    data = Data.objects.all()
    calc = Calculate.objects.order_by('-ts').first()
    error_logs = ErrorLog.objects.all()

    if request.method == 'POST':
        form = AddDataForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AddDataForm()
    return render(request, 'index.html', {
        'data': data, 'form': form,
        'calculate': calc, 'error_logs': error_logs,
        'calc_started': request.GET.get('calc_started') == 'yes'})


def run_calculator(request):
    tasks = []
    calc_id = Calculate.objects.create(ts=timezone.now(),
                                       started=True).pk

    for data_id in Data.objects.values_list('pk', flat=True):
        task = chain(get_data.si(data_id, calc_id),
                     calculator.s(data_id, calc_id),
                     save_data.s(data_id))
        tasks.append(task)
    chord(tasks, tasks_done.s(calc_id)).delay()

    return redirect(reverse('index') + '?calc_started=yes')


@shared_task
def get_data(data_id, calc_id):
    try:
        return Data.objects.get(pk=data_id).data
    except Exception as exc:
        err = ErrorLog.objects.create(ts=timezone.now(),
                                      data_id=data_id, msg=str(exc))
        Calculate.objects.filter(pk=calc_id).update(error=err)


@shared_task
def save_data(result, data_id):
    if result is not None:
        result = {'result': result}
    Data.objects.filter(pk=data_id).update(result=result)


@shared_task
def calculator(data, data_id, calc_id):
    if not data:
        return None

    try:
        return sum(item['a'] + item['b'] for item in data)
    except Exception as exc:
        err = ErrorLog.objects.create(ts=timezone.now(),
                                      data_id=data_id, msg=str(exc))
        Calculate.objects.filter(pk=calc_id).update(error=err)


@shared_task
def tasks_done(r, calc_id):
    Calculate.objects.filter(pk=calc_id).update(started=False)
