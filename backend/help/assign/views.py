from django.shortcuts import render, redirect
from main.models import Revisor, Shop
from .utils import assign_shop_to_revisor

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

    revisors = Revisor.objects.all()
    return render(request, 'assign.html', {'revisors': revisors, 'message': message})
