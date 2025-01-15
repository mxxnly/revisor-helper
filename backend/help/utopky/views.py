from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
from counting.utils import calculate_salary
from django.contrib.auth.models import User

@login_required
def top(request):
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
    
    return render(request, 'top.html', {
        'users': users,
        'salary_data': salary_data,
        'month': month,
        'year': year,
        'months': months,
        'is_admin':is_admin
    })
