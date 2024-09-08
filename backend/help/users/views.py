from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from main.models import Revisor
from .forms import AddUserForm, LoginForm
from django.contrib.auth.decorators import login_required
from decorators import group_required

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
