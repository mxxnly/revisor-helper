from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from decorators import group_required
from main.models import Revisor
from django.shortcuts import render, redirect
from hours_bonus.forms import BonusForm
from .models import bonus_hours
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


@login_required
def update_hours_difference(request):
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='Admin').exists()
    else:
        is_admin = False
    
    if request.method == 'POST':
        form = BonusForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']

            try:
                bonus_hours.objects.filter(user=request.user,month=month, year=year).delete()
                
                bonus_hours.objects.create(
                    user=request.user,
                    month=month,
                    year=year,
                    hours=hours,
                    minutes=minutes
                )

                messages.success(request, 'Запис створено або перезаписано успішно.')
                return redirect('update_hours')
            except Exception as e:
                messages.error(request, f'Сталася помилка: {str(e)}')
        else:
            messages.error(request, 'Некоректні дані у формі.')

    else:
        form = BonusForm()

    revisors = Revisor.objects.select_related('user').all()

    return render(request, 'difference.html', {
        'form': form,
        'revisors': revisors,
        'is_admin': is_admin
    })