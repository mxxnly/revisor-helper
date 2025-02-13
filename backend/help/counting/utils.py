
from django.shortcuts import render
from django.contrib.auth.models import User
from decimal import Decimal
import calendar
import datetime
from .models import WorkLog
from main.models import Revisor
from hours_bonus.models import bonus_hours
from .models import MoneyLog


def format_hours(minutes_total):
    hours = int(minutes_total)
    minutes = int((minutes_total - hours) * 60)
    return f"{hours} год {minutes} хв"


def calculate_total_money_for_month(user, year, month):
    logs = MoneyLog.objects.filter(user=user, date__year=year, date__month=month)
    total_money = sum(log.money_spend for log in logs if log.money_spend > 0)
    return total_money


def calculate_salary(user, year, month):
    first_day, last_day = calendar.monthrange(year, month)

    weekdays_count = sum(1 for day in range(1, last_day + 1)
                         if datetime.date(year, month, day).weekday() < 5)
    hours_count = Decimal(weekdays_count) * Decimal('8.00')
    user_email = user.email

    first_name = 'Unknown'
    last_name = 'Unknown'
    who_are = 'Unknown'
    
    try:
        revisor = Revisor.objects.get(email=user_email)
        first_name = revisor.firstname
        last_name = revisor.lastname
        who_are = revisor.who_are
    except Revisor.DoesNotExist:
        plus_or_minus = Decimal('0.00')
    
    try:
        bonus_entry = bonus_hours.objects.get(user=user, year=year, month=month)
        hours = Decimal(str(bonus_entry.hours))
        minutes = Decimal(str(bonus_entry.minutes)) / 60  
        plus_or_minus = hours + minutes
    except bonus_hours.DoesNotExist:
        plus_or_minus = Decimal('0.00')

    formatted_plus_or_minus = format_hours(plus_or_minus)
    work_logs = WorkLog.objects.filter(
        user=user, 
        date__year=year, 
        date__month=month
    )
    if who_are == 'ревізор' or 'Ревізор':
        salary_per_hour = Decimal('19500.00') / hours_count
    else:
        salary_per_hour = Decimal('18500.00') / hours_count

    

    
    total_hours = Decimal('0.00')
    for log in work_logs:
        total_hours += log.hours_worked + log.minutes_worked/60

    current_month_hours = format_hours(total_hours)
    total_hours += plus_or_minus
    hours_difference = total_hours - hours_count

    if total_hours <= 0:
        salary = Decimal('0.00')
    elif total_hours > hours_count:
        salary=Decimal('19500.00')
    else:
        salary = round(salary_per_hour * total_hours, 2)

    formatted_hours_difference = format_hours(hours_difference)
    formatted_total_hours = format_hours(total_hours)

    return {
        'user': user,
        'hours_count': hours_count, 
        'total_hours': total_hours,  
        'hours_difference': hours_difference, 
        'formatted_total_hours': formatted_total_hours,  
        'formatted_hours_difference': formatted_hours_difference,
        'is_full_month': total_hours == hours_count,
        'is_full_and_more': total_hours > hours_count,
        'salary': salary,
        'first_name' : first_name,
        'last_name' : last_name,
        'plus_or_minus' : plus_or_minus,
        'current_month_hours' : current_month_hours,
        'formatted_plus_or_minus':formatted_plus_or_minus,
    }