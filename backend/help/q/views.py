
from django.shortcuts import redirect, render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import Shop
from .forms import ShopForm

def shop_list(request):
    shops = Shop.objects.all()
    return render(request, 'q.html', {'shops': shops})



@csrf_exempt
def reorder_shops(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for item in data['order']:
            Shop.objects.filter(id=item['id']).update(position=item['position'])
        return JsonResponse({'status': 'ok'})
    

def shop_list(request):
    shops = Shop.objects.all()
    return render(request, 'q.html', {'shops': shops})

def shop_add(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
    else:
        form = ShopForm()
    return render(request, 'shop_add.html', {'form': form})

def shop_edit(request, shop_id):
    shop = Shop.objects.get(id=shop_id)
    if request.method == 'POST':
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
    else:
        form = ShopForm(instance=shop)
    return render(request, 'shop_edit.html', {'form': form})

def shop_delete(request, shop_id):
    shop = Shop.objects.get(id=shop_id)
    if request.method == 'POST':
        shop.delete()
        return redirect('shop_list')
    return render(request, 'shop_delete.html', {'shop': shop})