from django.shortcuts import render, redirect
from .forms import WorkLogForm
from .models import WorkLog
from django.utils import timezone
import calendar
from .utils import calculate_salary
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth.models import User
from decimal import Decimal
from main.models import Revisor

from django.http import JsonResponse
from decorators import group_required



@login_required
def work_log_view(request):
    today = datetime.date.today()
    year = today.year
    month = today.month
    first_day, last_day = calendar.monthrange(year, month)

    salary_data = calculate_salary(request.user, year, month)

    cal = calendar.Calendar().monthdayscalendar(year, month)
    if request.method == 'POST':
        form = WorkLogForm(request.POST)
        if form.is_valid():
            work_log = form.save(commit=False)
            work_log.user = request.user
            existing_log = WorkLog.objects.filter(
                user=work_log.user,
                date=work_log.date
            ).first()

            if existing_log:
                existing_log.delete()

            work_log.save()
            return redirect('work_log')
    else:
        form = WorkLogForm()

    context = {
        'form': form,
        'calendar': cal,
        'year': year,
        'month': month,
        'work_logs': WorkLog.objects.filter(date__year=year, date__month=month, user=request.user),
        'hours_count': salary_data['hours_count'],
        'total_hours': salary_data['total_hours'],
        'hours_difference': salary_data['hours_difference'],
        'is_full_month': salary_data['is_full_month'],
        'is_full_and_more': salary_data['is_full_and_more'],
        'salary' : salary_data['salary']
    }
    return render(request, 'calendar.html', context)

@login_required
def delete_work_log(request, log_id):
    if request.method == 'POST':
        log = WorkLog.objects.filter(
            id=log_id,
            user=request.user
        ).first()

        if log:
            log.delete()

    return redirect('work_log')

@login_required
@group_required('Admin', 'God')
def salary_list_view(request):

    month = int(request.GET.get('month', datetime.date.today().month))
    year = int(request.GET.get('year', datetime.date.today().year))

    users = User.objects.all()
    salary_data = []
    
    for user in users:
        salary_info = calculate_salary(user, year, month)
        if salary_info['total_hours'] > 0:
            salary_data.append(salary_info)

    months = list(range(1, 13)) 
    
    return render(request, 'salary.html', {
        'salary_data': salary_data,
        'month': month,
        'year': year,
        'months': months,
    })


@login_required
@group_required('Admin', 'God')
def update_hours_difference(request):
    if request.method == 'POST':
        revisor_id = request.POST.get('revisor_id')
        hours_difference = request.POST.get('hours_difference')

        if revisor_id and hours_difference:
            try:
                revisor = Revisor.objects.get(id=revisor_id)
                revisor.plus_or_minus = hours_difference
                revisor.save()
                return redirect('salary_list')
            except Revisor.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Revisor does not exist'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)
    else:
        revisors = Revisor.objects.all()
        return render(request, 'difference.html', {'revisors': revisors})


def elina(request):
    return render(request, "elina.html")