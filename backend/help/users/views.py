from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from main.models import Revisor
from .forms import AddUserForm, LoginForm
from django.contrib.auth.decorators import login_required
from decorators import group_required
from counting.utils import calculate_salary
import datetime 


@login_required
def profile_view(request):
    revisor = get_object_or_404(Revisor, user=request.user)
    user = request.user
    today = datetime.date.today()
    year = today.year
    month = today.month

    salary_data = calculate_salary(user, year, month)
    total_hours = salary_data['total_hours']
    hours_count = salary_data['hours_count']
    percentage = (total_hours / hours_count) * 100 if hours_count > 0 else 0

    context = {
        'revisor': revisor,
        'total_hours': salary_data['total_hours'],
        'hours_count': salary_data['hours_count'],
        'percentage': round(percentage, 2)
    }

    return render(request, 'profile.html', context)

@login_required
@group_required('God')
def add_user_view(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                revisor = Revisor.objects.get(email=user.email)
                revisor.user = user
                revisor.save()
            except Revisor.DoesNotExist:
                pass
            messages.success(request, 'Registration successful.')
            return redirect('login')
    else:
        form = AddUserForm()
    return render(request, 'add_user.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['last_login'] = str(user.last_login)

            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):

    request.session.pop('user_id', None)
    request.session.pop('username', None)
    request.session.pop('last_login', None)

    auth_logout(request)


    return redirect('login')

def error_view(request):
    return render(request, 'login_error.html')
