import random
from main.models import Shop, Revisor, Task
from django.db import models

def assign_shop_to_revisor(revisor: Revisor):

    included_status = ['new', 'transported', 'c1', 'normal']
    
    active_task_shops = Task.objects.filter(completed_at__isnull=True).values_list('shop_id', flat=True)

    top_5_shops = Shop.objects.filter(
        status__in=included_status
    ).exclude(
        id__in=active_task_shops  
    ).exclude(
        last_counted_by=revisor
    ).order_by(
        'position'
    )[:5]

    
    if top_5_shops.exists():
        shop_to_assign = random.choice(top_5_shops)

        revisor.now_shop = shop_to_assign
        revisor.save()
        max_position = Shop.objects.aggregate(models.Max('position'))['position__max'] or 0
        shop_to_assign.position = max_position + 1
        shop_to_assign.last_counted_by = revisor
        shop_to_assign.save()

        Task.objects.create(
            shop=shop_to_assign,
            revisor=revisor
        )
        return shop_to_assign
    


    else:
        return None 