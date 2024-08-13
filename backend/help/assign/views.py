from django.shortcuts import render, redirect
from main.models import Revisor, Shop, Task
from .utils import assign_shop_to_revisor
from django.shortcuts import get_object_or_404


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
    
    tasks = Task.objects.filter(completed_at__isnull=True)

    return render(request, 'assign.html', {
        'revisors': revisors,
        'message': message,
        'tasks': tasks
    })

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    revisor = task.revisor
    task.complete_task()
    revisor.shops += 1
    revisor.save()
    return redirect('assign_shop')
