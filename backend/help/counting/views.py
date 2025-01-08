from django.shortcuts import render, redirect
from .forms import WorkLogForm
from .models import WorkLog
import calendar
from .utils import calculate_salary
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth.models import User
from decimal import Decimal
from decorators import group_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden


@login_required
def change_bonus_minutes(request, log_id):
    if request.method == 'POST':
        log = get_object_or_404(WorkLog, id=log_id, user=request.user)
        total_worked_hours = log.hours_worked + (log.minutes_worked / Decimal('60.00'))

        if log.bonus_added:
            log.minutes_worked -= Decimal('15')
            if log.minutes_worked < 0:
                log.hours_worked -= 1
                log.minutes_worked += 60
            log.bonus_added = False
        else:
            if total_worked_hours >= Decimal('7.75'):
                log.minutes_worked += Decimal('15')
                log.bonus_added = True
                log.adjust_time()
            

        log.save()

        return redirect('work_log')

    return HttpResponseForbidden("Invalid request method.")
@login_required
def work_log_view(request):
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='Admin').exists()
    else:
        is_admin = False
    today = datetime.date.today()
    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)  

    try:
        year = int(year)
        month = int(month)
        if month < 1 or month > 12:
            month = today.month  
    except ValueError:
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

            total_worked_hours = work_log.hours_worked + (work_log.minutes_worked / Decimal('60.00'))
            if total_worked_hours >= Decimal('7.75'):
                work_log.minutes_worked += Decimal('15')
                work_log.bonus_added = True
                work_log.save()

            work_log.adjust_time()

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
        'formatted_hours_difference': salary_data['formatted_hours_difference'],
        'formatted_total_hours': salary_data['formatted_total_hours'],
        'hours_difference': salary_data['hours_difference'],
        'is_full_month': salary_data['is_full_month'],
        'is_full_and_more': salary_data['is_full_and_more'],
        'salary': salary_data['salary'],
        'plus_or_minus': salary_data['plus_or_minus'],
        'months': list(range(1, 13)),
        'is_admin':is_admin,
    }
    return render(request, 'calendar.html', context)
@login_required
@group_required('Admin', 'God')
def user_work_log_view(request, user_id):
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='Admin').exists()
    else:
        is_admin = False
    user = get_object_or_404(User, id=user_id)
    today = datetime.date.today()
    year = today.year
    month = today.month
    first_day, last_day = calendar.monthrange(year, month)
    salary_data = calculate_salary(user, year, month)

    cal = calendar.Calendar().monthdayscalendar(year, month)

    if request.method == 'POST':
        form = WorkLogForm(request.POST)
        if form.is_valid():
            work_log = form.save(commit=False)
            work_log.user = user

            total_worked_hours = work_log.hours_worked + (work_log.minutes_worked / Decimal('60.00'))
            if total_worked_hours >= Decimal('7.75'):
                work_log.minutes_worked += Decimal('15')
                work_log.bonus_added = True
                work_log.adjust_time()
                work_log.save()


            existing_log = WorkLog.objects.filter(
                user=work_log.user,
                date=work_log.date
            ).first()

            if existing_log:
                existing_log.delete()

            work_log.save()
            return redirect('user_work_log_view', user_id=user_id)
    else:
        form = WorkLogForm()

    context = {
        'form': form,
        'calendar': cal,
        'year': year,
        'month': month,
        'user': user,
        'work_logs': WorkLog.objects.filter(date__year=year, date__month=month, user=user),
        'hours_count': salary_data['hours_count'],
        'total_hours': salary_data['total_hours'],
        'formatted_hours_difference': salary_data['formatted_hours_difference'],
        'formatted_total_hours': salary_data['formatted_total_hours'],
        'hours_difference': salary_data['hours_difference'],
        'is_full_month': salary_data['is_full_month'],
        'is_full_and_more': salary_data['is_full_and_more'],
        'salary': salary_data['salary'],
        'plus_or_minus': salary_data['plus_or_minus'],
        'is_admin':is_admin,
    }
    return render(request, 'user_calendar.html', context)

@login_required
@group_required('Admin', 'God')
def change_bonus_minutes_for_user(request, user_id, log_id):
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method.")

    log = get_object_or_404(WorkLog, id=log_id, user_id=user_id)
    total_worked_hours = log.hours_worked + (log.minutes_worked / Decimal('60.00'))

    if log.bonus_added:
        log.minutes_worked -= Decimal('15')
        if log.minutes_worked < 0:
            log.hours_worked -= 1
            log.minutes_worked += 60
        log.bonus_added = False
    elif total_worked_hours >= Decimal('7.75'):
        log.minutes_worked += Decimal('15')
        log.bonus_added = True
        log.adjust_time()

    log.save()

    return redirect('user_work_log_view', user_id=user_id)
@login_required
def delete_work_log(request, log_id,user_id):
    if request.method == 'POST':
        log = WorkLog.objects.filter(
            id=log_id,
            user=user_id
        ).first()

        if log:
            log.delete()

        return redirect('work_log', user_id=user_id)
    
    
@login_required
@group_required('Admin', 'God')
def delete_user_work_log(request, log_id, user_id):
    if request.method == 'POST':
        log = WorkLog.objects.filter(
            id=log_id,
            user=user_id
        ).first()

        if log:
            log.delete()

    return redirect('user_work_log_view',user_id=user_id)

@login_required
@group_required('Admin', 'God')
def salary_list_view(request):
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='Admin').exists()
    else:
        is_admin = False

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
        'users': users,
        'salary_data': salary_data,
        'month': month,
        'year': year,
        'months': months,
        'is_admin':is_admin
    })
