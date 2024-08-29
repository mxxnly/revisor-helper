from decimal import Decimal
import calendar
import datetime
from .models import WorkLog
from main.models import Revisor

def calculate_salary(user):
    today = datetime.date.today()
    year = today.year
    month = today.month
    first_day, last_day = calendar.monthrange(year, month)

    weekdays_count = sum(1 for day in range(1, last_day + 1)
                         if datetime.date(year, month, day).weekday() < 5)
    hours_count = Decimal(weekdays_count) * Decimal('8.00')
    user_email = user.email

    

    try:
        revisor = Revisor.objects.get(email=user_email)
        plus_or_minus = revisor.plus_or_minus
    except Revisor.DoesNotExist:
        revisor = None
        plus_or_minus = Decimal('0.00')


    work_logs = WorkLog.objects.filter(
        user=user, 
        date__year=year, 
        date__month=month
    )
    salary_per_hour = 19500/hours_count
    
    total_hours = Decimal('0.00')
    for log in work_logs:
        total_hours += log.hours_worked
        if log.hours_worked >= 8:
            total_hours += Decimal('0.25')
    total_hours += plus_or_minus
    salary = 0.00
    hours_difference = total_hours - hours_count
    if hours_difference > 0:
        salary = round(salary_per_hour * hours_count, 2)
    else:
        salary = round(salary_per_hour* (total_hours + hours_difference), 2)

    return {
        'hours_count': hours_count,
        'total_hours': total_hours,
        'hours_difference': hours_difference,
        'is_full_month': total_hours == hours_count,
        'is_full_and_more': total_hours > hours_count,
        'salary' : salary,
    }