from django.utils import timezone
from django.shortcuts import render, redirect
from main.models import Revisor, Shop, Task
from .utils import assign_shop_to_revisor
from django.shortcuts import get_object_or_404
from django.db import models
from django.contrib.auth.decorators import login_required
from decorators import group_required


@login_required
@group_required('Admin', 'God')
def assign_that_view(request):
    message = None
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='Admin').exists()
    else:
        is_admin = False

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
    
    shops = Shop.objects.all()

    tasks = Task.objects.filter(completed_at__isnull=True)

    return render(request, 'assign.html', {
        'revisors': revisors,
        'shops': shops,
        'message': message,
        'tasks': tasks,
        'is_admin':is_admin,
    })
@login_required
def assign_shop_view(request):
    message = None
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='Admin').exists()
    else:
        is_admin = False

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
        'tasks': tasks,
        'is_admin':is_admin,
    })
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    revisor = task.revisor
    
    if (revisor.user != request.user and
            not request.user.groups.filter(name__in=['Admin', 'God']).exists()):
        return redirect('perm_error')

    if request.method == 'POST':
        plus = float(request.POST.get('plus', 0))
        minus = float(request.POST.get('minus', 0))

        last_revision_value = plus - minus

        shop = task.shop
        shop.last_revision = last_revision_value
        shop.save()

        task.plus = plus
        task.minus = minus
        task.complete_task()

        revisor.shops += 1
        revisor.save()

        max_position = Shop.objects.aggregate(models.Max('position'))['position__max'] or 0
        shop.position = max_position + 1
        shop.last_counted_by = revisor
        shop.save()
        
        
        return redirect(f'/rate_shop/{shop.id}/')

    return redirect('assign_shop')