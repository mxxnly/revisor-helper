from django.utils import timezone
from django.shortcuts import render, redirect
from main.models import Revisor, Shop, Task
from .utils import assign_shop_to_revisor
from django.shortcuts import get_object_or_404
from django.db import models
from django.contrib.auth.decorators import login_required

@login_required
def assign_that_view(request):
    message = None

    if request.method == 'POST':
        revisor_id = request.POST.get('revisor_id')
        shop_id = request.POST.get('shop_id')

        if revisor_id and shop_id:
            revisor = get_object_or_404(Revisor, id=revisor_id)
            shop = get_object_or_404(Shop, id=shop_id)
            
            if not Task.objects.filter(shop=shop, completed_at__isnull=True).exists():
                Task.objects.create(shop=shop, revisor=revisor, assigned_at=timezone.now())
                message = f"{revisor.firstname} {revisor.lastname} був/-ла призначений/-a до {shop.name}"
                revisor.now_shop = shop
                revisor.save()
            else:
                message = "Магазин вже призначено."

        elif not revisor_id:
            message = "Будь ласка, виберіть ревізора."
        elif not shop_id:
            message = "Будь ласка, виберіть магазин."

    active_revisors = Task.objects.filter(completed_at__isnull=True).values_list('revisor_id', flat=True)
    revisors = Revisor.objects.exclude(id__in=active_revisors)
    
    # Retrieve all shops or apply any necessary filters
    shops = Shop.objects.all()

    tasks = Task.objects.filter(completed_at__isnull=True)

    return render(request, 'assign.html', {
        'revisors': revisors,
        'shops': shops,
        'message': message,
        'tasks': tasks
    })
@login_required
def assign_shop_view(request):
    message = None

    if request.method == 'POST':
        revisor_id = request.POST.get('revisor_id')
        if revisor_id:
            revisor = Revisor.objects.get(id=revisor_id)
            assigned_shop = assign_shop_to_revisor(revisor)
            if assigned_shop:
                message = f"{revisor.firstname} {revisor.lastname} був/-ла призначений/-a до {assigned_shop.name}"
            else:
                message = "Немає доступних магазинів для призначення."
        else:
            message = "Будь ласка, виберіть ревізора."

    active_revisors = Task.objects.filter(completed_at__isnull=True).values_list('revisor_id', flat=True)
    revisors = Revisor.objects.exclude(id__in=active_revisors)
    shops = Shop.objects.all()
    tasks = Task.objects.filter(completed_at__isnull=True)

    return render(request, 'assign.html', {
        'revisors': revisors,
        'shops': shops,
        'message': message,
        'tasks': tasks
    })
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    revisor = task.revisor
    task.complete_task()
    revisor.shops += 1
    revisor.save()
    shop = task.shop
    max_position = Shop.objects.aggregate(models.Max('position'))['position__max'] or 0
    shop.position = max_position + 1
    shop.last_counted_by = revisor
    shop.save()
    return redirect('assign_shop')
