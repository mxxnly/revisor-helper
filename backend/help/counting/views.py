from django.shortcuts import render, redirect
from .forms import WorkLogForm
from .models import WorkLog
from django.utils import timezone
import calendar
from .utils import calculate_salary
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def work_log_view(request):
    today = datetime.date.today()
    year = today.year
    month = today.month
    first_day, last_day = calendar.monthrange(year, month)
    salary_data = calculate_salary(request.user)
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