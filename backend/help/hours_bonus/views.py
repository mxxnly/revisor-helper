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
@group_required('Admin', 'God')
@login_required
@group_required('Admin', 'God')
def update_hours_difference(request):
    if request.method == 'POST':
        form = BonusForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']

            try:
                bonus_entry, created = bonus_hours.objects.update_or_create(
                    user=user,
                    month=month,
                    year=year,
                    defaults={
                        'hours': hours,
                        'minutes': minutes
                    }
                )
                if created:
                    messages.success(request, 'Новий бонусний запис створено успішно.')
                else:
                    messages.success(request, 'Існуючий запис оновлено успішно.')
                return redirect('update_hours')
            except Revisor.DoesNotExist:
                messages.error(request, 'Ревізора для цього користувача не знайдено.')
        else:
            messages.error(request, 'Некоректні дані у формі.')

    else:
        form = BonusForm()

    revisors = Revisor.objects.select_related('user').all()

    return render(request, 'difference.html', {'form': form, 'revisors': revisors})
