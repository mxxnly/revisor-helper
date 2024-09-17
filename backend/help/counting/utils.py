
from django.shortcuts import render
from django.contrib.auth.models import User
from decimal import Decimal
import calendar
import datetime
from .models import WorkLog
from main.models import Revisor


def calculate_salary(user, year, month):
    first_day, last_day = calendar.monthrange(year, month)

    weekdays_count = sum(1 for day in range(1, last_day + 1)
                         if datetime.date(year, month, day).weekday() < 5)
    hours_count = Decimal(weekdays_count) * Decimal('8.00')
    user_email = user.email

    first_name = 'Unknown'
    last_name = 'Unknown'
    
    try:
        revisor = Revisor.objects.get(email=user_email)
        plus_or_minus = revisor.plus_or_minus
        first_name = revisor.firstname
        last_name = revisor.lastname
    except Revisor.DoesNotExist:
        plus_or_minus = Decimal('0.00')
    

    work_logs = WorkLog.objects.filter(
        user=user, 
        date__year=year, 
        date__month=month
    )

    salary_per_hour = Decimal('19500.00') / hours_count

    
    total_hours = Decimal('0.00')
    for log in work_logs:
        total_hours += log.hours_worked
        if log.hours_worked >= Decimal('8.0000'):
            total_hours += Decimal('0.25')


    total_hours += plus_or_minus
    hours_difference = total_hours - hours_count

    if total_hours <= 0:
        salary = Decimal('0.00')
    elif total_hours > hours_count:
        salary=Decimal('19500.00')
    else:
        salary = round(salary_per_hour * total_hours, 2)

    return {
        'user': user,
        'hours_count': hours_count,
        'total_hours': total_hours,
        'hours_difference': hours_difference,
        'is_full_month': total_hours == hours_count,
        'is_full_and_more': total_hours > hours_count,
        'salary': salary,
        'first_name' : first_name,
        'last_name' : last_name,
    }